// tb_vga.v - temporal dithering in vga_out.v.
//   Every frame-buffer pixel holds R5 = 11, G6 = 35, B5 = 6, i.e. 4-bit levels R 5.5, G 8.75, B 3.
//   Over 4 screen frames each screen pixel must average exactly that (sums 22, 35, 12), and in every
//   single frame the 2x2 frame-buffer block (4x4 screen pixels) must already sum to it (no flicker
//   of the area as a whole).
// Run: iverilog -g2005 -o v.vvp tb_vga.v ../vga_out.v && vvp -n v.vvp
`timescale 1ns/1ps
module tb_vga;
	reg clk = 0;  always #20 clk = ~clk;
	wire [16:0] raddr;
	reg  [15:0] rdata = 0;
	wire [3:0]  r, g, b;
	wire        hs, vs;
	vga_out u(.clk(clk), .pattern(1'b0), .events(1'b0), .flick(1'b0), .f_bcd(20'h0), .exp_i(3'd0),
	          .pw_clk(1'b0), .pw_we(1'b0), .pw_addr(9'h0), .pw_val(8'h0), .raddr(raddr), .rdata(rdata),
	          .vga_r(r), .vga_g(g), .vga_b(b), .vga_hs(hs), .vga_vs(vs));
	always @(posedge clk) rdata <= {5'd11, 6'd35, 5'd6};

	// screen position of the colour on the pins: 2 clocks after h, v
	reg [9:0] h1, h2, v1, v2;
	always @(posedge clk) begin h1 <= u.h; v1 <= u.v; h2 <= h1; v2 <= v1; end

	integer sr [0:15], sg [0:15], sb [0:15];      // per screen pixel (0..3, 0..3), over 4 frames
	integer fr, fg, fb;                           // this frame, over the 2x2 fb block (4 fb pixels)
	integer i, frame = 0, errors = 0;
	initial for (i = 0; i < 16; i = i + 1) begin sr[i] = 0; sg[i] = 0; sb[i] = 0; end
	initial begin fr = 0; fg = 0; fb = 0; end
	always @(posedge clk) begin
		// screen pixels (0..3, 0..3) cover fb pixels (0..1, 0..1); count each fb pixel once (even h, v)
		if (frame >= 1 && frame <= 4 && h2 < 4 && v2 < 4) begin
			sr[v2 * 4 + h2] = sr[v2 * 4 + h2] + r;
			sg[v2 * 4 + h2] = sg[v2 * 4 + h2] + g;
			sb[v2 * 4 + h2] = sb[v2 * 4 + h2] + b;
			if (!h2[0] && !v2[0]) begin fr = fr + r; fg = fg + g; fb = fb + b; end
		end
		if (h2 == 700 && v2 == 3 && frame >= 1 && frame <= 4) begin
			$display("frame %0d: 2x2 block sums R %0d G %0d B %0d (want 22 35 12)", frame, fr, fg, fb);
			if (fr != 22 || fg != 35 || fb != 12) errors = errors + 1;
			fr = 0; fg = 0; fb = 0;
		end
		if (h2 == 799 && v2 == 524) frame = frame + 1;   // end of a screen frame
		if (frame == 5) begin
			for (i = 0; i < 16; i = i + 1)
				if (sr[i] != 22 || sg[i] != 35 || sb[i] != 12) begin
					$display("ERROR: screen pixel (%0d,%0d) 4-frame sums R %0d G %0d B %0d", i % 4, i / 4, sr[i], sg[i], sb[i]);
					errors = errors + 1;
				end
			$display("each screen pixel over 4 frames: R %0d G %0d B %0d (want 22 35 12)", sr[5], sg[5], sb[5]);
			if (errors == 0) $display("ALL CHECKS PASSED"); else $display("%0d CHECK(S) FAILED", errors);
			$finish;
		end
	end
endmodule
