# Starts the white balance from the PC, like pressing KEY1: quartus_stp -t wb.tcl
set hw [lindex [get_hardware_names] 0]
set dev [lindex [get_device_names -hardware_name $hw] 0]
start_insystem_source_probe -device_name $dev -hardware_name $hw
write_source_data -instance_index 0 -value 1
after 100
write_source_data -instance_index 0 -value 0
end_insystem_source_probe
puts "white balance started"
