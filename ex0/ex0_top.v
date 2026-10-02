// Exercise 0 - LED wave demo on the Terasic DE1.  Wraps led_wave.v (written for the DE10-Lite).
//
//   CLOCK_50 (50 MHz, PIN_L1) drives led_wave's clk
//   LEDR9..LEDR0 = the travelling hump of light, left to right
module ex0_top(
	input        CLOCK_50,
	output [9:0] LEDR
	);

	led_wave u_wave(
		.clk (CLOCK_50),
		.LEDR(LEDR)
	);

endmodule
