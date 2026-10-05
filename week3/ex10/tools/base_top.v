// Exercise 10 - a 4:1 mux and a 3:8 decoder.  DO NOT EDIT: Claude writes student_logic.v from answer.txt.
//
//   SW0 = A, SW1 = B, SW2 = C        HEX3 = A, HEX2 = B, HEX1 = C, HEX0 = Y
//   LEDG0 = Y from the truth table (the target)
//   LEDR0 = your mux (selects A B, data D0-D3)   LEDR1 = your decoder + OR   LEDR5-LEDR2 = D3-D0
//   LEDR9 = ALARM: your mux or your decoder disagrees with Y on this row
//
// SIGNAL: y0 = ~A & ~B & ~C
// SIGNAL: y1 = ~A & ~B & C
// SIGNAL: y2 = ~A & B & ~C
// SIGNAL: y3 = ~A & B & C
// SIGNAL: y4 = A & ~B & ~C
// SIGNAL: y5 = A & ~B & C
// SIGNAL: y6 = A & B & ~C
// SIGNAL: y7 = A & B & C
// CHECK: MUX = (~A & ~B & D0) | (~A & B & D1) | (A & ~B & D2) | (A & B & D3)
// ONLY: D0 D1 D2 D3 : TOKENS C ~ 1'b0 1'b1
// ONLY: DEC : TOKENS y0 y1 y2 y3 y4 y5 y6 y7 |
// ASK Q1 MUX: D0 D1 D2 D3 | A 4:1 mux, selects A (high bit) and B: AB=00 -> D0 ... 11 -> D3. Each D is 0, 1, C or C'
// ASK Q2 DEC: DEC | A 3:8 decoder (yi = 1 only on row i) and an OR: which outputs go into the OR? e.g. y0 + y3 + y5
// TEXT Q3 1: How did you find D0? Explain which two rows of the table you looked at, and why they decide it.
// TEXT Q4 2: In how many rows of the table is Y = 1, and how many decoder outputs go into the OR? Why is it always the same number? How is it related to the canonical SOP?
// TEXT Q5 3: How many select inputs does a mux with N data inputs have? And how would you build Y with an 8:1 mux instead of a 4:1?
// TEXT Q6 4: Predict before you move the switches: A=1 B=0 C=1 - which mux input is selected, and what will LEDR0 and LEDR1 show?
// Truth table:  A B C | Y
//               0 0 0 | 0
//               0 0 1 | 1
//               0 1 0 | 1
//               0 1 1 | 0
//               1 0 0 | 1
//               1 0 1 | 0
//               1 1 0 | 1
//               1 1 1 | 1
module ex10_top(
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
			3'b011: Y = 1'b0;
			3'b100: Y = 1'b1;
			3'b101: Y = 1'b0;
			3'b110: Y = 1'b1;
			3'b111: Y = 1'b1;
		endcase
	end

	// A 3:8 decoder: y[i] is 1 only on row i (the minterms)
	wire [7:0] y;
	assign y[0] = ~A & ~B & ~C;
	assign y[1] = ~A & ~B &  C;
	assign y[2] = ~A &  B & ~C;
	assign y[3] = ~A &  B &  C;
	assign y[4] =  A & ~B & ~C;
	assign y[5] =  A & ~B &  C;
	assign y[6] =  A &  B & ~C;
	assign y[7] =  A &  B &  C;

	wire d0, d1, d2, d3, dec;
	student_logic u(.A(A), .B(B), .C(C), .y0(y[0]), .y1(y[1]), .y2(y[2]), .y3(y[3]),
		.y4(y[4]), .y5(y[5]), .y6(y[6]), .y7(y[7]), .D0(d0), .D1(d1), .D2(d2), .D3(d3), .DEC(dec));

	// A 4:1 mux: A and B select which data input reaches the output
	wire mux = A ? (B ? d3 : d2) : (B ? d1 : d0);

	wire alarm = (mux != Y) | (dec != Y);

	assign LEDG    = {7'b0, Y};
	assign LEDR    = {alarm, 3'b0, d3, d2, d1, d0, dec, mux};

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
