# week 4 ex9 - glitches: the hidden functions

| puzzle | Y (minimal SOP) | the glitch | fix term | NOT AND OR delays | first -> last |
|---|---|---|---|---|---|
| 0 | Y = A'C + AB' | SW0 (A) falls from ABC = 101 | B'C | 2 5 1 | 6 -> 8 |
| 1 | Y = B'C' + A'C | SW2 (C) falls from ABC = 001 | A'B' | 2 2 4 | 6 -> 8 |
| 2 | Y = B'C' + AB | SW1 (B) falls from ABC = 110 | AC' | 6 4 1 | 5 -> 11 |
| 3 | Y = A'C' + BC | SW2 (C) falls from ABC = 011 | A'B | 4 5 2 | 7 -> 11 |
| 4 | Y = A'C' + B'C | SW2 (C) falls from ABC = 001 | A'B' | 3 2 4 | 6 -> 9 |
| 5 | Y = B'C' + AC | SW2 (C) falls from ABC = 101 | AB' | 2 5 1 | 6 -> 8 |
| 6 | Y = B'C + A'B | SW1 (B) falls from ABC = 011 | A'C | 5 3 3 | 6 -> 11 |
| 7 | Y = A'B + AC' | SW0 (A) falls from ABC = 110 | BC' | 3 5 1 | 6 -> 9 |

The glitch: V falls while both other literals are 1 - V L2 turns off after AND+OR, L1 V' turns on only after NOT+AND+OR.
V rising gives no glitch (the slow term turns off after the fast one turned on). SW6 up adds L1 L2: no glitch.
