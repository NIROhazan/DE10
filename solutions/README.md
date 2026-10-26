# solutions/ - the source of the class exercises and the answers (instructor only)

Everything the student folders `week2` ... `week11` are built from: the question generators, the answer keys and the
grading tools. The repo is public, so students can read this folder too.

The paths are absolute: clone the repo to `C:\DE10`.

## Fixing or changing a question (weeks 3-11, DE10-Lite)

1. Edit the question in its generator:
   - week 3: `class_exercise/gen.py` (the lecture-3 engine, used by every week)
   - weeks 5-11: `weekN/class_exercise/gen_wN.py` (with `wk_common.py`)
   - weeks 2 and 4: `week2/class_exercise/gen_w2.py`, `week4/class_exercise/gen_w4.py`
2. Check it, then build the DE10-Lite boards into `C:\DE10\weekN` (Quartus Prime Lite 25.1, `C:\altera_lite\25.1std`):

   ```
   cd C:\DE10\solutions\de10
   py port.py N                          # simulate week N, write weekN\questions.txt and QUESTIONS.md
   py port.py N --compile --only Q13     # build weekN\sof\Q13.sof (leave out --only for all of them)
   py port.py N --id <student ID>        # a student's login number, every step's answer and the codes
   ```

3. Commit `weekN/` (and the generator here) and push.

`py gen_wN.py` (in `weekN/class_exercise`) runs the same questions on the old DE1 board (Quartus II 13.0sp1) and
writes into `solutions/de1/weekN`, never into the student folders.

## Grading

- `verify.bat <folder>`: checks the `moodle.txt` files students handed in, writes `grades.csv`.
- `answers.bat <exercise> <ID>`: a student's answers and codes.
- `class_exercise/key.txt`: the key that the codes come from. If you change it, every code changes.

## Not here

`C:\DE10_solutions\class_exercise_de10\` (the week 2 DE10 engine) and `C:\DE10_solutions\old_exercises\`, which the main
README mentions, are not on this computer. Ask whoever built them.
