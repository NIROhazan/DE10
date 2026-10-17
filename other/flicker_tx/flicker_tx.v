// flicker_tx.v - a "lamp" with a known flicker, for the D5M camera's flicker meter (SW6 on the
// camera board).  All 10 red LEDs and all six 7-segment displays blink together, 50 % on / 50 % off,
// at the frequency set on the switches.
//
//   SW9..SW0   frequency in Hz, binary (e.g. 100 Hz = SW6 + SW5 + SW2 up)
//   KEY0       held: steady on (no flicker - the meter should go to 0)
//   KEY1       held: off
//   HEX        as much light as possible: every display fully lit with its dot ("8."), except the
//              digits of the frequency (no leading zeros), which show the number (dots still on).
//              At 50 Hz and up the eye sees it steady (dimmer), the camera sees it blink.
//
// The square wave is the top bit of a 48-bit phase accumulator that adds SW x 2^48 / 50 MHz every
// clock (DDS): exact to ~1e-7 at any frequency, no division needed.
module flicker_tx(
	input        MAX10_CLK1_50,
	input  [1:0] KEY,
	input  [9:0] SW,
	output [9:0] LEDR,
	output [7:0] HEX0, HEX1, HEX2, HEX3, HEX4, HEX5
);
	wire clk = MAX10_CLK1_50;

	reg [9:0] sw1 = 0, sw2 = 0;
	reg [1:0] k1 = 2'b11, k2 = 2'b11;
	always @(posedge clk) begin sw1 <= SW; sw2 <= sw1; k1 <= KEY; k2 <= k1; end

	// phase accumulator: one full turn (2^48) per flicker period
	localparam [47:0] HZ_STEP = 48'd5629500;          // 2^48 / 50e6 = 5629499.53
	reg  [47:0] acc = 0;
	wire [47:0] step = sw2 * HZ_STEP;
	always @(posedge clk) acc <= acc + step;

	wire light = !k2[1] ? 1'b0 :                      // KEY1 held: off
	             !k2[0] ? 1'b1 :                      // KEY0 held: steady
	             acc[47];

	// frequency in decimal (10 bits -> 4 digits, double dabble)
	function [15:0] bcd(input [9:0] b);
		integer i;
		reg [25:0] s;
		begin
			s = {16'b0, b};
			for (i = 0; i < 10; i = i + 1) begin
				if (s[13:10] > 4) s[13:10] = s[13:10] + 3;
				if (s[17:14] > 4) s[17:14] = s[17:14] + 3;
				if (s[21:18] > 4) s[21:18] = s[21:18] + 3;
				if (s[25:22] > 4) s[25:22] = s[25:22] + 3;
				s = s << 1;
			end
			bcd = s[25:10];
		end
	endfunction
	wire [15:0] dec = bcd(sw2);

	wire [7:0] s0, s1, s2, s3;
	hex7 h0(.v(dec[3:0]),   .seg(s0));
	hex7 h1(.v(dec[7:4]),   .seg(s1));
	hex7 h2(.v(dec[11:8]),  .seg(s2));
	hex7 h3(.v(dec[15:12]), .seg(s3));

	// leading zeros and the unused displays: everything on ("8.", all segments active low = 0)
	localparam [7:0] ALL = 8'h00;
	wire lead3 = dec[15:12] == 0;
	wire lead2 = lead3 && dec[11:8] == 0;
	wire lead1 = lead2 && dec[7:4] == 0;
	wire [7:0] g0 = {1'b0, s0[6:0]};                 // digits: their segments plus the dot
	wire [7:0] g1 = lead1 ? ALL : {1'b0, s1[6:0]};
	wire [7:0] g2 = lead2 ? ALL : {1'b0, s2[6:0]};
	wire [7:0] g3 = lead3 ? ALL : {1'b0, s3[6:0]};

	// segments and LEDs are on only while the light is on
	assign HEX0 = light ? g0  : 8'hFF;
	assign HEX1 = light ? g1  : 8'hFF;
	assign HEX2 = light ? g2  : 8'hFF;
	assign HEX3 = light ? g3  : 8'hFF;
	assign HEX4 = light ? ALL : 8'hFF;
	assign HEX5 = light ? ALL : 8'hFF;
	assign LEDR = {10{light}};
endmodule

// one hex digit on a 7-segment display (active low, [6:0] = g f e d c b a, dot off)
module hex7(input [3:0] v, output [7:0] seg);
	reg [6:0] s;
	always @(*)
		case (v)
			4'h0: s = 7'b1000000; 4'h1: s = 7'b1111001; 4'h2: s = 7'b0100100; 4'h3: s = 7'b0110000;
			4'h4: s = 7'b0011001; 4'h5: s = 7'b0010010; 4'h6: s = 7'b0000010; 4'h7: s = 7'b1111000;
			4'h8: s = 7'b0000000; 4'h9: s = 7'b0010000; 4'hA: s = 7'b0001000; 4'hB: s = 7'b0000011;
			4'hC: s = 7'b1000110; 4'hD: s = 7'b0100001; 4'hE: s = 7'b0000110; default: s = 7'b0001110;
		endcase
	assign seg = {1'b1, s};
endmodule
