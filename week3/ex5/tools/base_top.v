// Exercise 5 - simplifying with the theorems.  DO NOT EDIT: Claude writes student_logic.v from answer.txt.
//
//   SW0 = A, SW1 = B, SW2 = C        HEX3 = A, HEX2 = B, HEX1 = C, HEX0 = Y
//   LEDG0 = Y (the expression you were given)
//   LEDR0-LEDR7 = your steps S1-S8     LEDR8 = your final MIN
//   LEDR9 = ALARM: one of your answers disagrees with Y on this row
//
// EXPR: AB + A(B + C)' + A'BC
// ONLY: MIN : SOP
// GRADE: MIN : SOP MIN
// ASK Q1 STEPS: S1 S2 S3 S4 S5 S6 S7 S8 | Simplify Y step by step: ONE theorem per step, its name in [ ], e.g.  B(A + A')   [T8]
// ASK Q2 MIN: MIN | The final expression: a minimal SOP
// TEXT Q3 1: In which step did the ' over the parentheses disappear? Write that theorem in its general form (with B, C, D as in the table of the lecture).
// TEXT Q4 2: At the end of the simplification a whole term disappeared. Which term, by which theorem, and why may it be removed without changing Y?
// TEXT Q5 3: Prove 'Simplification' A + A'P = A + P by method 1 (perfect induction). How many rows does the table need, and why is that enough as a proof?
// TEXT Q6 4: Predict before you move the switches: A=1 B=0 C=1 - what will LEDG0 be, and which LEDR lights will be on?
// Truth table:  A B C | Y
//               0 0 0 | 0
//               0 0 1 | 0
//               0 1 0 | 0
//               0 1 1 | 1
//               1 0 0 | 1
//               1 0 1 | 0
//               1 1 0 | 1
//               1 1 1 | 1
module ex5_top(
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
			3'b101: Y = 1'b0;
			3'b110: Y = 1'b1;
			3'b111: Y = 1'b1;
		endcase
	end

	wire s1, s2, s3, s4, s5, s6, s7, s8, min;
	student_logic u(.A(A), .B(B), .C(C), .S1(s1), .S2(s2), .S3(s3), .S4(s4), .S5(s5), .S6(s6), .S7(s7), .S8(s8), .MIN(min));

	wire alarm = (s1 != Y) | (s2 != Y) | (s3 != Y) | (s4 != Y) | (s5 != Y) | (s6 != Y) | (s7 != Y) | (s8 != Y) | (min != Y);

	assign LEDG    = {7'b0, Y};
	assign LEDR    = {alarm, min, s8, s7, s6, s5, s4, s3, s2, s1};

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
