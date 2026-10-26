// week 4 ex9 board - Terasic DE1 (Cyclone II EP2C20F484C7). Instructor source: students get only board.sof.
// Glitches: a hidden Y = L1 V' + V L2 in slow motion (1 tick = 0.1 s), puzzle SW9..7; SW6 up adds the term L1 L2. HEX3..2 = ticks to the LAST change of Y, HEX1..0 = to the FIRST, LEDR3..0 = how many times Y changed.
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

	wire clk = CLOCK_50;
	wire t;
	tick10 tk(.clk(clk), .t(t));

	// the inputs, sampled every tick: {puzzle, fix, C, B, A}
	wire [6:0] now = {SW[9:6], SW[2:0]};
	reg  [6:0] in = 7'd0;
	always @(posedge clk) if (t) in <= now;
	wire changed = (now != in);
	wire fix = in[3];
	wire [2:0] p = in[6:4];

	reg v, l1, l2;
	reg [3:0] dN, dA, dO;
	always @(*) begin
		case (p)
			3'd0: begin v = in[0]; l1 = in[2]; l2 = ~in[1]; dN = 4'd2; dA = 4'd5; dO = 4'd1; end
			3'd1: begin v = in[2]; l1 = ~in[1]; l2 = ~in[0]; dN = 4'd2; dA = 4'd2; dO = 4'd4; end
			3'd2: begin v = in[1]; l1 = ~in[2]; l2 = in[0]; dN = 4'd6; dA = 4'd4; dO = 4'd1; end
			3'd3: begin v = in[2]; l1 = ~in[0]; l2 = in[1]; dN = 4'd4; dA = 4'd5; dO = 4'd2; end
			3'd4: begin v = in[2]; l1 = ~in[0]; l2 = ~in[1]; dN = 4'd3; dA = 4'd2; dO = 4'd4; end
			3'd5: begin v = in[2]; l1 = ~in[1]; l2 = in[0]; dN = 4'd2; dA = 4'd5; dO = 4'd1; end
			3'd6: begin v = in[1]; l1 = in[2]; l2 = ~in[0]; dN = 4'd5; dA = 4'd3; dO = 4'd3; end
			3'd7: begin v = in[0]; l1 = in[1]; l2 = ~in[2]; dN = 4'd3; dA = 4'd5; dO = 4'd1; end
			default: begin v = 1'b0; l1 = 1'b0; l2 = 1'b0; dN = 4'd1; dA = 4'd1; dO = 4'd1; end
		endcase
	end

	wire vn, n1, n2, n3, Y;
	dly g0(.clk(clk), .t(t), .x(~v),            .d(dN), .y(vn));
	dly g1(.clk(clk), .t(t), .x(l1 & vn),       .d(dA), .y(n1));
	dly g2(.clk(clk), .t(t), .x(v & l2),        .d(dA), .y(n2));
	dly g3(.clk(clk), .t(t), .x(l1 & l2 & fix), .d(dA), .y(n3));
	dly g4(.clk(clk), .t(t), .x(n1 | n2 | n3),  .d(dO), .y(Y));

	wire [6:0] first, last;
	wire [3:0] n;
	watch w(.clk(clk), .t(t), .changed(changed), .y(Y), .first(first), .last(last), .n(n));

	assign LEDG = {7'b0, Y};
	assign LEDR = {6'b0, n};
	dec2 dl(.v(last), .tens(HEX3), .ones(HEX2));
	dec2 df(.v(first), .tens(HEX1), .ones(HEX0));
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
