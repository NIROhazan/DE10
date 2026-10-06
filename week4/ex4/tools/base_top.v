// Exercise 4 - a K-map with three variables.  DO NOT EDIT: Claude writes student_logic.v from answer.txt.
//
//   SW0 = A, SW1 = B, SW2 = C        HEX3 = A, HEX2 = B, HEX1 = C, HEX0 = Y
//   LEDG0 = Y from the truth table (the target)
//   LEDR0 = your minimal SOP   LEDR1 = your minimal POS
//   LEDR9 = ALARM: one of your answers disagrees with Y on this row
//
// GRADE: MSOP : SOP MIN
// GRADE: MPOS : POS MIN
// ASK Q1 MSOP: MSOP | Minimal SOP from the K-map of the 1s: the fewest terms, then the fewest literals
// ASK Q2 MPOS: MPOS | Minimal POS from the K-map of the 0s: the fewest sums, then the fewest literals
// TEXT Q3 1: Why are the K-map columns in the order 00 01 11 10 and not 00 01 10 11? Which two columns are neighbours across the edge of the map, and why?
// TEXT Q4 2: Your table has a prime implicant that is NOT in your minimal SOP. Which one is it, and why is it not needed?
// TEXT Q5 3: For each term of your MSOP: which variable did its circle remove, and why (what happens to that variable inside the circle)?
// TEXT Q6 4: Predict before you move the switches: A=1 B=1 C=0 - what will LEDG0 be, and which LEDR lights will be on?
// Truth table:  A B C | Y
//               0 0 0 | 1
//               0 0 1 | 0
//               0 1 0 | 1
//               0 1 1 | 1
//               1 0 0 | 0
//               1 0 1 | 0
//               1 1 0 | 0
//               1 1 1 | 1
module ex4_top(
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

	// The truth table as a lookup, written without any SOP or POS.  dc = 1 on an X row.
	reg Y, dc;
	always @(*) begin
		dc = 1'b0;
		case ({A, B, C})
			3'b000: Y = 1'b1;
			3'b001: Y = 1'b0;
			3'b010: Y = 1'b1;
			3'b011: Y = 1'b1;
			3'b100: Y = 1'b0;
			3'b101: Y = 1'b0;
			3'b110: Y = 1'b0;
			3'b111: Y = 1'b1;
		endcase
	end

	wire msop, mpos;
	student_logic u(.A(A), .B(B), .C(C), .MSOP(msop), .MPOS(mpos));

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
	assign HEX0 = bit7(Y);
endmodule
