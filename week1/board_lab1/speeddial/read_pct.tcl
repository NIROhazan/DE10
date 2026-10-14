# Reads every tester's % wrong from a board running speeddial.sof, over the USB cable.
#   quartus_stp -t read_pct.tcl
# Prints one row per clock: MHz, then % wrong for 8-bit add, 64-bit add, multiply, divide.
set hw [lindex [get_hardware_names] 0]
set dev [lindex [get_device_names -hardware_name $hw] 0]
start_insystem_source_probe -hardware_name $hw -device_name $dev
set v [read_probe_data -instance_index 0]
end_insystem_source_probe
# v is a binary string, most significant bit first: bit 168 = PLL locked
set bits [string reverse $v]
puts "locked: [string index $bits 168]"
puts [format "%6s %8s %8s %8s %8s" MHz add8 add64 mult div]
foreach f {0 1 2 3 4 5} mhz {10 25 50 100 200 300} {
    set row {}
    foreach o {0 1 2 3} {
        set lo [expr {($f * 4 + $o) * 7}]
        set b [string reverse [string range $bits $lo [expr {$lo + 6}]]]
        lappend row [expr "0b$b"]
    }
    puts [format "%6s %8s %8s %8s %8s" $mhz {*}$row]
}
