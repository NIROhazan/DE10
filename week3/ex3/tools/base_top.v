// Exercise 3 - minimal SOP and minimal POS.  DO NOT EDIT: Claude writes student_logic.v from answer.txt.
//
//   SW0 = A, SW1 = B, SW2 = C        HEX3 = A, HEX2 = B, HEX1 = C, HEX0 = Y from the table
//   LEDG0 = Y from the truth table   (the target)
//   LEDR0 = your SOP        LEDR1 = your POS        LEDR2 = your minimal SOP   LEDR3 = your minimal POS
//   LEDR9 = ALARM: one of your answers disagrees with Y on this row
//
// GRADE: SOP : CSOP
// GRADE: POS : CPOS
// GRADE: MSOP : SOP MIN
// GRADE: MPOS : POS MIN
// ASK Q1 SOP: SOP | Canonical SOP: one minterm for every row where Y = 1, e.g. A'BC + ABC'
// ASK Q2 POS: POS | Canonical POS: one maxterm for every row where Y = 0, e.g. (A + B + C')(A' + B + C)
// ASK Q3 MSOP: MSOP | Minimal SOP: the fewest terms, then the fewest literals
// ASK Q4 MPOS: MPOS | Minimal POS: the fewest sums, then the fewest literals
// TEXT Q5 1: Y has more than one minimal SOP. Find a second minimal SOP, different from yours, and explain why both are correct.
// TEXT Q6 2: Count the literals of your MSOP and of your MPOS. Which is smaller, and what in the table hinted at it?
// TEXT Q7 3: Is the row A=0 B=0 C=0 covered by more than one term of your MSOP? Why may terms overlap?
// TEXT Q8 4: Predict before you move the switches: A=1 B=1 C=0 - which LEDR lights will be on?
// Truth table:  A B C | Y
//               0 0 0 | 1
//               0 0 1 | 0
//               0 1 0 | 1
//               0 1 1 | 0
//               1 0 0 | 1
//               1 0 1 | 1
//               1 1 0 | 0
//               1 1 1 | 1
module ex3_top(
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
			3'b010: Y = 1'b1;
			3'b011: Y = 1'b0;
			3'b100: Y = 1'b1;
			3'b101: Y = 1'b1;
			3'b110: Y = 1'b0;
			3'b111: Y = 1'b1;
		endcase
	end

	wire sop, pos, msop, mpos;
	student_logic u(.A(A), .B(B), .C(C), .SOP(sop), .POS(pos), .MSOP(msop), .MPOS(mpos));

	wire alarm = (sop != Y) | (pos != Y) | (msop != Y) | (mpos != Y);

	assign LEDG    = {7'b0, Y};
	assign LEDR    = {alarm, 5'b0, mpos, msop, pos, sop};

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
