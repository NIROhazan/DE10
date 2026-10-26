// week 4 ex10 board - Terasic DE1 (Cyclone II EP2C20F484C7). Instructor source: students get only board.sof.
// case / casez: 16 casez blocks, puzzle SW9..6 (HEX1), a = SW3..0 (HEX0), y on LEDG3..0 and HEX3.
module board(
	input        CLOCK_50,
	input  [9:0] SW,
	input  [3:0] KEY,
	output [9:0] LEDR,
	output [7:0] LEDG,
	output [6:0] HEX0,
	output [6:0] HEX1,
	output [6:0] HEX2,
	output [6:0] HEX3
	);

	wire [3:0] a = SW[3:0];
	wire [3:0] p = SW[9:6];
	reg  [3:0] y;
	always @(*) begin
		y = 4'h0;
		case (p)
			4'd0:
				casez (a)
					4'b??1?: y = 4'h7;
					4'b1?1?: y = 4'h1;
					4'b1??1: y = 4'hE;
					4'b?0??: y = 4'hD;
					default: y = 4'h0;
				endcase
			4'd1:
				casez (a)
					4'b?00?: y = 4'h3;
					4'b???0: y = 4'hE;
					4'b0?00: y = 4'h5;
					4'b??1?: y = 4'h7;
					default: y = 4'h0;
				endcase
			4'd2:
				casez (a)
					4'b01??: y = 4'hF;
					4'b11?0: y = 4'h4;
					4'b1???: y = 4'hC;
					4'b??11: y = 4'h7;
					4'b1??1: y = 4'h8;
					default: y = 4'h0;
				endcase
			4'd3:
				casez (a)
					4'b0?0?: y = 4'hC;
					4'b?0?1: y = 4'hF;
					4'b?111: y = 4'h3;
					4'b??11: y = 4'h5;
					4'b??0?: y = 4'hB;
					default: y = 4'h0;
				endcase
			4'd4:
				casez (a)
					4'b111?: y = 4'h5;
					4'b?10?: y = 4'hA;
					4'b???0: y = 4'hB;
					4'b??1?: y = 4'h4;
					4'b00?0: y = 4'h3;
					default: y = 4'h0;
				endcase
			4'd5:
				casez (a)
					4'b0??1: y = 4'h7;
					4'b1?0?: y = 4'hE;
					4'b?1??: y = 4'hF;
					4'b?10?: y = 4'hC;
					4'b?0?1: y = 4'hD;
					default: y = 4'h0;
				endcase
			4'd6:
				casez (a)
					4'b??01: y = 4'h1;
					4'b?00?: y = 4'h3;
					4'b11??: y = 4'hF;
					4'b0?1?: y = 4'hD;
					4'b0?11: y = 4'hA;
					default: y = 4'h0;
				endcase
			4'd7:
				casez (a)
					4'b1???: y = 4'h9;
					4'b10?1: y = 4'h7;
					4'b0?0?: y = 4'hF;
					4'b?1?0: y = 4'hE;
					4'b??11: y = 4'hB;
					default: y = 4'h0;
				endcase
			4'd8:
				casez (a)
					4'b1??1: y = 4'hE;
					4'b??1?: y = 4'hD;
					4'b?100: y = 4'h2;
					4'b1?0?: y = 4'hB;
					4'b10?1: y = 4'h9;
					default: y = 4'h0;
				endcase
			4'd9:
				casez (a)
					4'b0?00: y = 4'h4;
					4'b1??0: y = 4'hB;
					4'b0??1: y = 4'hF;
					4'b?100: y = 4'hC;
					default: y = 4'h0;
				endcase
			4'd10:
				casez (a)
					4'b???0: y = 4'h7;
					4'b?110: y = 4'h9;
					4'b??0?: y = 4'hE;
					4'b?0??: y = 4'hB;
					default: y = 4'h0;
				endcase
			4'd11:
				casez (a)
					4'b001?: y = 4'hB;
					4'b??00: y = 4'hD;
					4'b?11?: y = 4'h6;
					4'b?111: y = 4'hA;
					default: y = 4'h0;
				endcase
			4'd12:
				casez (a)
					4'b??0?: y = 4'hF;
					4'b???1: y = 4'h3;
					4'b??01: y = 4'hA;
					4'b11??: y = 4'hE;
					default: y = 4'h0;
				endcase
			4'd13:
				casez (a)
					4'b?1?0: y = 4'hB;
					4'b1?10: y = 4'h1;
					4'b?1?1: y = 4'hD;
					4'b111?: y = 4'hC;
					4'b00??: y = 4'hE;
					default: y = 4'h0;
				endcase
			4'd14:
				casez (a)
					4'b?000: y = 4'h4;
					4'b001?: y = 4'hC;
					4'b0??1: y = 4'hB;
					4'b?10?: y = 4'h3;
					4'b000?: y = 4'h5;
					default: y = 4'h0;
				endcase
			4'd15:
				casez (a)
					4'b??11: y = 4'hA;
					4'b?11?: y = 4'h9;
					4'b10??: y = 4'h7;
					4'b100?: y = 4'h6;
					4'b???1: y = 4'hF;
					default: y = 4'h0;
				endcase
		endcase
	end

	assign LEDG = {4'b0, y};
	assign LEDR = 10'b0;
	hex7seg h3(.x(y), .seg(HEX3));
	assign HEX2 = 7'b1111111;
	hex7seg h1(.x(p), .seg(HEX1));
	hex7seg h0(.x(a), .seg(HEX0));
endmodule

// Hex digit to 7-segment, active low, seg[6:0] = g f e d c b a
module hex7seg(input [3:0] x, output reg [6:0] seg);
	always @(*) case (x)
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
		4'hF: seg = 7'b0001110;
		default: seg = 7'b1111111;
	endcase
endmodule

// One pulse of one clock every 0.1 s (50 MHz): the "tick" of the slow-motion circuits
module tick10(input clk, output reg t);
	reg [22:0] c = 23'd0;
	always @(posedge clk) begin
		t <= (c == 23'd4999999);
		c <= (c == 23'd4999999) ? 23'd0 : c + 23'd1;
	end
endmodule

// A gate output in slow motion: y follows x d ticks later (d = 1..15), pulses included
module dly(input clk, input t, input x, input [3:0] d, output y);
	reg [14:0] h = 15'd0;
	always @(posedge clk) if (t) h <= {h[13:0], x};
	assign y = h[d - 4'd1];
endmodule

// Stopwatch: ticks since the last input change, at the first and at the last change of y; n = changes of y
module watch(input clk, input t, input changed, input y, output reg [6:0] first, output reg [6:0] last, output reg [3:0] n);
	reg [6:0] c = 7'd0;
	reg yp = 1'b0;
	always @(posedge clk) if (t) begin
		yp <= y;
		if (changed) begin c <= 7'd0; first <= 7'd0; last <= 7'd0; n <= 4'd0; end
		else begin
			if (c != 7'd99) c <= c + 7'd1;
			if (y != yp) begin
				if (n == 4'd0) first <= c;
				last <= c;
				if (n != 4'd15) n <= n + 4'd1;
			end
		end
	end
endmodule

// 0..99 on two digits
module dec2(input [6:0] v, output [6:0] tens, output [6:0] ones);
	hex7seg ht(.x(v / 7'd10), .seg(tens));
	hex7seg ho(.x(v % 7'd10), .seg(ones));
endmodule
