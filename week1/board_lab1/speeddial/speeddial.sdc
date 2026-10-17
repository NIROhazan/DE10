# 50 MHz board clock + the PLL's five outputs (10, 25, 100, 200, 300 MHz).
create_clock -name clk50 -period 20.000 [get_ports MAX10_CLK1_50]
derive_pll_clocks
derive_clock_uncertainty

set_false_path -from [get_ports {SW[*] KEY[*]}]
set_false_path -to   [get_ports {LEDR[*] HEX0[*] HEX1[*] HEX2[*] HEX3[*] HEX4[*] HEX5[*]}]

# The "settled" answer is captured 24 cycles after the operands change, on purpose.
set_multicycle_path -setup 24 -from [get_registers {*|a[*] *|b[*] *|cin}] -to [get_registers {*|r_slow[*]}]
set_multicycle_path -hold  23 -from [get_registers {*|a[*] *|b[*] *|cin}] -to [get_registers {*|r_slow[*]}]

# The judge (op_tester.sv): each step reads data written at least 3 cycles before, and is enabled by
# its own strobe flip-flop. Only the strobes themselves and a/b -> r_fast are one-cycle paths.
set judge_from [get_registers {*|lfsr[*] *|r_fast[*] *|r_slow[*] *|mismatch *|wrong[*] *|tests[*] *|wrong_done[*]}]
set judge_to   [get_registers {*|lfsr[*] *|a[*] *|b[*] *|cin *|mismatch *|wrong[*] *|tests[*] *|wrong_done[*] *|pct[*]}]
set_multicycle_path -setup 3 -from $judge_from -to $judge_to
set_multicycle_path -hold  2 -from $judge_from -to $judge_to

# Error percentages cross from each test clock into the 50 MHz display through a synchroniser.
set_false_path -to [get_registers {*pct_meta[*]}]

# The single-cycle path a/b -> r_fast is the one under test: it is EXPECTED to fail
# timing at the faster clocks. The Timing Analyzer's Fmax per clock is the fallback demo.
