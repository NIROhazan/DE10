# The link to the board (run by run.ps1 through quartus_stp): In-System Sources and Probes over the USB cable.
#   quartus_stp -t link.tcl <source hex>   writes {go, start step, login} into the board, then prints
#   "P <probe hex>" every time the board's {done, step, code} changes.  "X" = the link is lost.
if {[info exists quartus(args)] && [llength $quartus(args)] > 0} { set src [lindex $quartus(args) 0] } else { set src [lindex $argv 0] }
set hw [lindex [get_hardware_names] 0]
set dev [lindex [get_device_names -hardware_name $hw] 0]
start_insystem_source_probe -device_name $dev -hardware_name $hw
write_source_data -instance_index 0 -value $src -value_in_hex
puts "LINK OK"
flush stdout
set prev ""
set stop 0
if {[info exists env(CE_TEST_SECONDS)]} { set stop [expr {[clock seconds] + $env(CE_TEST_SECONDS)}] }
while {$stop == 0 || [clock seconds] < $stop} {
	if {[catch {set v [read_probe_data -instance_index 0 -value_in_hex]}]} { puts "X"; flush stdout; break }
	if {$v ne $prev} { puts "P $v"; flush stdout; set prev $v }
	after 150
}
catch { end_insystem_source_probe }
if {$stop != 0} { puts "X"; flush stdout }
