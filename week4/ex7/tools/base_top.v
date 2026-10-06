// Exercise 7 - a seven-segment display: a BCD digit, with don't-cares.  DO NOT EDIT: Claude writes student_logic.v from answer.txt.
//
//   SW3 = A, SW2 = B, SW1 = C, SW0 = D  (the switches read as the binary number ABCD)
//   HEX0 = the digit ABCD on the display ("-" on an X row, 1010-1111)
//   LEDG0 = Y, your segment from the table (the target; off on an X row)
//   LEDR0 = your minimal SOP   LEDR1 = your minimal POS
//   LEDR9 = ALARM: one of your answers disagrees with Y on this row (never lights on an X row)
//
// VARIANTS: perms=ABCD masks=-   (the segment is personal: tools/stories.txt)
// GRADE: MSOP : SOP MIN
// GRADE: MPOS : POS MIN
// ASK Q1 MSOP: MSOP | Minimal SOP of your segment: the fewest terms, then the fewest literals - use the X rows where they help
// ASK Q2 MPOS: MPOS | Minimal POS of your segment: the fewest sums, then the fewest literals - use the X rows where they help
// TEXT Q3 1: Why are the rows 1010 to 1111 X (don't care) in this exercise? Could they ever reach the display?
// TEXT Q4 2: Which X rows did your MSOP take as 1? Without the X rows (all of them 0), how many terms and literals would the minimal SOP need?
// TEXT Q5 3: In the lecture's sevenseg module the case ends with 'default: segments = 7'b000_0000'. Does that let the tool use rows 10-15 as don't-cares? What would?
// TEXT Q6 4: Predict before you move the switches: A=1 B=1 C=0 D=0 - what will HEX0 show, and what will LEDR0 and LEDR1 show with YOUR expressions?
// Truth table:  A B C D | Y          A B C D | Y
//               0 0 0 0 | 1          1 0 0 0 | 1
//               0 0 0 1 | 0          1 0 0 1 | 1
//               0 0 1 0 | 1          1 0 1 0 | X
//               0 0 1 1 | 1          1 0 1 1 | X
//               0 1 0 0 | 0          1 1 0 0 | X
//               0 1 0 1 | 1          1 1 0 1 | X
//               0 1 1 0 | 1          1 1 1 0 | X
//               0 1 1 1 | 1          1 1 1 1 | X
module ex7_top(
	input  [9:0] SW,
	output [7:0] LEDG,
	output [9:0] LEDR,
	output [6:0] HEX0,
	output [6:0] HEX1,
	output [6:0] HEX2,
	output [6:0] HEX3
	);

	wire A = SW[3];
	wire B = SW[2];
	wire C = SW[1];
	wire D = SW[0];

	// The truth table as a lookup, written without any SOP or POS.  dc = 1 on an X row.
	reg Y, dc;
	always @(*) begin
		dc = 1'b0;
		case ({A, B, C, D})
			4'b0000: Y = 1'b1;
			4'b0001: Y = 1'b0;
			4'b0010: Y = 1'b1;
			4'b0011: Y = 1'b1;
			4'b0100: Y = 1'b0;
			4'b0101: Y = 1'b1;
			4'b0110: Y = 1'b1;
			4'b0111: Y = 1'b1;
			4'b1000: Y = 1'b1;
			4'b1001: Y = 1'b1;
			4'b1010: begin Y = 1'b0; dc = 1'b1; end
			4'b1011: begin Y = 1'b0; dc = 1'b1; end
			4'b1100: begin Y = 1'b0; dc = 1'b1; end
			4'b1101: begin Y = 1'b0; dc = 1'b1; end
			4'b1110: begin Y = 1'b0; dc = 1'b1; end
			4'b1111: begin Y = 1'b0; dc = 1'b1; end
		endcase
	end

	wire msop, mpos;
	student_logic u(.A(A), .B(B), .C(C), .D(D), .MSOP(msop), .MPOS(mpos));

	// An X row may take any value, so it can never raise the alarm
	wire alarm = ~dc & ((msop != Y) | (mpos != Y));

	assign LEDG    = {7'b0, Y};
	assign LEDR    = {alarm, 7'b0, mpos, msop};

	// The digit on HEX0 (active low, gfedcba); "-" on the X rows. HEX3..HEX1 are off.
	reg [6:0] digit;
	always @(*) begin
		case ({A, B, C, D})
			4'd0: digit = 7'b1000000;
			4'd1: digit = 7'b1111001;
			4'd2: digit = 7'b0100100;
			4'd3: digit = 7'b0110000;
			4'd4: digit = 7'b0011001;
			4'd5: digit = 7'b0010010;
			4'd6: digit = 7'b0000010;
			4'd7: digit = 7'b1111000;
			4'd8: digit = 7'b0000000;
			4'd9: digit = 7'b0011000;	// 9 as in the lecture: no bottom segment (d)
			default: digit = 7'b0111111;
		endcase
	end

	assign HEX3 = 7'b1111111;
	assign HEX2 = 7'b1111111;
	assign HEX1 = 7'b1111111;
	assign HEX0 = digit;
endmodule
