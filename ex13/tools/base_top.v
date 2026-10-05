// Exercise 13 - reading a multilevel circuit.  DO NOT EDIT: Claude writes student_logic.v from answer.txt.
//
//   SW0 = A, SW1 = B, SW2 = C        HEX3 = A, HEX2 = B, HEX1 = C, HEX0 = Y
//   LEDG0 = Y of the circuit (the target)
//   LEDR0 = your minimal SOP   LEDR1 = your minimal POS
//   LEDR9 = ALARM: one of your answers disagrees with Y on this row
//
// NET: n1 = (AB')'
// NET: n2 = (A' + C)'
// NET: n3 = (n1 n2')'
// NET: Y = (n3 + BC)'
// GRADE: MSOP : SOP MIN
// GRADE: MPOS : POS MIN
// ASK Q1 MSOP: MSOP | Y of the circuit as a minimal SOP: the fewest terms, then the fewest literals
// ASK Q2 MPOS: MPOS | Y of the circuit as a minimal POS: the fewest sums, then the fewest literals
// TEXT Q3 1: What does gate n3 compute? Write it as a simplified expression of A, B and C, and name the theorems you used.
// TEXT Q4 2: Bubble pushing: which gates of the circuit have bubbles that cancel each other? Redraw the last two gates so the bubbles cancel - which gate types do you get?
// TEXT Q5 3: How many levels of gates does the circuit have from the inputs to Y, and how many levels does your minimal SOP need? Why is that allowed?
// TEXT Q6 4: Predict before you move the switches: A=0 B=1 C=1 - what will LEDG0 be, and which LEDR lights will be on?
// Truth table:  A B C | Y
//               0 0 0 | 1
//               0 0 1 | 1
//               0 1 0 | 1
//               0 1 1 | 0
//               1 0 0 | 0
//               1 0 1 | 0
//               1 1 0 | 0
//               1 1 1 | 0
module ex13_top(
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
			3'b000: Y = 1'b1;
			3'b001: Y = 1'b1;
			3'b010: Y = 1'b1;
			3'b011: Y = 1'b0;
			3'b100: Y = 1'b0;
			3'b101: Y = 1'b0;
			3'b110: Y = 1'b0;
			3'b111: Y = 1'b0;
		endcase
	end

	wire s_msop, s_mpos;
	student_logic u(.A(A), .B(B), .C(C), .MSOP(s_msop), .MPOS(s_mpos));

	wire alarm = (s_msop != Y) | (s_mpos != Y);

	assign LEDG    = {7'b0, Y};
	assign LEDR    = {alarm, 7'b0, s_mpos, s_msop};

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
