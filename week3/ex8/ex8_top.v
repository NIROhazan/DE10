// Exercise 8 - NAND only and NOR only.  DO NOT EDIT: Claude writes student_logic.v from answer.txt.
//
//   SW0 = A, SW1 = B, SW2 = C        HEX3 = A, HEX2 = B, HEX1 = C, HEX0 = Y
//   LEDG0 = Y from the truth table (the target)
//   LEDR0 = your SOP   LEDR1 = your POS   LEDR2 = your NAND   LEDR3 = your NOR
//   LEDR9 = ALARM: one of your answers disagrees with Y on this row
//
// ONLY: SOP : SOP
// ONLY: POS : POS
// ONLY: NAND : NAND
// ONLY: NOR : NOR
// GRADE: SOP : SOP MIN
// GRADE: POS : POS MIN
// ASK Q1 SOP: SOP | Minimal SOP (K-map of the 1s)
// ASK Q2 POS: POS | Minimal POS (K-map of the 0s)
// ASK Q3 NAND: NAND | Y with NAND gates only, built from your SOP. A NAND is written (XY)'
// ASK Q4 NOR: NOR | Y with NOR gates only, built from your POS. A NOR is written (X + Y)'
// TEXT Q5 1: Bubble pushing: why can the AND-OR levels of the SOP be replaced by NAND-NAND without changing Y? Which theorem does this use?
// TEXT Q6 2: How many NAND gates are in your NAND expression, and how many NOR gates in your NOR expression? (A' alone counts as one gate.)
// TEXT Q7 3: Why is NAND called a 'universal gate'? Show how to build NOT, AND and OR from NAND only.
// TEXT Q8 4: Predict before you move the switches: A=1 B=1 C=0 - what will LEDG0 be, and which LEDR lights will be on?
// Truth table:  A B C | Y
//               0 0 0 | 0
//               0 0 1 | 0
//               0 1 0 | 0
//               0 1 1 | 1
//               1 0 0 | 1
//               1 0 1 | 1
//               1 1 0 | 0
//               1 1 1 | 1
module ex8_top(
	input  [9:0] SW,
	output [7:0] LEDG,
	output [9:0] LEDR,
	output [6:0] HEX0,
	output [6:0] HEX1,
	output [6:0] HEX2,
	output [6:0] HEX3
	);

	wire A = SW[0];
	wire B = SW[1];
	wire C = SW[2];

	// The target as a lookup, written without any expression
	reg Y;
	always @(*) begin
		case ({A, B, C})
			3'b000: Y = 1'b0;
			3'b001: Y = 1'b0;
			3'b010: Y = 1'b0;
			3'b011: Y = 1'b1;
			3'b100: Y = 1'b1;
			3'b101: Y = 1'b1;
			3'b110: Y = 1'b0;
			3'b111: Y = 1'b1;
		endcase
	end

	wire sop, pos, g_nand, g_nor;
	student_logic u(.A(A), .B(B), .C(C), .SOP(sop), .POS(pos), .NAND(g_nand), .NOR(g_nor));

	wire alarm = (sop != Y) | (pos != Y) | (g_nand != Y) | (g_nor != Y);

	assign LEDG    = {7'b0, Y};
	assign LEDR    = {alarm, 5'b0, g_nor, g_nand, pos, sop};

	// 7-segment, active low: "0" and "1" only
	function [6:0] bit7;
		input b;
		bit7 = b ? 7'b1111001 : 7'b1000000;
	endfunction

	assign HEX3 = bit7(A);
	assign HEX2 = bit7(B);
	assign HEX1 = bit7(C);
	assign HEX0 = bit7(Y);
endmodule
