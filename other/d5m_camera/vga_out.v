// vga_out.v - 640 x 480 @ 60 Hz VGA (25 MHz pixel clock), shows the 320 x 240
// frame buffer with every pixel doubled, or a colour-bar test pattern.
//
// The frame buffer is RGB565 but the DE10-Lite's VGA has 4 bits per colour.  Temporal dithering
// shows the extra bits: a value between two 4-bit levels is shown as the higher level in some
// screen frames and the lower one in the others, and the eye averages them (like the FRC of
// cheap LCD panels).  Red / blue (1 extra bit): higher level every 2nd frame.  Green (2 extra
// bits, e = 0..3): higher level in e of every 4 frames.  Neighbouring pixels take turns, so the
// screen as a whole does not flicker.
//
//   line  = 640 visible + 16 front porch + 96 sync + 48 back porch = 800 clocks
//   frame = 480 visible + 10 front porch +  2 sync + 33 back porch = 525 lines
module vga_out(
	input             clk,          // 25 MHz
	input             pattern,      // 1 = colour bars instead of the camera
	input             events,       // 1 = frame buffer holds event-camera words {ref 8, polarity, age 3}
	input             flick,        // 1 = flicker mode: frequency text and stripe graph on top
	input      [19:0] f_bcd,        // frequency x 10, 5 decimal digits
	input      [2:0]  exp_i,        // flicker exposure setting (two small lines under the frequency)
	input             pw_clk,       // graph points, from flicker.v (camera clock)
	input             pw_we,
	input      [8:0]  pw_addr,
	input      [7:0]  pw_val,
	output     [16:0] raddr,
	input      [15:0] rdata,        // arrives one clock after raddr
	output reg [3:0]  vga_r,
	output reg [3:0]  vga_g,
	output reg [3:0]  vga_b,
	output reg        vga_hs,
	output reg        vga_vs
);

	reg [9:0] h = 0, v = 0;
	always @(posedge clk)
		if (h == 10'd799) begin
			h <= 0;
			v <= (v == 10'd524) ? 10'd0 : v + 1'b1;
		end else
			h <= h + 1'b1;

	wire vis = (h < 10'd640) && (v < 10'd480);
	wire hs  = !((h >= 10'd656) && (h < 10'd752));   // active low
	wire vs  = !((v >= 10'd490) && (v < 10'd492));

	// frame buffer pixel (h/2, v/2):  address = (v/2)*320 + h/2
	wire [7:0] y = v[8:1];
	assign raddr = {y, 8'b0} + {y, 6'b0} + h[9:1];

	// colour bars: 8 bars of 80 pixels, white frame around the edge
	wire [2:0]  bar    = (h < 80) ? 3'd7 : (h < 160) ? 3'd6 : (h < 240) ? 3'd5 : (h < 320) ? 3'd4 :
	                     (h < 400) ? 3'd3 : (h < 480) ? 3'd2 : (h < 560) ? 3'd1 : 3'd0;
	wire        edge_px = (h == 0) || (h == 639) || (v == 0) || (v == 479);
	wire [11:0] bars   = edge_px ? 12'hFFF : {{4{bar[2]}}, {4{bar[1]}}, {4{bar[0]}}};

	// ---- flicker overlay ----
	// 5 x 7 font: 0-9, 10 '.', 11 'H', 12 'z', 13 'e', 14 'x', 15 'p', 16 'm', 17 's', 18 'n', 19 'u',
	// 20 'l', anything else blank; row 7 is blank
	function [4:0] font(input [4:0] ch, input [2:0] row);
		case ({ch, row})
			{5'd0, 3'd0}: font = 5'b01110;   // 0
			{5'd0, 3'd1}: font = 5'b10001;
			{5'd0, 3'd2}: font = 5'b10011;
			{5'd0, 3'd3}: font = 5'b10101;
			{5'd0, 3'd4}: font = 5'b11001;
			{5'd0, 3'd5}: font = 5'b10001;
			{5'd0, 3'd6}: font = 5'b01110;
			{5'd1, 3'd0}: font = 5'b00100;   // 1
			{5'd1, 3'd1}: font = 5'b01100;
			{5'd1, 3'd2}: font = 5'b00100;
			{5'd1, 3'd3}: font = 5'b00100;
			{5'd1, 3'd4}: font = 5'b00100;
			{5'd1, 3'd5}: font = 5'b00100;
			{5'd1, 3'd6}: font = 5'b01110;
			{5'd2, 3'd0}: font = 5'b01110;   // 2
			{5'd2, 3'd1}: font = 5'b10001;
			{5'd2, 3'd2}: font = 5'b00001;
			{5'd2, 3'd3}: font = 5'b00010;
			{5'd2, 3'd4}: font = 5'b00100;
			{5'd2, 3'd5}: font = 5'b01000;
			{5'd2, 3'd6}: font = 5'b11111;
			{5'd3, 3'd0}: font = 5'b11111;   // 3
			{5'd3, 3'd1}: font = 5'b00010;
			{5'd3, 3'd2}: font = 5'b00100;
			{5'd3, 3'd3}: font = 5'b00010;
			{5'd3, 3'd4}: font = 5'b00001;
			{5'd3, 3'd5}: font = 5'b10001;
			{5'd3, 3'd6}: font = 5'b01110;
			{5'd4, 3'd0}: font = 5'b00010;   // 4
			{5'd4, 3'd1}: font = 5'b00110;
			{5'd4, 3'd2}: font = 5'b01010;
			{5'd4, 3'd3}: font = 5'b10010;
			{5'd4, 3'd4}: font = 5'b11111;
			{5'd4, 3'd5}: font = 5'b00010;
			{5'd4, 3'd6}: font = 5'b00010;
			{5'd5, 3'd0}: font = 5'b11111;   // 5
			{5'd5, 3'd1}: font = 5'b10000;
			{5'd5, 3'd2}: font = 5'b11110;
			{5'd5, 3'd3}: font = 5'b00001;
			{5'd5, 3'd4}: font = 5'b00001;
			{5'd5, 3'd5}: font = 5'b10001;
			{5'd5, 3'd6}: font = 5'b01110;
			{5'd6, 3'd0}: font = 5'b00110;   // 6
			{5'd6, 3'd1}: font = 5'b01000;
			{5'd6, 3'd2}: font = 5'b10000;
			{5'd6, 3'd3}: font = 5'b11110;
			{5'd6, 3'd4}: font = 5'b10001;
			{5'd6, 3'd5}: font = 5'b10001;
			{5'd6, 3'd6}: font = 5'b01110;
			{5'd7, 3'd0}: font = 5'b11111;   // 7
			{5'd7, 3'd1}: font = 5'b00001;
			{5'd7, 3'd2}: font = 5'b00010;
			{5'd7, 3'd3}: font = 5'b00100;
			{5'd7, 3'd4}: font = 5'b01000;
			{5'd7, 3'd5}: font = 5'b01000;
			{5'd7, 3'd6}: font = 5'b01000;
			{5'd8, 3'd0}: font = 5'b01110;   // 8
			{5'd8, 3'd1}: font = 5'b10001;
			{5'd8, 3'd2}: font = 5'b10001;
			{5'd8, 3'd3}: font = 5'b01110;
			{5'd8, 3'd4}: font = 5'b10001;
			{5'd8, 3'd5}: font = 5'b10001;
			{5'd8, 3'd6}: font = 5'b01110;
			{5'd9, 3'd0}: font = 5'b01110;   // 9
			{5'd9, 3'd1}: font = 5'b10001;
			{5'd9, 3'd2}: font = 5'b10001;
			{5'd9, 3'd3}: font = 5'b01111;
			{5'd9, 3'd4}: font = 5'b00001;
			{5'd9, 3'd5}: font = 5'b00010;
			{5'd9, 3'd6}: font = 5'b01100;
			{5'd10, 3'd0}: font = 5'b00000;   // .
			{5'd10, 3'd1}: font = 5'b00000;
			{5'd10, 3'd2}: font = 5'b00000;
			{5'd10, 3'd3}: font = 5'b00000;
			{5'd10, 3'd4}: font = 5'b00000;
			{5'd10, 3'd5}: font = 5'b01100;
			{5'd10, 3'd6}: font = 5'b01100;
			{5'd11, 3'd0}: font = 5'b10001;   // H
			{5'd11, 3'd1}: font = 5'b10001;
			{5'd11, 3'd2}: font = 5'b10001;
			{5'd11, 3'd3}: font = 5'b11111;
			{5'd11, 3'd4}: font = 5'b10001;
			{5'd11, 3'd5}: font = 5'b10001;
			{5'd11, 3'd6}: font = 5'b10001;
			{5'd12, 3'd0}: font = 5'b00000;   // z
			{5'd12, 3'd1}: font = 5'b00000;
			{5'd12, 3'd2}: font = 5'b11111;
			{5'd12, 3'd3}: font = 5'b00010;
			{5'd12, 3'd4}: font = 5'b00100;
			{5'd12, 3'd5}: font = 5'b01000;
			{5'd12, 3'd6}: font = 5'b11111;
			{5'd13, 3'd0}: font = 5'b00000;   // e
			{5'd13, 3'd1}: font = 5'b00000;
			{5'd13, 3'd2}: font = 5'b01110;
			{5'd13, 3'd3}: font = 5'b10001;
			{5'd13, 3'd4}: font = 5'b11111;
			{5'd13, 3'd5}: font = 5'b10000;
			{5'd13, 3'd6}: font = 5'b01110;
			{5'd14, 3'd0}: font = 5'b00000;   // x
			{5'd14, 3'd1}: font = 5'b00000;
			{5'd14, 3'd2}: font = 5'b10001;
			{5'd14, 3'd3}: font = 5'b01010;
			{5'd14, 3'd4}: font = 5'b00100;
			{5'd14, 3'd5}: font = 5'b01010;
			{5'd14, 3'd6}: font = 5'b10001;
			{5'd15, 3'd0}: font = 5'b00000;   // p
			{5'd15, 3'd1}: font = 5'b00000;
			{5'd15, 3'd2}: font = 5'b11110;
			{5'd15, 3'd3}: font = 5'b10001;
			{5'd15, 3'd4}: font = 5'b11110;
			{5'd15, 3'd5}: font = 5'b10000;
			{5'd15, 3'd6}: font = 5'b10000;
			{5'd16, 3'd0}: font = 5'b00000;   // m
			{5'd16, 3'd1}: font = 5'b00000;
			{5'd16, 3'd2}: font = 5'b11010;
			{5'd16, 3'd3}: font = 5'b10101;
			{5'd16, 3'd4}: font = 5'b10101;
			{5'd16, 3'd5}: font = 5'b10001;
			{5'd16, 3'd6}: font = 5'b10001;
			{5'd17, 3'd0}: font = 5'b00000;   // s
			{5'd17, 3'd1}: font = 5'b00000;
			{5'd17, 3'd2}: font = 5'b01111;
			{5'd17, 3'd3}: font = 5'b10000;
			{5'd17, 3'd4}: font = 5'b01110;
			{5'd17, 3'd5}: font = 5'b00001;
			{5'd17, 3'd6}: font = 5'b11110;
			{5'd18, 3'd0}: font = 5'b00000;   // n
			{5'd18, 3'd1}: font = 5'b00000;
			{5'd18, 3'd2}: font = 5'b10110;
			{5'd18, 3'd3}: font = 5'b11001;
			{5'd18, 3'd4}: font = 5'b10001;
			{5'd18, 3'd5}: font = 5'b10001;
			{5'd18, 3'd6}: font = 5'b10001;
			{5'd19, 3'd0}: font = 5'b00000;   // u
			{5'd19, 3'd1}: font = 5'b00000;
			{5'd19, 3'd2}: font = 5'b10001;
			{5'd19, 3'd3}: font = 5'b10001;
			{5'd19, 3'd4}: font = 5'b10001;
			{5'd19, 3'd5}: font = 5'b10011;
			{5'd19, 3'd6}: font = 5'b01101;
			{5'd20, 3'd0}: font = 5'b01100;   // l
			{5'd20, 3'd1}: font = 5'b00100;
			{5'd20, 3'd2}: font = 5'b00100;
			{5'd20, 3'd3}: font = 5'b00100;
			{5'd20, 3'd4}: font = 5'b00100;
			{5'd20, 3'd5}: font = 5'b00100;
			{5'd20, 3'd6}: font = 5'b01110;
			default: font = 5'b00000;
		endcase
	endfunction

	// the two small lines for exposure setting i: exposure time, and the flicker it cannot see (1 / exposure)
	// rows 24 16 12 8 6 4 3 2 x 113.3 us; 12 characters each
	function [4:0] txt(input [2:0] i, input ln, input [3:0] pos);
		case ({i, ln, pos})
			// 0: "exp 2.72 ms "
			{3'd0, 1'b0, 4'd0}: txt = 5'd13;
			{3'd0, 1'b0, 4'd1}: txt = 5'd14;
			{3'd0, 1'b0, 4'd2}: txt = 5'd15;
			{3'd0, 1'b0, 4'd4}: txt = 5'd2;
			{3'd0, 1'b0, 4'd5}: txt = 5'd10;
			{3'd0, 1'b0, 4'd6}: txt = 5'd7;
			{3'd0, 1'b0, 4'd7}: txt = 5'd2;
			{3'd0, 1'b0, 4'd9}: txt = 5'd16;
			{3'd0, 1'b0, 4'd10}: txt = 5'd17;
			// 0: "null  368 Hz"
			{3'd0, 1'b1, 4'd0}: txt = 5'd18;
			{3'd0, 1'b1, 4'd1}: txt = 5'd19;
			{3'd0, 1'b1, 4'd2}: txt = 5'd20;
			{3'd0, 1'b1, 4'd3}: txt = 5'd20;
			{3'd0, 1'b1, 4'd6}: txt = 5'd3;
			{3'd0, 1'b1, 4'd7}: txt = 5'd6;
			{3'd0, 1'b1, 4'd8}: txt = 5'd8;
			{3'd0, 1'b1, 4'd10}: txt = 5'd11;
			{3'd0, 1'b1, 4'd11}: txt = 5'd12;
			// 1: "exp 1.81 ms "
			{3'd1, 1'b0, 4'd0}: txt = 5'd13;
			{3'd1, 1'b0, 4'd1}: txt = 5'd14;
			{3'd1, 1'b0, 4'd2}: txt = 5'd15;
			{3'd1, 1'b0, 4'd4}: txt = 5'd1;
			{3'd1, 1'b0, 4'd5}: txt = 5'd10;
			{3'd1, 1'b0, 4'd6}: txt = 5'd8;
			{3'd1, 1'b0, 4'd7}: txt = 5'd1;
			{3'd1, 1'b0, 4'd9}: txt = 5'd16;
			{3'd1, 1'b0, 4'd10}: txt = 5'd17;
			// 1: "null  552 Hz"
			{3'd1, 1'b1, 4'd0}: txt = 5'd18;
			{3'd1, 1'b1, 4'd1}: txt = 5'd19;
			{3'd1, 1'b1, 4'd2}: txt = 5'd20;
			{3'd1, 1'b1, 4'd3}: txt = 5'd20;
			{3'd1, 1'b1, 4'd6}: txt = 5'd5;
			{3'd1, 1'b1, 4'd7}: txt = 5'd5;
			{3'd1, 1'b1, 4'd8}: txt = 5'd2;
			{3'd1, 1'b1, 4'd10}: txt = 5'd11;
			{3'd1, 1'b1, 4'd11}: txt = 5'd12;
			// 2: "exp 1.36 ms "
			{3'd2, 1'b0, 4'd0}: txt = 5'd13;
			{3'd2, 1'b0, 4'd1}: txt = 5'd14;
			{3'd2, 1'b0, 4'd2}: txt = 5'd15;
			{3'd2, 1'b0, 4'd4}: txt = 5'd1;
			{3'd2, 1'b0, 4'd5}: txt = 5'd10;
			{3'd2, 1'b0, 4'd6}: txt = 5'd3;
			{3'd2, 1'b0, 4'd7}: txt = 5'd6;
			{3'd2, 1'b0, 4'd9}: txt = 5'd16;
			{3'd2, 1'b0, 4'd10}: txt = 5'd17;
			// 2: "null  736 Hz"
			{3'd2, 1'b1, 4'd0}: txt = 5'd18;
			{3'd2, 1'b1, 4'd1}: txt = 5'd19;
			{3'd2, 1'b1, 4'd2}: txt = 5'd20;
			{3'd2, 1'b1, 4'd3}: txt = 5'd20;
			{3'd2, 1'b1, 4'd6}: txt = 5'd7;
			{3'd2, 1'b1, 4'd7}: txt = 5'd3;
			{3'd2, 1'b1, 4'd8}: txt = 5'd6;
			{3'd2, 1'b1, 4'd10}: txt = 5'd11;
			{3'd2, 1'b1, 4'd11}: txt = 5'd12;
			// 3: "exp 0.91 ms "
			{3'd3, 1'b0, 4'd0}: txt = 5'd13;
			{3'd3, 1'b0, 4'd1}: txt = 5'd14;
			{3'd3, 1'b0, 4'd2}: txt = 5'd15;
			{3'd3, 1'b0, 4'd4}: txt = 5'd0;
			{3'd3, 1'b0, 4'd5}: txt = 5'd10;
			{3'd3, 1'b0, 4'd6}: txt = 5'd9;
			{3'd3, 1'b0, 4'd7}: txt = 5'd1;
			{3'd3, 1'b0, 4'd9}: txt = 5'd16;
			{3'd3, 1'b0, 4'd10}: txt = 5'd17;
			// 3: "null 1103 Hz"
			{3'd3, 1'b1, 4'd0}: txt = 5'd18;
			{3'd3, 1'b1, 4'd1}: txt = 5'd19;
			{3'd3, 1'b1, 4'd2}: txt = 5'd20;
			{3'd3, 1'b1, 4'd3}: txt = 5'd20;
			{3'd3, 1'b1, 4'd5}: txt = 5'd1;
			{3'd3, 1'b1, 4'd6}: txt = 5'd1;
			{3'd3, 1'b1, 4'd7}: txt = 5'd0;
			{3'd3, 1'b1, 4'd8}: txt = 5'd3;
			{3'd3, 1'b1, 4'd10}: txt = 5'd11;
			{3'd3, 1'b1, 4'd11}: txt = 5'd12;
			// 4: "exp 0.68 ms "
			{3'd4, 1'b0, 4'd0}: txt = 5'd13;
			{3'd4, 1'b0, 4'd1}: txt = 5'd14;
			{3'd4, 1'b0, 4'd2}: txt = 5'd15;
			{3'd4, 1'b0, 4'd4}: txt = 5'd0;
			{3'd4, 1'b0, 4'd5}: txt = 5'd10;
			{3'd4, 1'b0, 4'd6}: txt = 5'd6;
			{3'd4, 1'b0, 4'd7}: txt = 5'd8;
			{3'd4, 1'b0, 4'd9}: txt = 5'd16;
			{3'd4, 1'b0, 4'd10}: txt = 5'd17;
			// 4: "null 1471 Hz"
			{3'd4, 1'b1, 4'd0}: txt = 5'd18;
			{3'd4, 1'b1, 4'd1}: txt = 5'd19;
			{3'd4, 1'b1, 4'd2}: txt = 5'd20;
			{3'd4, 1'b1, 4'd3}: txt = 5'd20;
			{3'd4, 1'b1, 4'd5}: txt = 5'd1;
			{3'd4, 1'b1, 4'd6}: txt = 5'd4;
			{3'd4, 1'b1, 4'd7}: txt = 5'd7;
			{3'd4, 1'b1, 4'd8}: txt = 5'd1;
			{3'd4, 1'b1, 4'd10}: txt = 5'd11;
			{3'd4, 1'b1, 4'd11}: txt = 5'd12;
			// 5: "exp 0.45 ms "
			{3'd5, 1'b0, 4'd0}: txt = 5'd13;
			{3'd5, 1'b0, 4'd1}: txt = 5'd14;
			{3'd5, 1'b0, 4'd2}: txt = 5'd15;
			{3'd5, 1'b0, 4'd4}: txt = 5'd0;
			{3'd5, 1'b0, 4'd5}: txt = 5'd10;
			{3'd5, 1'b0, 4'd6}: txt = 5'd4;
			{3'd5, 1'b0, 4'd7}: txt = 5'd5;
			{3'd5, 1'b0, 4'd9}: txt = 5'd16;
			{3'd5, 1'b0, 4'd10}: txt = 5'd17;
			// 5: "null 2207 Hz"
			{3'd5, 1'b1, 4'd0}: txt = 5'd18;
			{3'd5, 1'b1, 4'd1}: txt = 5'd19;
			{3'd5, 1'b1, 4'd2}: txt = 5'd20;
			{3'd5, 1'b1, 4'd3}: txt = 5'd20;
			{3'd5, 1'b1, 4'd5}: txt = 5'd2;
			{3'd5, 1'b1, 4'd6}: txt = 5'd2;
			{3'd5, 1'b1, 4'd7}: txt = 5'd0;
			{3'd5, 1'b1, 4'd8}: txt = 5'd7;
			{3'd5, 1'b1, 4'd10}: txt = 5'd11;
			{3'd5, 1'b1, 4'd11}: txt = 5'd12;
			// 6: "exp 0.34 ms "
			{3'd6, 1'b0, 4'd0}: txt = 5'd13;
			{3'd6, 1'b0, 4'd1}: txt = 5'd14;
			{3'd6, 1'b0, 4'd2}: txt = 5'd15;
			{3'd6, 1'b0, 4'd4}: txt = 5'd0;
			{3'd6, 1'b0, 4'd5}: txt = 5'd10;
			{3'd6, 1'b0, 4'd6}: txt = 5'd3;
			{3'd6, 1'b0, 4'd7}: txt = 5'd4;
			{3'd6, 1'b0, 4'd9}: txt = 5'd16;
			{3'd6, 1'b0, 4'd10}: txt = 5'd17;
			// 6: "null 2943 Hz"
			{3'd6, 1'b1, 4'd0}: txt = 5'd18;
			{3'd6, 1'b1, 4'd1}: txt = 5'd19;
			{3'd6, 1'b1, 4'd2}: txt = 5'd20;
			{3'd6, 1'b1, 4'd3}: txt = 5'd20;
			{3'd6, 1'b1, 4'd5}: txt = 5'd2;
			{3'd6, 1'b1, 4'd6}: txt = 5'd9;
			{3'd6, 1'b1, 4'd7}: txt = 5'd4;
			{3'd6, 1'b1, 4'd8}: txt = 5'd3;
			{3'd6, 1'b1, 4'd10}: txt = 5'd11;
			{3'd6, 1'b1, 4'd11}: txt = 5'd12;
			// 7: "exp 0.23 ms "
			{3'd7, 1'b0, 4'd0}: txt = 5'd13;
			{3'd7, 1'b0, 4'd1}: txt = 5'd14;
			{3'd7, 1'b0, 4'd2}: txt = 5'd15;
			{3'd7, 1'b0, 4'd4}: txt = 5'd0;
			{3'd7, 1'b0, 4'd5}: txt = 5'd10;
			{3'd7, 1'b0, 4'd6}: txt = 5'd2;
			{3'd7, 1'b0, 4'd7}: txt = 5'd3;
			{3'd7, 1'b0, 4'd9}: txt = 5'd16;
			{3'd7, 1'b0, 4'd10}: txt = 5'd17;
			// 7: "null 4414 Hz"
			{3'd7, 1'b1, 4'd0}: txt = 5'd18;
			{3'd7, 1'b1, 4'd1}: txt = 5'd19;
			{3'd7, 1'b1, 4'd2}: txt = 5'd20;
			{3'd7, 1'b1, 4'd3}: txt = 5'd20;
			{3'd7, 1'b1, 4'd5}: txt = 5'd4;
			{3'd7, 1'b1, 4'd6}: txt = 5'd4;
			{3'd7, 1'b1, 4'd7}: txt = 5'd1;
			{3'd7, 1'b1, 4'd8}: txt = 5'd4;
			{3'd7, 1'b1, 4'd10}: txt = 5'd11;
			{3'd7, 1'b1, 4'd11}: txt = 5'd12;
			default: txt = 5'd31;
		endcase
	endfunction

	// graph: one point per screen line (2 sensor rows), -31..31
	reg  [7:0] plot [0:511];
	always @(posedge pw_clk) if (pw_we) plot[pw_addr] <= pw_val;
	reg  [7:0] pnow;
	always @(posedge clk) pnow <= plot[v[8:0]];

	// text "dddd.d Hz" at (16, 16): 9 characters of 32 x 32 pixels (5 x 7 font, x 4)
	wire [9:0] tx = h - 10'd16;
	wire [9:0] ty = v - 10'd16;
	wire       in_box  = (h >= 8) && (h < 8 + 9 * 32 + 16) && (v >= 8) && (v < 100);
	wire       in_text = (h >= 16) && (tx < 9 * 32) && (v >= 16) && (ty < 32);
	wire [3:0] tcell = tx[9:5];      // which character
	wire [3:0] d4 = f_bcd[19:16], d3 = f_bcd[15:12], d2 = f_bcd[11:8], d1 = f_bcd[7:4], d0 = f_bcd[3:0];
	reg  [4:0] ch;
	always @(*)
		case (tcell)
			4'd0: ch = (d4 == 0) ? 5'd31 : {1'b0, d4};                       // no leading zeros
			4'd1: ch = (d4 == 0 && d3 == 0) ? 5'd31 : {1'b0, d3};
			4'd2: ch = (d4 == 0 && d3 == 0 && d2 == 0) ? 5'd31 : {1'b0, d2};
			4'd3: ch = {1'b0, d1};
			4'd4: ch = 5'd10;                                                // '.'
			4'd5: ch = {1'b0, d0};
			4'd7: ch = 5'd11;                                                // 'H'
			4'd8: ch = 5'd12;                                                // 'z'
			default: ch = 5'd31;
		endcase
	wire [4:0] frow  = font(ch, ty[4:2]);
	wire [2:0] fcol  = tx[4:2];
	wire       t_on1 = in_text && (fcol < 5) && frow[3'd4 - fcol];

	// two small lines (x 2, 16 x 16 cells) at y 56 and 76: "exp 0.91 ms", "null 1103 Hz"
	wire [9:0] sx  = h - 10'd16;
	wire [9:0] sy2 = v - 10'd56;
	wire [9:0] sy3 = v - 10'd76;
	wire       in2 = (h >= 16) && (sx < 12 * 16) && (v >= 56) && (sy2 < 16);
	wire       in3 = (h >= 16) && (sx < 12 * 16) && (v >= 76) && (sy3 < 16);
	wire [4:0] ch23  = txt(exp_i, in3, sx[7:4]);
	wire [4:0] frow2 = font(ch23, in3 ? sy3[3:1] : sy2[3:1]);
	wire [2:0] fcol2 = sx[3:1];
	wire       t_on  = t_on1 || ((in2 || in3) && (fcol2 < 5) && frow2[3'd4 - fcol2]);

	// graph band x 576..639: centre line, and the point (3 pixels wide)
	wire        in_g   = (h >= 576) && (v < 480);
	wire signed [10:0] gx = $signed({1'b0, h}) - 11'sd608 - $signed({{3{pnow[7]}}, pnow});
	wire        g_dot  = in_g && (gx >= -11'sd1) && (gx <= 11'sd1);
	wire        g_mid  = in_g && (h == 608);

	// one clock of delay to line up with rdata
	reg        vis_d, hs_d, vs_d;
	reg        ov_box, ov_txt, ov_g, ov_dot, ov_mid;
	reg [11:0] bars_d;
	reg        xd0, yd0;               // lowest bit of the frame-buffer x and y
	reg [1:0]  fc = 0;                 // screen frame counter
	always @(posedge clk) begin
		vis_d <= vis; hs_d <= hs; vs_d <= vs; bars_d <= bars;
		ov_box <= flick && in_box;  ov_txt <= flick && t_on;
		ov_g   <= flick && in_g;    ov_dot <= flick && g_dot;  ov_mid <= flick && g_mid;
		xd0 <= h[1];  yd0 <= v[1];
		if (h == 0 && v == 0) fc <= fc + 1'b1;
	end

	// temporal dither RGB565 -> RGB444
	wire [4:0] r5 = rdata[15:11];
	wire [5:0] g6 = rdata[10:5];
	wire [4:0] b5 = rdata[4:0];
	wire       p1 = xd0 ^ yd0 ^ fc[0];                       // red / blue: every 2nd frame
	reg  [1:0] t2;                                           // green: 0..3, each once per 4 frames
	always @(*)
		case ({yd0 ^ fc[1], xd0 ^ fc[0]})
			2'b00: t2 = 2'd0;  2'b01: t2 = 2'd2;  2'b10: t2 = 2'd3;  default: t2 = 2'd1;
		endcase
	wire       up_r = r5[0] && p1 && (r5[4:1] != 4'hF);
	wire       up_g = (g6[1:0] > t2) && (g6[5:2] != 4'hF);
	wire       up_b = b5[0] && p1 && (b5[4:1] != 4'hF);
	wire [11:0] cam = {r5[4:1] + up_r, g6[5:2] + up_g, b5[4:1] + up_b};

	// event camera: ON = green, OFF = red, brighter when newer; no event = the reference, very dim
	wire [2:0]  age = rdata[2:0];
	wire [3:0]  lvl = {age, 1'b1};
	wire [3:0]  bg  = {2'b0, rdata[11:10]};
	wire [11:0] evc = (age == 0) ? {bg, bg, bg} : rdata[3] ? {4'h0, lvl, 4'h0} : {lvl, 8'h00};

	wire [11:0] img = pattern ? bars_d : events ? evc : cam;
	wire [11:0] px  = !vis_d ? 12'h000 :
	                  ov_txt ? 12'hFF0 : ov_box ? 12'h000 :                 // yellow text on black
	                  ov_dot ? 12'hFFF : ov_mid ? 12'h555 : ov_g ? 12'h000 : img;
	always @(posedge clk) begin
		{vga_r, vga_g, vga_b} <= px;
		vga_hs <= hs_d;
		vga_vs <= vs_d;
	end

endmodule
