// Exercise 6 - don't-care rows (X).  DO NOT EDIT: Claude writes student_logic.v from answer.txt.
//
//   SW0 = A, SW1 = B, SW2 = C        HEX3 = A, HEX2 = B, HEX1 = C, HEX0 = Y ("-" on an X row)
//   Green LEDs are not used: Y is on HEX0
//   LEDR0 = your SOP        LEDR1 = your POS        LEDR2 = your minimal SOP   LEDR3 = your minimal POS
//   LEDR9 = ALARM: one of your answers disagrees with Y on this row (never lights on an X row)
//
// Truth table:  A B C | Y
//               0 0 0 | 0
//               0 0 1 | 0
//               0 1 0 | 0
//               0 1 1 | 1
//               1 0 0 | X
//               1 0 1 | 1
//               1 1 0 | X
//               1 1 1 | 1
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

	// The truth table as a lookup, written without any SOP or POS.  dc = 1 on an X row.
	reg Y, dc;
	always @(*) begin
		dc = 1'b0;
		case ({A, B, C})
			3'b000: Y = 1'b0;
			3'b001: Y = 1'b0;
			3'b010: Y = 1'b0;
			3'b011: Y = 1'b1;
			3'b100: begin Y = 1'b0; dc = 1'b1; end
			3'b101: Y = 1'b1;
			3'b110: begin Y = 1'b0; dc = 1'b1; end
			3'b111: Y = 1'b1;
		endcase
	end

	wire sop, pos, msop, mpos;
	student_logic u(.A(A), .B(B), .C(C), .SOP(sop), .POS(pos), .MSOP(msop), .MPOS(mpos));

	// An X row may take any value, so it can never raise the alarm
	wire alarm = ~dc & ((sop != Y) | (pos != Y) | (msop != Y) | (mpos != Y));

	assign LEDG    = 8'b0;
	assign LEDR    = {alarm, 5'b0, mpos, msop, pos, sop};

	// 7-segment, active low: "0" and "1" only
	function [6:0] bit7;
		input b;
		bit7 = b ? 7'b1111001 : 7'b1000000;
	endfunction

	assign HEX3 = bit7(A);
	assign HEX2 = bit7(B);
	assign HEX1 = bit7(C);
	assign HEX0 = dc ? 7'b0111111 : bit7(Y);	// "-" = don't care
endmodule
