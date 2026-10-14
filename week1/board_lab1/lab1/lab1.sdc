# 50 MHz board clock. Without create_clock Quartus does no timing analysis at all.
create_clock -name clk50 -period 20.000 [get_ports MAX10_CLK1_50]
derive_clock_uncertainty

# Switches, buttons, LEDs and displays are human-speed and asynchronous: not timed.
set_false_path -from [get_ports {SW[*] KEY[*]}]
set_false_path -to   [get_ports {LEDR[*] HEX0[*] HEX1[*] HEX2[*] HEX3[*] HEX4[*] HEX5[*]}]
