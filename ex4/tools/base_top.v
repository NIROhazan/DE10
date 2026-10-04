// Exercise 4 - four variables.  DO NOT EDIT: Claude writes student_logic.v from answer.txt.
//
//   SW0 = A, SW1 = B, SW2 = C, KEY3 = D (hold KEY3 pressed for D = 1)
//   HEX3 = A, HEX2 = B, HEX1 = C, HEX0 = D      LEDG0 = Y from the truth table (the target)
//   LEDR0 = your SOP   LEDR1 = your POS   LEDR2 = your minimal SOP   LEDR3 = your XOR form
//   LEDR9 = ALARM: one of your answers disagrees with Y on this row
//
// Truth table:  A B C D | Y        A B C D | Y
//               0 0 0 0 | 1        1 0 0 0 | 0
//               0 0 0 1 | 0        1 0 0 1 | 1
//               0 0 1 0 | 0        1 0 1 0 | 1
//               0 0 1 1 | 1        1 0 1 1 | 0
//               0 1 0 0 | 0        1 1 0 0 | 1
//               0 1 0 1 | 1        1 1 0 1 | 0
//               0 1 1 0 | 1        1 1 1 0 | 0
//               0 1 1 1 | 0        1 1 1 1 | 1
module ex4_top(
	input  [9:0] SW,
	input  [3:0] KEY,
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
	wire D = ~KEY[3];	// keys are active low: pressed = 0, so invert

	// The truth table as a lookup, written without any SOP or POS
	reg Y;
	always @(*) begin
		case ({A, B, C, D})
			4'b0000: Y = 1'b1;
			4'b0001: Y = 1'b0;
			4'b0010: Y = 1'b0;
			4'b0011: Y = 1'b1;
			4'b0100: Y = 1'b0;
			4'b0101: Y = 1'b1;
			4'b0110: Y = 1'b1;
			4'b0111: Y = 1'b0;
			4'b1000: Y = 1'b0;
			4'b1001: Y = 1'b1;
			4'b1010: Y = 1'b1;
			4'b1011: Y = 1'b0;
			4'b1100: Y = 1'b1;
			4'b1101: Y = 1'b0;
			4'b1110: Y = 1'b0;
			4'b1111: Y = 1'b1;
		endcase
	end

	wire sop, pos, msop, xorf;
	student_logic u(.A(A), .B(B), .C(C), .D(D), .SOP(sop), .POS(pos), .MSOP(msop), .XOR(xorf));

	wire alarm = (sop != Y) | (pos != Y) | (msop != Y) | (xorf != Y);

	assign LEDG    = {7'b0, Y};
	assign LEDR    = {alarm, 5'b0, xorf, msop, pos, sop};

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
