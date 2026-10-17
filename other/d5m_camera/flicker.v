// flicker.v - measures how fast the light flickers, from the rolling shutter.
//
// The sensor reads its rows one after the other (one every 113.3 us), so a light that flickers
// faster than a frame makes horizontal stripes: rows read while the lamp was bright are brighter.
// Per row: s = sum of all its pixels.  d = s - (s of the same row in the previous frame):
// the scene cancels, the stripes stay (they move from frame to frame because a frame is not a
// whole number of flicker periods).  d is smoothed (sm += (d - sm) / 8, or / 2 with fast = 1): the
// sensor adds random noise to whole rows, which would look like thin stripes; a lamp's stripes are
// far wider (100 Hz = 88 rows).  Low range ~40-200 Hz, fast (high range) ~150-1000 Hz.
// Down the frame sm swings + and -; every swing from - to + (with hysteresis = 1/4 of the last
// frame's biggest |sm|) is one flicker period.  The noise is measured too: what the smoothing
// takes away (|d - sm|, averaged over the frame).  A frame counts only if it has at least 4
// swings, evenly spaced (longest gap <= 1.5 x shortest: noise swings come at random), and its
// biggest swing is at least 1.5 x the noise.  The display averages good frames (new = 3/4 old +
// 1/4 frame, or jumps if the frame differs by > 1/32), keeps the last value through bad frames,
// and goes to 0 after HOLD frames without a good one (a steady lamp).  Each swing is
// time-stamped in PIXCLKs (25 MHz), so
//     frequency = (swings - 1) periods / (time of last swing - time of first swing)
// f10 = frequency x 10 (one decimal), from a 36-bit division at the end of each frame.
module flicker #(
	parameter [35:0] CLK10 = 36'd250_000_000,     // PIXCLK x 10
	parameter        HOLD  = 18                   // frames (~2 s) without flicker before 0
)(
	input             clk,                // PIXCLK
	input      [11:0] d,                  // straight from the camera pins
	input             lval,
	input             fval,
	input             fast,               // 1 = high range: smoothing over ~2 rows instead of ~8
	output reg [16:0] f10 = 0,            // frequency x 10, 0 = no flicker found
	output reg [7:0]  ncross = 0,         // swings found in the last frame
	output reg        done = 0,           // one-clock pulse: f10 is new
	output reg [22:0] swing = 0,          // last frame: biggest smoothed |d| (for tools/pins.py)
	output reg [24:0] noise_lvl = 0,      //             and the noise
	output reg        plot_we = 0,        // graph for the screen: smoothed d of every 2nd row,
	output reg [8:0]  plot_addr = 0,      //   at screen line row / 2,
	output reg [7:0]  plot_val = 0        //   scaled to -31..31 by the last frame's biggest swing
);
	reg [11:0] d_r;
	reg        lval_r = 0, fval_r = 0, lval_d = 0, fval_d = 0;
	always @(posedge clk) begin
		d_r <= d;
		lval_r <= lval;  lval_d <= lval_r;
		fval_r <= fval;  fval_d <= fval_r;
	end

	reg  [25:0] t = 0;                    // time in PIXCLKs
	reg  [22:0] acc = 0;                  // this row's sum (1280 x 4095 < 2^23)
	reg  [9:0]  row = 0;
	reg  [22:0] prev [0:1023];            // last frame's row sums
	reg  [22:0] pq = 0;
	wire signed [23:0] diff = $signed({1'b0, acc}) - $signed({1'b0, pq});
	reg  signed [23:0] sm = 0;            // smoothed diff
	wire signed [23:0] sm_n = (row == 0) ? diff : sm + ((diff - sm) >>> (fast ? 1 : 3));
	wire [23:0] neg  = -sm_n;
	wire [22:0] mag  = sm_n[23] ? neg[22:0] : sm_n[22:0];
	reg  [22:0] peak = 0, peak_prev = 0;
	wire [22:0] thr  = (peak_prev[22:2] > 23'd64) ? {2'b0, peak_prev[22:2]} : 23'd64;
	// noise: |d - sm|, added up over the frame (/1024 ~ /960 rows = its average)
	wire signed [23:0] res  = diff - sm;
	wire [23:0] nres = -res;
	wire [22:0] rmag = res[23] ? nres[22:0] : res[22:0];
	reg  [32:0] noise_acc = 0;
	wire [24:0] noise    = noise_acc[32:10];
	wire        strong   = {2'b0, peak, 1'b0} > {noise, 1'b0} + noise;   // biggest swing > 1.5 x noise
	// graph scale: shift so the last frame's biggest swing lands in 16..31
	reg  [4:0]  psh = 0;
	integer     bi;
	always @(*) begin
		psh = 0;
		for (bi = 4; bi < 23; bi = bi + 1) if (peak_prev[bi]) psh = bi - 4;
	end
	wire signed [23:0] pv = sm_n >>> psh;
	wire [7:0]  pclip = (pv > 24'sd31) ? 8'd31 : (pv < -24'sd31) ? -8'sd31 : pv[7:0];
	reg  [25:0] gmin = 0, gmax = 0;                                   // shortest / longest gap
	wire [25:0] gap      = t - t_last;
	wire        regular  = {gmax, 1'b0} <= {gmin, 1'b0} + gmin;       // longest <= 1.5 x shortest
	reg  [4:0]  miss = 0;                                             // frames since a good one
	wire [16:0] fq   = ({q[34:0], fits} > 36'd99999) ? 17'd99999 : {q[15:0], fits};
	wire [18:0] avg4 = {f10, 1'b0} + f10 + fq;                       // 3 old + 1 new
	wire [16:0] fdif = (fq > f10) ? fq - f10 : f10 - fq;
	wire        jump = (f10 == 0) || (fdif > {5'b0, f10[16:5]});
	wire        up   = sm_n > $signed({1'b0, thr});
	wire        dn   = sm_n < -$signed({1'b0, thr});
	reg  [1:0]  st = 0;                   // 0 = not known yet, 1 = below, 2 = above
	reg  [7:0]  n = 0;
	reg  [25:0] t_first = 0, t_last = 0;

	// division (one bit per clock)
	reg  [35:0] num = 0, q = 0;
	reg  [26:0] rem = 0;
	reg  [25:0] den = 1;
	reg  [5:0]  k = 0;
	wire [26:0] trial = {rem[25:0], num[35]};
	wire        fits  = trial >= {1'b0, den};

	always @(posedge clk) begin
		t    <= t + 1'b1;
		done <= 1'b0;
		plot_we <= 1'b0;

		if (lval_r) acc <= (lval_r && !lval_d) ? {11'b0, d_r} : acc + d_r;
		if (lval_r && !lval_d) pq <= prev[row];

		if (lval_d && !lval_r) begin              // end of a row: acc is its sum
			prev[row] <= acc;
			row <= row + 1'b1;
			if (!row[0]) begin plot_we <= 1'b1; plot_addr <= row[9:1]; plot_val <= pclip; end
			sm  <= sm_n;
			if (row != 0) noise_acc <= noise_acc + rmag;
			if (mag > peak) peak <= mag;
			case (st)
				2'd0: if (up) st <= 2'd2; else if (dn) st <= 2'd1;
				2'd1: if (up) begin
					st <= 2'd2;
					if (n != 8'hFF) n <= n + 1'b1;
					if (n == 0) t_first <= t;
					t_last <= t;
					if (n == 1) begin gmin <= gap; gmax <= gap; end
					else if (n > 1) begin
						if (gap < gmin) gmin <= gap;
						if (gap > gmax) gmax <= gap;
					end
				end
				default: if (dn) st <= 2'd1;
			endcase
		end

		if (fval_r && !fval_d) begin              // frame starts
			row <= 0;  st <= 0;  n <= 0;  peak <= 0;  noise_acc <= 0;
		end

		if (fval_d && !fval_r) begin              // frame ends
			peak_prev <= peak;
			ncross <= n;
			swing <= peak;  noise_lvl <= noise;
			if (n >= 8'd4 && regular && strong) begin
				miss <= 0;
				num <= CLK10 * (n - 1'b1);
				den <= t_last - t_first;
				q <= 0;  rem <= 0;  k <= 6'd36;
			end else begin
				if (miss == HOLD - 1) f10 <= 0;
				if (miss != HOLD - 1) miss <= miss + 1'b1;
				done <= 1'b1;
			end
		end else if (k != 0) begin
			rem <= fits ? trial - {1'b0, den} : trial;
			q   <= {q[34:0], fits};
			num <= {num[34:0], 1'b0};
			k   <= k - 1'b1;
			if (k == 6'd1) begin
				f10  <= jump ? fq : avg4[18:2];
				done <= 1'b1;
			end
		end
	end
endmodule
