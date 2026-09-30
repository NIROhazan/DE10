// DE10 starter top level - Terasic DE1 (Cyclone II EP2C20F484C7)
//   SW[9:0]  -> LEDR[9:0]
//   KEY[3:0] -> LEDG[7:4]   (keys are active low)
//   LEDG[0]  blinks at 1 Hz from CLOCK_50
//   HEX3..HEX0 show SW[9:0] in hex (HEX3 blank)
module top(
	input        CLOCK_50,
	input  [3:0] KEY,
	input  [9:0] SW,
	output [7:0] LEDG,
	output [9:0] LEDR,
	output [6:0] HEX0,
	output [6:0] HEX1,
	output [6:0] HEX2,
	output [6:0] HEX3
	);

	// 1 Hz blink: toggle every 25,000,000 cycles of the 50 MHz clock
	reg [24:0] count = 0;
	reg        blink = 0;
	always @(posedge CLOCK_50) begin
		if (count == 25'd24_999_999) begin
			count <= 0;
			blink <= ~blink;
		end else
			count <= count + 1'b1;
	end

	assign LEDR      = SW;
	assign LEDG[7:4] = ~KEY;
	assign LEDG[3:1] = 3'b000;
	assign LEDG[0]   = blink;

	hex7seg h0(.x(SW[3:0]),        .seg(HEX0));
	hex7seg h1(.x(SW[7:4]),        .seg(HEX1));
	hex7seg h2(.x({2'b00, SW[9:8]}), .seg(HEX2));
	assign HEX3 = 7'h7F;	// segments are active low: all off
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
