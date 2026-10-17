# make_log.py - writes log.hex: 10-bit linear brightness -> 8-bit log brightness, for the event camera.
#   L = 255 * (log2(i + 8) - 3) / (log2(1031) - 3)
# The +8 keeps the darkest levels (where sensor noise is largest) from spreading over many log steps.
# 255 covers ~7 stops, so one stop (x2 in light) is ~36 log steps.
import math, os
top = math.log2(1023 + 8) - 3
with open(os.path.join(os.path.dirname(__file__), "..", "log.hex"), "w") as f:
    for i in range(1024):
        f.write("%02x\n" % round(255 * (math.log2(i + 8) - 3) / top))
