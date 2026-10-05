// Exercise 8 - De Morgan, multiplying out, factoring.  DO NOT EDIT: Claude writes student_logic.v from answer.txt.
//
//   SW0 = A, SW1 = B, SW2 = C        HEX3 = A, HEX2 = B, HEX1 = C, HEX0 = Y
//   LEDG0 = Y (the expression you were given)
//   LEDR0 = your DM   LEDR1 = your SOP   LEDR2 = your POS
//   LEDR9 = ALARM: one of your answers disagrees with Y on this row
//
// EXPR: ((A + B'C)' + A'B)'
// ONLY: DM : LITNOT
// ONLY: SOP : SOP
// ONLY: POS : POS
// GRADE: SOP : SOP MIN
// GRADE: POS : POS MIN
// ASK Q1 DM: DM | Y after De Morgan, from the outside in: no ' after a parenthesis - only on single variables
// ASK Q2 SOP: SOP | Minimal SOP (multiplying out): the fewest terms, then the fewest literals
// ASK Q3 POS: POS | Minimal POS (factoring, T8'): the fewest sums, then the fewest literals
// TEXT Q4 1: What is the complement of a product by De Morgan, and what is the complement of a sum? Write both forms (T12 and T12') with B and C.
// TEXT Q5 2: Why do we start from the outer ' and not from the inner one? What would have happened in your expression if you had started from the inside?
// TEXT Q6 3: To get from SOP to POS you used T8': W + XZ = (W + X)(W + Z). What were W, X and Z for you?
// TEXT Q7 4: Predict before you move the switches: A=0 B=1 C=1 - what will LEDG0 be, and which LEDR lights will be on?
// Truth table:  A B C | Y
//               0 0 0 | 0
//               0 0 1 | 1
//               0 1 0 | 0
//               0 1 1 | 0
//               1 0 0 | 1
//               1 0 1 | 1
//               1 1 0 | 1
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
			3'b001: Y = 1'b1;
			3'b010: Y = 1'b0;
			3'b011: Y = 1'b0;
			3'b100: Y = 1'b1;
			3'b101: Y = 1'b1;
			3'b110: Y = 1'b1;
			3'b111: Y = 1'b1;
		endcase
	end

	wire dm, sop, pos;
	student_logic u(.A(A), .B(B), .C(C), .DM(dm), .SOP(sop), .POS(pos));

	wire alarm = (dm != Y) | (sop != Y) | (pos != Y);

	assign LEDG    = {7'b0, Y};
	assign LEDR    = {alarm, 6'b0, pos, sop, dm};

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
