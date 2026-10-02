// The "locked" board: run.bat programs this whenever it stops (empty or wrong answers),
// so the board never keeps showing an older design that looks correct.
//
//   HEX3..HEX1 = "Err", HEX0 off, all red and green LEDs off
module locked(
	output [9:0] LEDR,
	output [7:0] LEDG,
	output [6:0] HEX0,
	output [6:0] HEX1,
	output [6:0] HEX2,
	output [6:0] HEX3
	);

	assign LEDR = 10'b0;
	assign LEDG = 8'b0;

	// 7-segment, active low, bits = g f e d c b a
	assign HEX3 = 7'b0000110;	// E
	assign HEX2 = 7'b0101111;	// r
	assign HEX1 = 7'b0101111;	// r
	assign HEX0 = 7'h7F;		// off
endmodule
