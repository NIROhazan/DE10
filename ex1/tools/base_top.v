// Exercise 1 - SOP / POS.  DO NOT EDIT: Claude writes student_logic.v from answer.txt.
//
//   SW0 = A, SW1 = B                 HEX3 = A, HEX2 = B, HEX0 = Y from the table
//   LEDG0 = Y from the truth table   (the target)
//   LEDR0 = your SOP                 LEDR1 = your POS        LEDR2 = your MIN
//   LEDR9 = ALARM: one of your answers disagrees with Y on this row
//
// Truth table:  A B | Y
//               0 0 | 1
//               0 1 | 0
//               1 0 | 1
//               1 1 | 1
module ex1_top(
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

	// The truth table as a lookup, written without any SOP or POS
	reg Y;
	always @(*) begin
		case ({A, B})
			2'b00: Y = 1'b1;
			2'b01: Y = 1'b0;
			2'b10: Y = 1'b1;
			2'b11: Y = 1'b1;
		endcase
	end

	wire sop, pos, min;
	student_logic u(.A(A), .B(B), .SOP(sop), .POS(pos), .MIN(min));

	assign LEDG    = {7'b0, Y};
	assign LEDR    = {(sop != Y) | (pos != Y) | (min != Y), 6'b0, min, pos, sop};

	// 7-segment, active low: "0" and "1" only
	function [6:0] bit7;
		input b;
		bit7 = b ? 7'b1111001 : 7'b1000000;
	endfunction

	assign HEX3 = bit7(A);
	assign HEX2 = bit7(B);
	assign HEX1 = 7'h7F;
	assign HEX0 = bit7(Y);
endmodule
