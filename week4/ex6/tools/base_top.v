// Exercise 6 - a K-map with four variables: groups of 8 and of 4.  DO NOT EDIT: Claude writes student_logic.v from answer.txt.
//
//   SW0 = A, SW1 = B, SW2 = C, SW3 = D        HEX3 = A, HEX2 = B, HEX1 = C, HEX0 = D
//   LEDG0 = Y from the truth table (the target)
//   LEDR0 = your minimal SOP   LEDR1 = your minimal POS
//   LEDR9 = ALARM: one of your answers disagrees with Y on this row
//
// GRADE: MSOP : SOP MIN
// GRADE: MPOS : POS MIN
// ASK Q1 MSOP: MSOP | Minimal SOP from the K-map of the 1s: the fewest terms, then the fewest literals
// ASK Q2 MPOS: MPOS | Minimal POS from the K-map of the 0s: the fewest sums, then the fewest literals
// TEXT Q3 1: Your MSOP has a term with a single literal. How many squares does its circle hold, and why must a circle hold 1, 2, 4 or 8 squares - never 6?
// TEXT Q4 2: Compare your MSOP and MPOS: which has fewer terms, which has fewer literals? Which one would you build, and why?
// TEXT Q5 3: 'Each circle must be as large as possible.' Take one term of your MSOP and give a smaller circle someone might draw instead. What does it cost?
// TEXT Q6 4: Predict before you move the switches: A=1 B=1 C=0 D=1 - what will LEDG0 be, and which LEDR lights will be on?
// Truth table:  A B C D | Y          A B C D | Y
//               0 0 0 0 | 1          1 0 0 0 | 1
//               0 0 0 1 | 1          1 0 0 1 | 1
//               0 0 1 0 | 1          1 0 1 0 | 1
//               0 0 1 1 | 1          1 0 1 1 | 1
//               0 1 0 0 | 0          1 1 0 0 | 0
//               0 1 0 1 | 1          1 1 0 1 | 0
//               0 1 1 0 | 1          1 1 1 0 | 1
//               0 1 1 1 | 1          1 1 1 1 | 0
module ex6_top(
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
	wire D = SW[3];

	// The truth table as a lookup, written without any SOP or POS.  dc = 1 on an X row.
	reg Y, dc;
	always @(*) begin
		dc = 1'b0;
		case ({A, B, C, D})
			4'b0000: Y = 1'b1;
			4'b0001: Y = 1'b1;
			4'b0010: Y = 1'b1;
			4'b0011: Y = 1'b1;
			4'b0100: Y = 1'b0;
			4'b0101: Y = 1'b1;
			4'b0110: Y = 1'b1;
			4'b0111: Y = 1'b1;
			4'b1000: Y = 1'b1;
			4'b1001: Y = 1'b1;
			4'b1010: Y = 1'b1;
			4'b1011: Y = 1'b1;
			4'b1100: Y = 1'b0;
			4'b1101: Y = 1'b0;
			4'b1110: Y = 1'b1;
			4'b1111: Y = 1'b0;
		endcase
	end

	wire msop, mpos;
	student_logic u(.A(A), .B(B), .C(C), .D(D), .MSOP(msop), .MPOS(mpos));

	// An X row may take any value, so it can never raise the alarm
	wire alarm = ~dc & ((msop != Y) | (mpos != Y));

	assign LEDG    = {7'b0, Y};
	assign LEDR    = {alarm, 7'b0, mpos, msop};

	// 7-segment, active low: "0" and "1" only
	function [6:0] bit7;
		input b;
		bit7 = b ? 7'b1111001 : 7'b1000000;
	endfunction

	assign HEX3 = bit7(A);
	assign HEX2 = bit7(B);
	assign HEX1 = bit7(C);
	assign HEX0 = bit7(D);
endmodule
