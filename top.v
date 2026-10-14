// DE10 starter top level - Terasic DE10-Lite (MAX 10 10M50DAF484C7G)
//   SW[9:0]  -> LEDR[9:0]
//   HEX2..HEX0 show SW[9:0] in hex, HEX3 blank
//   KEY1, KEY0 -> decimal points of HEX5, HEX4 (keys are active low)
//   decimal point of HEX0 blinks at 1 Hz from MAX10_CLK1_50
module top(
	input        MAX10_CLK1_50,
	input  [1:0] KEY,
	input  [9:0] SW,
	output [9:0] LEDR,
	output [7:0] HEX0,
	output [7:0] HEX1,
	output [7:0] HEX2,
	output [7:0] HEX3,
	output [7:0] HEX4,
	output [7:0] HEX5
	);

	// 1 Hz blink: toggle every 25,000,000 cycles of the 50 MHz clock
	reg [24:0] count = 0;
	reg        blink = 0;
	always @(posedge MAX10_CLK1_50) begin
		if (count == 25'd24_999_999) begin
			count <= 0;
			blink <= ~blink;
		end else
			count <= count + 1'b1;
	end

	assign LEDR = SW;

	// Segments and decimal points are active low: 1 = off
	hex7seg h0(.x(SW[3:0]),          .seg(HEX0[6:0]));
	hex7seg h1(.x(SW[7:4]),          .seg(HEX1[6:0]));
	hex7seg h2(.x({2'b00, SW[9:8]}), .seg(HEX2[6:0]));
	assign HEX0[7] = ~blink;
	assign HEX1[7] = 1'b1;
	assign HEX2[7] = 1'b1;
	assign HEX3    = 8'hFF;
	assign HEX4    = {KEY[0], 7'h7F};
	assign HEX5    = {KEY[1], 7'h7F};
endmodule

// Hex digit to 7-segment, active low, seg[6:0] = g f e d c b a
module hex7seg(
	input      [3:0] x,
	output reg [6:0] seg
	);
	always @(*) begin
		case (x)
			4'h0: seg = 7'b1000000;
			4'h1: seg = 7'b1111001;
			4'h2: seg = 7'b0100100;
			4'h3: seg = 7'b0110000;
			4'h4: seg = 7'b0011001;
			4'h5: seg = 7'b0010010;
			4'h6: seg = 7'b0000010;
			4'h7: seg = 7'b1111000;
			4'h8: seg = 7'b0000000;
			4'h9: seg = 7'b0010000;
			4'hA: seg = 7'b0001000;
			4'hB: seg = 7'b0000011;
			4'hC: seg = 7'b1000110;
			4'hD: seg = 7'b0100001;
			4'hE: seg = 7'b0000110;
			default: seg = 7'b0001110;	// F
		endcase
	end
endmodule
