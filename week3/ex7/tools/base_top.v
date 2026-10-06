// Exercise 7 - a priority circuit: four requests, four outputs.  DO NOT EDIT: Claude writes student_logic.v from answer.txt.
//
//   SW0 = A, SW1 = B, SW2 = C, SW3 = D        HEX3 = A, HEX2 = B, HEX1 = C, HEX0 = D
//   LEDG3 LEDG2 LEDG1 LEDG0 = Y3 Y2 Y1 Y0 from the table (the target)
//   LEDR3 LEDR2 LEDR1 LEDR0 = your Y3 Y2 Y1 Y0
//   LEDR9 = ALARM: one of your outputs disagrees with the table on this row
//
// VARIANTS: perms=ABCD masks=all   (the priority order stays; some inputs are active low)
// TARGETS: Y3 Y2 Y1 Y0
// GRADE: Y3 Y2 Y1 Y0 : SOP MIN
// ASK Q1 Y3: Y3 | Y3 - the output of the highest request (A) - as a minimal SOP
// ASK Q2 Y2: Y2 | Y2 (request B) as a minimal SOP
// ASK Q3 Y1: Y1 | Y1 (request C) as a minimal SOP
// ASK Q4 Y0: Y0 | Y0 - the output of the lowest request (D) - as a minimal SOP
// TEXT Q5 1: On the row A=0 B=1 C=1 D=0, which output is 1? Why that one, and not another request that is also on?
// TEXT Q6 2: Some of your inputs are active low (pressed = 0). Which ones, and how did the table show you?
// TEXT Q7 3: Why is Y3 so short and Y0 so long? What does each output have to check?
// TEXT Q8 4: In the lecture this table was written with X (don't care). Where would the X go, and why do they not change your equations?
// Truth table:  A B C D | Y3 Y2 Y1 Y0
//               0 0 0 0 | 0 0 0 0
//               0 0 0 1 | 0 0 0 1
//               0 0 1 0 | 0 0 1 0
//               0 0 1 1 | 0 0 1 0
//               0 1 0 0 | 0 1 0 0
//               0 1 0 1 | 0 1 0 0
//               0 1 1 0 | 0 1 0 0
//               0 1 1 1 | 0 1 0 0
//               1 0 0 0 | 1 0 0 0
//               1 0 0 1 | 1 0 0 0
//               1 0 1 0 | 1 0 0 0
//               1 0 1 1 | 1 0 0 0
//               1 1 0 0 | 1 0 0 0
//               1 1 0 1 | 1 0 0 0
//               1 1 1 0 | 1 0 0 0
//               1 1 1 1 | 1 0 0 0
module ex7_top(
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

	// The target as a lookup: Y = {Y3, Y2, Y1, Y0}
	reg [3:0] Y;
	always @(*) begin
		case ({A, B, C, D})
			4'b0000: Y = 4'b0000;
			4'b0001: Y = 4'b0001;
			4'b0010: Y = 4'b0010;
			4'b0011: Y = 4'b0010;
			4'b0100: Y = 4'b0100;
			4'b0101: Y = 4'b0100;
			4'b0110: Y = 4'b0100;
			4'b0111: Y = 4'b0100;
			4'b1000: Y = 4'b1000;
			4'b1001: Y = 4'b1000;
			4'b1010: Y = 4'b1000;
			4'b1011: Y = 4'b1000;
			4'b1100: Y = 4'b1000;
			4'b1101: Y = 4'b1000;
			4'b1110: Y = 4'b1000;
			4'b1111: Y = 4'b1000;
		endcase
	end

	wire s3, s2, s1, s0;
	student_logic u(.A(A), .B(B), .C(C), .D(D), .Y3(s3), .Y2(s2), .Y1(s1), .Y0(s0));

	wire alarm = (s3 != Y[3]) | (s2 != Y[2]) | (s1 != Y[1]) | (s0 != Y[0]);

	assign LEDG    = {4'b0, Y};
	assign LEDR    = {alarm, 5'b0, s3, s2, s1, s0};

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
