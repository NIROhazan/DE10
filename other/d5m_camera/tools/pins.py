# Decodes the pin monitor: py pins.py  (runs quartus_stp -t pins.tcl and prints a table of the 36 header pins)
import re, subprocess, sys, os
Q = r"C:\altera_lite\25.1std\quartus\bin64\quartus_stp.exe"
here = os.path.dirname(os.path.abspath(__file__))
out = subprocess.run([Q, "-t", os.path.join(here, "pins.tcl")], capture_output=True, text=True).stdout
m = re.search(r"^P ([0-9A-Fa-f]+)", out, re.M)
if not m: sys.exit("no probe data:\n" + out)
v = int(m.group(1), 16)
def f(lo, n): return (v >> lo) & ((1 << n) - 1)
lvl, pixels, lines, frames, nack, done = f(0, 36), f(36, 12), f(48, 12), f(60, 8), f(68, 1), f(69, 1)
name = {0: "PIXCLK", 1: "D11", 3: "D10", 4: "D9", 5: "D8", 6: "D7", 7: "D6", 8: "D5", 9: "D4", 10: "D3", 11: "D2",
        12: "D1", 13: "D0", 16: "XCLKIN (out)", 17: "RESET_N (out)", 19: "TRIGGER (out)", 20: "STROBE", 21: "LVAL",
        22: "FVAL", 23: "SDATA", 24: "SCLK (out)"}
rowp, framep, expo, gall, gr, gb = f(362, 16), f(378, 26), f(404, 16), f(420, 8), f(428, 8), f(436, 8)
print(f"config done={done} nack={nack}  frames={frames} lines={lines:#x} pixels={pixels:#x}")
print(f"row period {rowp} PIXCLK = {rowp/25:.1f} us   frame period {framep} PIXCLK = {framep/25e3:.1f} ms ({25e6/max(framep,1):.1f} fps)")
print(f"exposure {expo} rows")
evc, thr, wbb, evm = f(444, 17), f(461, 3), f(464, 1), f(466, 1)
print(f"event camera {'ON' if evm else 'off'}  threshold {thr + 1}  events last frame {evc}   white balance R x{gr/64:.2f} B x{gb/64:.2f}{' (measuring)' if wbb else ''}")
mq = re.search(r"^Q ([0-9A-Fa-f]+)", out, re.M)
w = int(mq.group(1), 16) if mq else 0
def g(lo, n): return (w >> lo) & ((1 << n) - 1)
f10, fln = g(0, 17), g(17, 8)
fsw, fno = g(25, 23), g(48, 25)
print(f"flicker {f10/10:.1f} Hz ({fln} stripes in the last frame, stripe size {fsw}, noise {fno}, ratio {fsw/max(fno,1):.1f} - needs 1.5)")
print("GPIO hdr-pin  level  edges/21ms  D5M signal")
for g in range(36):
    pin = g + 1 + (2 if g >= 10 else 0) + (2 if g >= 26 else 0)
    print(f"{g:4d} {pin:7d} {f(g,1):6d} {f(74 + 8*g, 8):10d}   {name.get(g, '-')}")
