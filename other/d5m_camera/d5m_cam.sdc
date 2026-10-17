create_clock -name clk50 -period 20.000 [get_ports MAX10_CLK1_50]
create_generated_clock -name clk25 -source [get_ports MAX10_CLK1_50] -divide_by 2 [get_registers clk25]
create_clock -name pclk -period 40.000 [get_ports D5M_PIXCLK]
derive_clock_uncertainty

# camera clock and board clock are unrelated
set_clock_groups -asynchronous -group {clk50 clk25} -group {pclk}

# camera data: the sensor changes it on the other PIXCLK edge (R0x0A inverts PIXCLK)
set_input_delay -clock pclk -max 15 [get_ports {D5M_D[*] D5M_LVAL D5M_FVAL}]
set_input_delay -clock pclk -min 2  [get_ports {D5M_D[*] D5M_LVAL D5M_FVAL}]

# switches, keys, LEDs, displays, VGA, camera control: slow or not timed
set_false_path -from [get_ports {SW[*] KEY[*] D5M_STROBE D5M_SDATA}]
set_false_path -to   [get_ports {LEDR[*] HEX*[*] VGA_* D5M_XCLKIN D5M_RESET_N D5M_TRIGGER D5M_SCLK D5M_SDATA}]
