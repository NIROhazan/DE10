# Reads the pin monitor once: quartus_stp -t pins.tcl  -> prints "P <hex>"
set hw [lindex [get_hardware_names] 0]
set dev [lindex [get_device_names -hardware_name $hw] 0]
start_insystem_source_probe -device_name $dev -hardware_name $hw
after 100
puts "P [read_probe_data -instance_index 0 -value_in_hex]"
puts "Q [read_probe_data -instance_index 1 -value_in_hex]"
end_insystem_source_probe
