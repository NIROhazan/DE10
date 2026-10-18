# D5M camera -> VGA (DE10-Lite)

Terasic **TRDB-D5M** camera on the DE10-Lite's 2x20 GPIO header (JP1), picture on a VGA monitor
(640 x 480; 320 x 240 camera pixels, each drawn 2 x 2). Everything stays on the chip: the frame
buffer (RGB565, 16 bits per pixel) is 152 of the 10M50's 182 M9K memory blocks, no SDRAM.

| File | What it is |
|---|---|
| `tools/demo.ps1` | Loads the demo onto one or two boards, no compile (started by `../CAMERA_DEMO.bat`) |
| `d5m_cam_top.v` | Top level: 25 MHz clock (also the camera's XCLKIN), reset, switches, LEDs, HEX |
| `d5m_i2c_cfg.v` | Writes the sensor's registers over I2C, then rewrites exposure / test pattern when SW changes |
| `d5m_capture.v` | Bayer stream -> 320 x 240 RGB565 (each 4x4 averaged), white-balance gains, event camera; measures the sensor, sums R/G/B per frame |
| `flicker.v` | Flicker frequency from the rolling-shutter stripes: row sums minus last frame's, timed swings, a division -> Hz x 10 |
| `white_bal.v` | One-shot white balance: on KEY1, sets the red and blue gains so the frame averages grey, then holds them |
| `log.hex` | Log table for the event camera, 10-bit linear -> 8-bit log, ~36 steps per doubling of light (`tools/make_log.py`) |
| `frame_ram.v` | Dual-clock frame buffer: camera clock writes (and reads, for the event camera), VGA clock reads |
| `vga_out.v` | 640 x 480 @ 60 Hz timing, pixel doubling, temporal dithering RGB565 -> the board's RGB444, colour-bar test pattern |
| `sim/tb_vga.v` | Temporal dithering: every screen pixel averages the stored 5/6-bit value over 4 frames, and every 2x2 block already does in each frame |
| `sim/tb_d5m_cam.v` | Icarus testbench with a model of the D5M (I2C slave + 1280 x 960 frames); exact pixels |
| `sim/tb_wb.v` | White balance: a tinted grey card comes out grey after KEY1, the gains then hold, KEY0 clears them |
| `sim/tb_fl.v` | Flicker: a weak (15 %) flickering lamp on a scene with a gradient and row noise reads within 1 %, a steady lamp reads 0 |
| `tools/wb.tcl` | Starts the white balance from the PC (same as `KEY1`) |
| `sim/tb_ev.v` | Event camera: still scene -> no events, a patch brightens / darkens -> exactly its ON / OFF events, fading, KEY1 |

## Controls

| | |
|---|---|
| `KEY0` | Reset: restart the camera, write its registers again, white balance back to the default |
| `KEY1` | Camera: **white balance** - fill the view with something white or grey (paper), press; red and blue are corrected over the next ~3 frames and then stay fixed. Event camera: next threshold (`HEX5`, 1..8) |
| `SW0` | VGA colour bars instead of the camera - checks the monitor and cable alone |
| `SW1` | Freeze the picture |
| `SW3..SW2` | Which corner of the 2x2 colour block is red. All down = right for this camera (found by trying, `BAYER` in the top). Green/pink picture = `SW2` wrong; red and blue swapped = `SW3` wrong |
| `SW4` | The sensor sends its own colour bars - checks the camera -> FPGA path |
| `SW5` | **Event camera** (see below) |
| `SW6` | **Flicker** (see below). `KEY1` = next exposure, `SW5` = light smoothing, `SW9..SW7` = display brightness |
| `SW9..SW7` | Exposure `128 << SW` rows (0 = darkest, 7 = brightest) |

| Display | Meaning |
|---|---|
| `HEX5..HEX3` | Lines per frame in hex - expect `3C0` (960) |
| `HEX2..HEX0` | Pixels per line in hex - expect `500` (1280) |
| `LEDR0` | Blinks every 8 frames: frames are arriving |
| `LEDR1` | Camera registers written |
| `LEDR2` | A register write got no acknowledge: the camera is not answering on I2C |
| `LEDR3` | Blinks while the camera's PIXCLK runs |
| `LEDR4` / `LEDR5` | FVAL / LVAL straight from the camera |
| `LEDR7` | White balance measuring |
| `LEDR8` | White balance set (gains not x1) |
| `LEDR9` | Event camera on |
| `HEX5` / `HEX4..HEX0` | Event camera: threshold 1..8 / events in the last frame, decimal |
| `HEX5..HEX0` | Flicker: `F` and the frequency in Hz with one decimal, e.g. `F 0100.0` (0 = no flicker found) |

**Event camera (`SW5`):** imitates a DVS (dynamic vision sensor). Each pixel keeps a reference log brightness; when
a frame's log brightness differs from it by more than the threshold, the pixel fires an event - green = brighter
(ON), red = darker (OFF) - and the reference moves to the new value. Events fade over ~4 frames; a still scene stays
black (with a very dim outline of the reference). Thresholds 1..8 = 3, 5, 8, 12, 16, 24, 32, 48 log steps (36 = twice
the light; default 4 = ~25% change). While it is on the exposure is rounded to a multiple of 88 rows (10 ms) so
100 Hz lamp flicker cancels. It is an emulation at the frame rate (~9 per second):
a real DVS has no frames and reacts in microseconds. The frame buffer word holds `{reference 8, polarity, age 3}`.

**Flicker (`SW6`):** the sensor reads its rows one after another, 113.3 us apart (rolling shutter), so a lamp
that flickers faster than a frame shows as horizontal stripes - an LED lamp on 50 Hz mains flickers at 100 Hz, one
stripe every ~88 rows. The exposure drops to 24 rows (2.7 ms) so the stripes are sharp. `flicker.v` adds up each
row, subtracts the same row of the previous frame (the scene cancels, the stripes stay because they move from frame
to frame), smooths over ~8 rows (the sensor's random row noise would look like thin stripes), and times the swings
from dark to bright against the 25 MHz pixel clock - good for lamp flicker up to a few hundred Hz. A frame counts
only if its swings are evenly spaced and stand out from the noise (both measured); the display averages good frames
and drops to 0 after ~2 s without one. `py tools\pins.py` prints the frequency, stripes, stripe size and noise.
Measured on a room LED lamp (2026-10-17): 98.3-99.2 Hz, 8-11 stripes per frame, stripes ~2x the noise; on a
second DE10-Lite blinking at exactly 100 Hz (`../flicker_tx`, through a paper diffuser): 100.1-101.0 Hz.

`KEY1` steps the exposure; the screen shows it under the frequency, with the flicker it cannot see (1 / exposure: a
row then catches exactly one whole cycle). The display brightens by ~24 / rows on its own; `SW9..SW7` add x 2^SW.
`SW5` up = light smoothing (~2 rows) for fast flicker, down = ~8 rows for slow flicker.

| `KEY1` presses | Exposure | Blind at | Good up to about |
|---|---|---|---|
| 0 | 24 rows (2.72 ms) | 368 Hz | 250 Hz |
| 1 | 16 rows (1.81 ms) | 552 Hz | 400 Hz |
| 2 | 12 rows (1.36 ms) | 736 Hz | 500 Hz |
| 3 | 8 rows (0.91 ms) | 1103 Hz | 750 Hz (measured: 252 and 500 Hz work, 1000 Hz fails) |
| 4 | 6 rows (0.68 ms) | 1471 Hz | 1000 Hz |
| 5 | 4 rows (0.45 ms) | 2207 Hz | ~1200 Hz |
| 6 | 3 rows (0.34 ms) | 2943 Hz | ~1200 Hz |
| 7 | 2 rows (0.23 ms) | 4414 Hz | ~1200 Hz |

Shorter exposures need more light. Above ~1.2 kHz whole-row timing is too coarse for the evenness check.

Limits: below ~37 Hz there are fewer than 4 stripes in a frame; the exposure averages a flicker away completely at
1/exposure (370 Hz low range, 1100 Hz high range); whole multiples of the frame rate (8.95 fps: 89.5, 98.5, 179.1 Hz
...) are blind, because the stripes then stand still and the frame-to-frame difference is 0; rows come every
113.3 us, so nothing above 4.4 kHz can ever be seen at this clock, and above ~1.2 kHz whole-row timing is too coarse.
Dim light lowers the top of each range (with the paper diffuser 252 Hz failed in the low range). A PC webcam cannot do this: its
exposure and row timing are hidden from the program and it usually removes flicker on purpose.

**Fault finding:** black screen with `SW0` up = monitor / VGA problem. `LEDR2` on or `LEDR3` not blinking =
camera not powered, not seated, or on the wrong header pins. HEX shows `000 000` = no LVAL/FVAL.
Picture there but too dark or white = `SW9..SW7`.

**Pin monitor (from the PC):** `py tools\pins.py` reads every header pin over the USB cable (In-System Sources and
Probes) and prints its level, its edges per ~21 ms and the D5M signal on it, plus config done/nack, frame count and
the measured size. Use it when the camera seems dead: a working camera shows PIXCLK and LVAL at 255 edges.

## Build and program

**Quickest: double-click `../CAMERA_DEMO.bat`** (in `week1/Demo`). It loads the ready-built designs, no compile: the camera design onto
the board with the D5M and, if a second DE10-Lite is plugged in, `../flicker_tx` onto that one. It finds the camera
board itself (it loads the camera design and asks whether the camera answered on I2C), so the USB ports can be in
any order. Run it again after unplugging a board.

Ready-built: `sof/d5m_cam.sof` - no compile needed, just load it (it is lost at power-off, load it again after
unplugging): `C:ltera_lite.1std\quartusin64\quartus_pgm -c USB-Blaster -m jtag -o "p;sof/d5m_cam.sof"`.
With two boards on the PC, `jtagconfig` lists them as `USB-Blaster [USB-0]` / `[USB-1]`; name the right one after `-c`.

To build it yourself:

Quartus is unreliable with Hebrew letters or spaces in a path, so build from a plain copy:

```
xcopy /E /I /Y d5m_camera C:\fpga\d5m_camera
cd /d C:\fpga\d5m_camera
C:\altera_lite\25.1std\quartus\bin64\quartus_sh --flow compile d5m_cam
C:\altera_lite\25.1std\quartus\bin64\quartus_pgm -c USB-Blaster -m jtag -o "p;output_files/d5m_cam.sof"
```

Simulation (Icarus): `cd sim`, copy `log.hex` there, then for each of `tb_d5m_cam.v` (~30 s), `tb_wb.v` (~40 s), `tb_ev.v` (~20 s) and `tb_fl.v` (~60 s) (and `tb_vga.v` with just `../vga_out.v`),
`iverilog -g2005 -DNO_PIN_MONITOR -o tb.vvp <tb> altsource_probe_stub.v ../d5m_cam_top.v ../d5m_i2c_cfg.v ../d5m_capture.v ../white_bal.v ../flicker.v ../frame_ram.v ../vga_out.v && vvp -n tb.vvp`
- each must end with `ALL CHECKS PASSED`.

## Notes

- **Picture quality:** the DE10-Lite's VGA connector has 4 bits per colour (resistor DAC on the board) - 8 bits
  would need an external DAC. The frame buffer keeps 5 / 6 / 5 bits and `vga_out.v` shows the extra bits by
  temporal dithering (FRC, as cheap LCD panels do): a pixel between two levels alternates between them from one
  60 Hz screen frame to the next, neighbours out of step, and the eye averages - ~32 / 64 / 32 levels without
  banding. Each output pixel is the average of its 4x4 sensor pixels (`AVG`), which lowers the noise. The sensor's own colour gains
  (R0x2B..0x2E) are Terasic's values, which leave a green cast under ordinary room light; `KEY1` corrects it with
  FPGA gains on red and blue, like the custom white balance of a camera. The default (red x0.59, blue x1.41) is
  what it measured under room light. Before the colour order was right (`BAYER`), the picture was green with pink
  highlights - the green pixels were being shown as red and blue. A version with gamma, dither, automatic exposure
  and grey-world white balance was tried and looked worse on this board (dot pattern, washed-out colours, the
  exposure loop hunted because the sensor applies a new exposure a frame later), so it was taken out.
- **Measured sensor timing:** one line every 113 us (2832 PIXCLK), so 960 lines + blanking = ~9 frames/s at most.
  Exposures longer than ~1000 rows lower the frame rate.

- **Pins:** D5M header pins as in Terasic's DE2-115 D5M demo (PIXCLK = pin 1, D11..D0 = pins 2, 4-10, 13-16,
  XCLKIN = 19, RESET_n = 20, TRIGGER = 22, STROBE = 23, LVAL = 24, FVAL = 25, SDATA = 26, SCLK = 27), mapped to the
  DE10-Lite's GPIO pins from its user manual (table 3-7). Everything else on the header stays an input with a weak pull-up.
- **Sensor settings:** Terasic's 640 x 480 demo values (2x bin + 2x skip of 2560 x 1920 -> 1280 x 960), but the
  sensor PLL is left off, so PIXCLK = XCLKIN = 25 MHz (about 9 frames/s at the shorter exposures, measured).
  Because the clock is ~3x slower than Terasic's, the same exposure number gives a ~3x brighter picture.
- **Test pattern mode** (`R0xA0 = 0x0041`, mode 8 = vertical colour bars) is from the MT9P001 register list; if the
  bars look different the mode number may differ, but any steady pattern proves the data path.
