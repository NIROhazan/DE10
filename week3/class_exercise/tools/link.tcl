# The link to the board (run by run.ps1 through quartus_stp): In-System Sources and Probes over the USB cable.
#   quartus_stp -t link.tcl <source hex> <state file>
# first writes 0 (the board drops to "waiting" and forgets its step), then {go, start step, login} - so a new link can
# move the board to ANY step (resume, or going back to a step already done). Then it keeps the board's
# {done, step, code} in the state file: "P <probe hex>" (rewritten on every change), "X" = the link is lost.
# A file, not stdout: quartus_stp holds back its stdout in a pipe until it exits, so run.ps1 could not follow it.
if {[info exists quartus(args)] && [llength $quartus(args)] > 1} { set a $quartus(args) } else { set a $argv }
set src [lindex $a 0]
set out [lindex $a 1]
proc state {t} {
	global out
	set tmp "$out.tmp"
	set f [open $tmp w]; puts $f $t; close $f
	file rename -force $tmp $out
}
if {[catch {
	set hw [lindex [get_hardware_names] 0]
	set dev [lindex [get_device_names -hardware_name $hw] 0]
	start_insystem_source_probe -device_name $dev -hardware_name $hw
	write_source_data -instance_index 0 -value "0000" -value_in_hex
	after 100
	write_source_data -instance_index 0 -value $src -value_in_hex
} err]} { state "X $err"; exit 1 }
set prev ""
set stop 0
if {[info exists env(CE_TEST_SECONDS)]} { set stop [expr {[clock seconds] + $env(CE_TEST_SECONDS)}] }
while {$stop == 0 || [clock seconds] < $stop} {
	if {[catch {set v [read_probe_data -instance_index 0 -value_in_hex]}]} { state "X"; break }
	if {$v ne $prev} { state "P $v"; set prev $v }
	after 150
}
catch { end_insystem_source_probe }
if {$stop != 0} { state "X" }
