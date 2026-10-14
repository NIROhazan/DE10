// Exercise 0 - LED wave on the Terasic DE10-Lite.  Wraps led_wave.v.
//
//   MAX10_CLK1_50 (50 MHz, PIN_P11) drives led_wave's clk
//   LEDR9..LEDR0 = the travelling hump of light, left to right
//
// Change ONLY the numbers in the KNOBS block, save, run run.bat.
// Write your prediction in answer.txt BEFORE you run.
module ex0_top(
	input        MAX10_CLK1_50,
	output [9:0] LEDR
	);

	// ===================== KNOBS =====================
	// Clock cycles per step. The clock ticks 50,000,000 times a second.
	localparam MOVE_DIV = 15_000_000;

	// Brightness in percent of the time the LED is on.
	localparam PEAK = 99;	// the brightest LED
	localparam B1   = 60;	// one LED away from it
	localparam B2   = 30;	// two LEDs away
	localparam B3   = 10;	// three LEDs away (further away = off)
	// =================================================

	led_wave #(
		.MOVE_DIV(MOVE_DIV),
		.PEAK    (PEAK),
		.B1      (B1),
		.B2      (B2),
		.B3      (B3)
	) u_wave(
		.clk (MAX10_CLK1_50),
		.LEDR(LEDR)
	);

endmodule
