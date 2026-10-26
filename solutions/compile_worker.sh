#!/bin/bash
# A compile worker: takes week numbers from compile_queue.txt (one per line) and runs gen_wN.py --compile for each.
# Stops after 40 minutes with an empty queue. Results: weekN/class_exercise/build_log.txt and compile_done.txt.
cd /c/DE10/solutions
idle=0
while [ $idle -lt 240 ]; do
	w=""
	if mkdir queue.lock 2>/dev/null; then
		w=$(head -1 compile_queue.txt 2>/dev/null)
		[ -n "$w" ] && sed -i '1d' compile_queue.txt
		rmdir queue.lock
	fi
	if [ -z "$w" ]; then idle=$((idle + 1)); sleep 10; continue; fi
	idle=0
	if [ "$w" = "3" ]; then d=class_exercise; g=gen.py; else d=week$w/class_exercise; g=gen_w$w.py; fi
	(cd $d && PYTHONIOENCODING=utf-8 python -u $g --compile > build_log.txt 2>&1)
	f=$d/build_log.txt
	echo "w$w: $(grep -c compiled $f) compiled, $(grep fails $f | grep -vc ' 0 fails') bad sims, $(tail -1 $f)" >> compile_done.txt
done
