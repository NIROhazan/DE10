// d5m_capture.v - turns the D5M's Bayer pixel stream into a 320 x 240 RGB444 frame.
//
// The sensor sends rows of 12-bit pixels in a 2x2 colour pattern (Bayer):
//      a b        one 2x2 block = one red, two green, one blue pixel
//      c d
// Every 4x4 sensor pixels (four 2x2 blocks) make one output pixel, 1280 x 960 -> 320 x 240.
// bayer[1:0] says which of a b c d is red (the blue is the opposite corner).
//   avg = 0: only the top-left 2x2 block of the 4x4 is used (red, mean of the 2 greens, blue),
//            like Terasic's RAW2RGB
//   avg = 1: the whole 4x4 is averaged (4 reds, 8 greens, 4 blues): same colours, less noise
// Red and blue are multiplied by their white-balance gains (white_bal.v, 64 = x1), then the frame
// buffer gets RGB565: the top 5 bits of red, 6 of green, 5 of blue.  The DE10-Lite's VGA has only
// 4 bits per colour; vga_out.v shows the extra bits by temporal dithering.
// The R, G, B of every frame are added up for the white balance.
//
// Event camera (ev_mode = 1): instead of colours, each frame-buffer word keeps
//   {reference log brightness 8, polarity 1, age 3}.
// Every frame each pixel's log brightness L is compared with its reference: if it rose by more
// than ev_thr it is an ON event, fell by more than ev_thr an OFF event; either way the reference
// becomes L and age = 7.  No event: the reference stays and the age fades by 2 per frame.
// The frame buffer is read (port A, camera clock) a clock before the comparison and two clocks
// before the same word is written.  For the first frames after switching on (prime) the
// references are only filled in, no events.
//
// It also measures the sensor: pixels per line, lines per frame, row and frame period.
module d5m_capture #(
	parameter LOG_FILE = "log.hex"
)(
	input             pclk,
	input      [11:0] d,
	input             lval,
	input             fval,
	input      [1:0]  bayer,        // position of red: 0 = a, 1 = b, 2 = c, 3 = d
	input             freeze,       // 1 = stop writing (keep the last picture)
	input             avg,          // 1 = average the whole 4x4
	input      [7:0]  gain_r,       // white balance, 64 = x1
	input      [7:0]  gain_b,
	input      [2:0]  dshift,       // display brightness x 2^dshift (flicker mode's short exposure)
	output reg [28:0] sum_r,        // last frame, after the gains
	output reg [28:0] sum_g,
	output reg [28:0] sum_b,
	input             ev_mode,      // 1 = event camera
	input      [7:0]  ev_thr,       // event threshold, log steps (~36 = x2 in light)
	output reg        we,
	output     [16:0] waddr,        // frame buffer address: y * 320 + x (write), or the next pixel (read)
	output reg [15:0] wdata,        // {R 5, G 6, B 5}, or {0000, reference 8, polarity, age 3}
	input      [15:0] rq,           // frame buffer word at waddr, one clock later
	output reg [16:0] ev_count,     // events in the last frame
	output reg [11:0] pixels,       // pixels in the last line
	output reg [11:0] lines,        // lines in the last frame
	output reg [7:0]  frames,       // counts frames
	output reg [15:0] row_period,   // PIXCLKs from one line start to the next
	output reg [25:0] frame_period, // PIXCLKs from one frame start to the next
	output reg        frame_end     // one-clock pulse at the end of each frame
);

	// ---- register the inputs once ----
	reg [11:0] d_r;
	reg        lval_r, fval_r, lval_d, fval_d;
	always @(posedge pclk) begin
		d_r    <= d;
		lval_r <= lval;  lval_d <= lval_r;
		fval_r <= fval;  fval_d <= fval_r;
	end

	// ---- where is pixel d_r? ----
	reg [11:0] col, row;
	always @(posedge pclk) begin
		if (!lval_r) col <= 0;
		else         col <= col + 1'b1;
		if (!fval_r)                  row <= 0;
		else if (lval_d && !lval_r)   row <= row + 1'b1;   // end of a line
	end

	// ---- measurements ----
	reg [15:0] rcnt = 0;
	reg [25:0] fcnt = 0;
	initial frames = 0;
	always @(posedge pclk) begin
		rcnt <= rcnt + 1'b1;
		fcnt <= fcnt + 1'b1;
		frame_end <= fval_d && !fval_r;
		if (lval_r && !lval_d) begin row_period <= rcnt; rcnt <= 1; end
		if (fval_r && !fval_d) begin frame_period <= fcnt; fcnt <= 1; end
		if (lval_d && !lval_r) pixels <= col;
		if (fval_d && !fval_r) begin
			lines  <= row;
			frames <= frames + 1'b1;
		end
	end

	// ---- 4x4 -> 1: add up the colours ----
	wire [8:0] x    = col[10:2];
	wire [7:0] y    = row[9:2];
	wire       keep = lval_r && fval_r && (col[11:2] < 12'd320) && (row[11:2] < 12'd240);
	wire       take = avg || (!col[1] && !row[1]);  // without avg: the top-left 2x2 only
	wire [1:0] pos  = {row[0], col[0]};             // 0 = a, 1 = b, 2 = c, 3 = d
	wire       is_r = take && (pos == bayer);
	wire       is_b = take && (pos == ~bayer);       // opposite corner
	wire       is_g = take && (pos != bayer) && (pos != ~bayer);

	// this line's share of the 4 pixels of block x
	reg  [12:0] pr, pg, pb;
	wire [12:0] part_r = (col[1:0] == 0 ? 13'd0 : pr) + (is_r ? d_r : 12'd0);
	wire [12:0] part_g = (col[1:0] == 0 ? 13'd0 : pg) + (is_g ? d_r : 12'd0);
	wire [12:0] part_b = (col[1:0] == 0 ? 13'd0 : pb) + (is_b ? d_r : 12'd0);

	// earlier lines of the block: {R 14, G 15, B 14}
	reg  [42:0] lb [0:319];
	reg  [42:0] lbq;
	wire [13:0] tot_r = lbq[42:29] + part_r;
	wire [14:0] tot_g = lbq[28:14] + part_g;
	wire [13:0] tot_b = lbq[13:0]  + part_b;

	reg         va;                 // stage A: one output pixel, 12-bit
	reg  [8:0]  xa;
	reg  [7:0]  ya;
	reg  [11:0] ra, ga, ba;
	always @(posedge pclk) begin
		va <= 1'b0;
		if (keep) begin
			pr <= part_r; pg <= part_g; pb <= part_b;
			if (col[1:0] == 2'd0) lbq <= lb[x];
			if (col[1:0] == 2'd3) begin
				case (row[1:0])
					2'd0:    lb[x] <= {1'b0, part_r, 2'b0, part_g, 1'b0, part_b};
					2'd3:    begin
						va <= 1'b1; xa <= x; ya <= y;
						ra <= avg ? tot_r[13:2] : tot_r[11:0];    // 4 reds / 4,   or the one red
						ga <= avg ? tot_g[14:3] : tot_g[12:1];    // 8 greens / 8, or 2 greens / 2
						ba <= avg ? tot_b[13:2] : tot_b[11:0];
					end
					default: lb[x] <= {tot_r, tot_g, tot_b};
				endcase
			end
		end
	end

	// ---- white balance gains ----
	wire [19:0] mr = ra * gain_r;
	wire [19:0] mb = ba * gain_b;
	wire [11:0] wr = (mr[19:18] != 0) ? 12'hFFF : mr[17:6];
	wire [11:0] wb = (mb[19:18] != 0) ? 12'hFFF : mb[17:6];

	// display brightness: x 2^dshift, clipped
	function [11:0] shl(input [11:0] v, input [2:0] s);
		reg [18:0] w;
		begin
			w   = {7'b0, v} << s;
			shl = (w[18:12] != 0) ? 12'hFFF : w[11:0];
		end
	endfunction
	wire [11:0] dr = shl(wr, dshift);
	wire [11:0] dg = shl(ga, dshift);
	wire [11:0] db = shl(wb, dshift);

	// ---- stage B: address (the frame buffer reads it), log brightness ----
	reg  [7:0]  log_rom [0:1023];
	initial $readmemh(LOG_FILE, log_rom);
	wire [13:0] ysum = ra + {ga, 1'b0} + ba;      // 4 x brightness (R + 2G + B)
	reg         vb, vc;
	reg  [16:0] ab, ac;
	reg  [15:0] colb, colc;
	reg  [7:0]  ldb, ld;
	reg  [11:0] rs, gs, bs;

	// frame sums for the white balance
	reg [28:0] acc_r = 0, acc_g = 0, acc_b = 0;
	always @(posedge pclk)
		if (fval_d && !fval_r) begin
			sum_r <= acc_r;  sum_g <= acc_g;  sum_b <= acc_b;
			acc_r <= 0;      acc_g <= 0;      acc_b <= 0;
		end else if (vb) begin
			acc_r <= acc_r + rs;  acc_g <= acc_g + gs;  acc_b <= acc_b + bs;
		end
	always @(posedge pclk) begin
		vb <= va;  vc <= vb;
		ab <= {ya, 8'b0} + {ya, 6'b0} + xa;       // y*256 + y*64 + x
		ac <= ab;
		colb <= {dr[11:7], dg[11:6], db[11:7]};  colc <= colb;
		rs <= wr;  gs <= ga;  bs <= wb;
		ldb  <= log_rom[ysum[13:4]];             ld   <= ldb;
	end

	// ---- stage C: rq = this pixel's old word; compare with the reference ----
	wire [7:0] rref = rq[11:4];
	wire       rpol = rq[3];
	wire [2:0] rage = rq[2:0];
	wire [8:0] ref_up = rref + ev_thr;
	wire [8:0] ld_up  = ld + ev_thr;
	wire       ev_on  = {1'b0, ld} > ref_up;            // brighter by more than the threshold
	wire       ev_off = ld_up < {1'b0, rref};          // darker by more than the threshold
	reg  [2:0] prime = 3'd4;
	wire       ev     = (prime == 0) && (ev_on || ev_off);
	wire [11:0] ev_word = (prime != 0) ? {ld, 4'b0} :
	                      ev           ? {ld, ev_on, 3'd7} :
	                                     {rref, rpol, (rage > 3'd2) ? rage - 3'd2 : 3'd0};
	reg  [16:0] ev_acc = 0;
	always @(posedge pclk) begin
		if (!ev_mode)                             prime <= 3'd4;  // fill references for ~3 frames first
		else if (fval_d && !fval_r && prime != 0) prime <= prime - 1'b1;
		if (fval_d && !fval_r) begin
			ev_count <= ev_acc;
			ev_acc   <= 0;
		end else if (vc && ev_mode && ev && !freeze)
			ev_acc <= ev_acc + 1'b1;
	end

	// ---- write (stage D) ----
	reg [16:0] wa;
	assign waddr = we ? wa : ab;        // read in stage B, write in stage D; pixels are 4 clocks apart
	always @(posedge pclk) begin
		we <= vc && !freeze;
		if (vc) begin
			wa    <= ac;
			wdata <= ev_mode ? {4'b0, ev_word} : colc;
		end
	end

	// synthesis translate_off
	integer rw_clash = 0;               // a read needed in the same clock as a write: must stay 0
	always @(posedge pclk) if (vb && we) rw_clash = rw_clash + 1;
	// synthesis translate_on

endmodule
