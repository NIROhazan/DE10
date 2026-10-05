// Exercise 2 - SOP / POS, three inputs.  DO NOT EDIT: Claude writes student_logic.v from answer.txt.
//
//   SW0 = A, SW1 = B, SW2 = C        HEX3 = A, HEX2 = B, HEX1 = C, HEX0 = Y from the table
//   LEDG0 = Y from the truth table   (the target)
//   LEDR0 = your SOP                 LEDR1 = your POS        LEDR2 = your minimal POS
//   LEDR9 = ALARM: one of your answers disagrees with Y on this row
//
// GRADE: SOP : CSOP
// GRADE: POS : CPOS
// GRADE: MIN : POS MIN
// ASK Q1 SOP: SOP | Canonical SOP: one minterm for every row where Y = 1, e.g. A'BC + ABC'
// ASK Q2 POS: POS | Canonical POS: one maxterm for every row where Y = 0, e.g. (A + B + C')(A' + B + C)
// ASK Q3 MIN: MIN | Minimal POS: the fewest sums (parentheses) - still a product of sums
// TEXT Q4 1: In exercise 1 the POS was shorter than the SOP; here it is the other way round. What in the table decides which canonical form is shorter?
// TEXT Q5 2: Can the two minterms of the SOP be merged into one shorter term? Explain why or why not.
// TEXT Q6 3: Describe in words, without a formula, when Y = 1.
// TEXT Q7 4: Predict before you move the switches: A=1 B=1 C=0 - which LEDR lights will be on?
// Truth table:  A B C | Y
//               0 0 0 | 1
//               0 0 1 | 0
//               0 1 0 | 0
//               0 1 1 | 0
//               1 0 0 | 0
//               1 0 1 | 0
//               1 1 0 | 0
//               1 1 1 | 1
module ex2_top(
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

	// The truth table as a lookup, written without any SOP or POS
	reg Y;
	always @(*) begin
		case ({A, B, C})
			3'b000: Y = 1'b1;
			3'b001: Y = 1'b0;
			3'b010: Y = 1'b0;
			3'b011: Y = 1'b0;
			3'b100: Y = 1'b0;
			3'b101: Y = 1'b0;
			3'b110: Y = 1'b0;
			3'b111: Y = 1'b1;
		endcase
	end

	wire sop, pos, min;
	student_logic u(.A(A), .B(B), .C(C), .SOP(sop), .POS(pos), .MIN(min));

	assign LEDG    = {7'b0, Y};
	assign LEDR    = {(sop != Y) | (pos != Y) | (min != Y), 6'b0, min, pos, sop};

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
