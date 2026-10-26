#!/bin/sh
cd /c/DE10/solutions/de10
for w in 3 4 5 6 7 8 9 10 11; do
  py port.py $w --compile --jobs 4 > log_week$w.txt 2>&1
  echo "week $w exit $?" >> build_all.log
done
echo ALL DONE >> build_all.log
