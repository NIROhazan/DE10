// Exercise 11 - from a story to an equation.  DO NOT EDIT: Claude writes student_logic.v from answer.txt.
//
//   SW0 = A, SW1 = B, SW2 = C        HEX3 = A, HEX2 = B, HEX1 = C, HEX0 = Y
//   LEDG0 = Y from your story (the target)
//   LEDR0 = your SOP   LEDR1 = your minimal SOP   LEDR2 = your minimal POS
//   LEDR9 = ALARM: one of your answers disagrees with Y on this row
//
// VARIANTS: perms=ABC masks=-   (the story is personal: tools/stories.txt)
// GRADE: SOP : CSOP
// GRADE: MSOP : SOP MIN
// GRADE: MPOS : POS MIN
// ASK Q1 SOP: SOP | Canonical SOP of your story: one minterm for every row where Y = 1
// ASK Q2 MSOP: MSOP | Minimal SOP of your story: the fewest terms, then the fewest literals
// ASK Q3 MPOS: MPOS | Minimal POS of your story: the fewest sums, then the fewest literals
// TEXT Q4 1: Write the truth table of your story as the 8 values of Y for the rows ABC = 000 to 111, and explain how you got the row A=1 B=1 C=1.
// TEXT Q5 2: Your story has the shape 'X and (Y or Z)'. Which variable is outside the parentheses? Give one row (ABC) where 'X and (Y or Z)' and '(X and Y) or Z' give different answers.
// TEXT Q6 3: Write Y with the Sigma notation (the minterm numbers) and with the Pi notation (the maxterm numbers). Why do the two lists together hold every number 0-7 exactly once?
// TEXT Q7 4: Predict before you move the switches: A=1 B=0 C=1 - what will LEDG0 be, and which LEDR lights will be on?
// Truth table:  A B C | Y
//               0 0 0 | 0
//               0 0 1 | 1
//               0 1 0 | 1
//               0 1 1 | 1
//               1 0 0 | 0
//               1 0 1 | 0
//               1 1 0 | 0
//               1 1 1 | 0
module ex11_top(
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
			3'b010: Y = 1'b1;
			3'b011: Y = 1'b1;
			3'b100: Y = 1'b0;
			3'b101: Y = 1'b0;
			3'b110: Y = 1'b0;
			3'b111: Y = 1'b0;
		endcase
	end

	wire s_sop, s_msop, s_mpos;
	student_logic u(.A(A), .B(B), .C(C), .SOP(s_sop), .MSOP(s_msop), .MPOS(s_mpos));

	wire alarm = (s_sop != Y) | (s_msop != Y) | (s_mpos != Y);

	assign LEDG    = {7'b0, Y};
	assign LEDR    = {alarm, 6'b0, s_mpos, s_msop, s_sop};

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
