# Flicker transmitter (second DE10-Lite)

A "lamp" with an exactly known flicker, for the D5M camera's flicker meter (`../d5m_camera`, `SW6`).
All 10 red LEDs and the 7-segment displays blink together, 50 % on / 50 % off, at the frequency set on the switches.

| | |
|---|---|
| `SW9..SW0` | Frequency in Hz, binary (100 Hz = `SW6` + `SW5` + `SW2`; 120 Hz = `SW6..SW3`) |
| `KEY0` held | Steady on - no flicker, the meter should drop to 0 |
| `KEY1` held | Off |
| `HEX5..HEX0` | As much light as possible: every display fully lit with its dot (`8.`), except the frequency digits (no leading zeros), e.g. `8. 8. 8. 1. 3. 7.` From ~50 Hz up the eye sees it steady (dimmer); the camera sees it blink |

The square wave is the top bit of a 48-bit phase accumulator (DDS) that adds `SW x 2^48 / 50 MHz` every clock:
exact to about 1e-7 at any frequency, with no divider.

**Demo:** camera board in flicker mode (`SW6` up), its camera 10-20 cm from this board so the LEDs and displays fill
much of the picture, room dimmed. The camera board's HEX and the monitor should show what this board's HEX shows.
Useful range: ~30-300 Hz (the meter smooths over ~8 sensor rows; a stripe has to be wider than that).

Build (from a plain path, like the camera project): `quartus_sh --flow compile flicker_tx`.
Simulation: `cd sim`, `iverilog -g2005 -o tx.vvp tb_flicker_tx.v ../flicker_tx.v && vvp -n tx.vvp` (~10 s) -
checks 100, 137 and 1000 Hz to 0.01 %, the duty, the HEX digits and both keys.
