// d5m_cam_top.v - TRDB-D5M camera -> VGA monitor on the Terasic DE10-Lite.
//
// The D5M sits on the 2x20 GPIO header (JP1).  The picture appears on a VGA
// monitor at 640 x 480 (320 x 240 camera pixels, each shown as 2 x 2).
//
//   KEY0        reset: restarts the camera and writes its registers again
//   KEY1        camera: white balance - point at something white, press (KEY0 = back to the default)
//               event camera: next threshold (HEX5 = 1..8)
//   SW0         VGA colour bars instead of the camera (checks monitor + cable)
//   SW1         freeze the picture
//   SW3..SW2    which corner of the 2x2 colour block is red: all down = right for this camera
//               (green/pink picture = SW2 wrong, red and blue swapped = SW3 wrong)
//   SW4         the sensor sends its own colour bars (checks camera -> FPGA path)
//   SW5         event camera: ON events green, OFF events red, events per frame on HEX4..HEX0
//   SW6         flicker: exposure 24 rows (2.7 ms), a flickering lamp makes stripes (rolling shutter);
//               HEX = F and the flicker frequency in Hz (e.g. F 0100.0); SW9..SW7 = brightness x 2^SW
//               KEY1 with SW6: next exposure, 24 16 12 8 6 4 3 2 rows (2.72 .. 0.23 ms); the screen shows it
//               and the flicker it cannot see (1 / exposure); the display brightens to make up for it
//               SW5 with SW6: light smoothing (~2 rows) for fast flicker, instead of ~8 rows
//   SW9..SW7    exposure: 128 << SW[9:7] rows (0 = darkest, 7 = brightest)
//
//   HEX5..HEX3  lines per frame, hex   (expected 3C0 = 960)     [event camera: see SW5]
//   HEX2..HEX0  pixels per line, hex   (expected 500 = 1280)
//   LEDR0       blinks every 8 frames  (camera is sending frames)
//   LEDR1       camera registers written
//   LEDR2       a register write was not acknowledged (camera not answering)
//   LEDR3       blinks while PIXCLK runs
//   LEDR4/5     FVAL / LVAL from the camera
//   LEDR6       picture frozen
//   LEDR7       white balance measuring (~1/3 s after KEY1)
//   LEDR8       white balance set (not x1)
//   LEDR9       event camera on
module d5m_cam_top #(
	parameter LOG_FILE   = "log.hex",
	parameter KEY_BITS   = 18,            // KEY1 is looked at every 2^KEY_BITS PIXCLKs (~10 ms)
	parameter AVG        = 1,             // 1 = average each 4x4 (less noise); 0 = one 2x2 block
	parameter BAYER      = 2'd2,          // red position with SW3..SW2 down (measured on the board: c)
	parameter [7:0] WB_R0 = 8'd38,        // default white balance, 64 = x1 (measured under room light:
	parameter [7:0] WB_B0 = 8'd90         //   red x0.59, blue x1.41)
)(
	input         MAX10_CLK1_50,
	input  [1:0]  KEY,
	input  [9:0]  SW,
	output [9:0]  LEDR,
	output [7:0]  HEX0, HEX1, HEX2, HEX3, HEX4, HEX5,

	output [3:0]  VGA_R, VGA_G, VGA_B,
	output        VGA_HS, VGA_VS,

	input         D5M_PIXCLK,
	input  [11:0] D5M_D,
	input         D5M_LVAL,
	input         D5M_FVAL,
	input         D5M_STROBE,
	output        D5M_XCLKIN,
	output        D5M_RESET_N,
	output        D5M_TRIGGER,
	output        D5M_SCLK,
	inout         D5M_SDATA,
	input  [14:0] GPIO_X        // the header pins the D5M does not use, for the pin monitor
);

	wire clk50 = MAX10_CLK1_50;

	// ---- 25 MHz: VGA pixel clock and the camera's input clock ----
	reg clk25 = 1'b0;
	always @(posedge clk50) clk25 <= ~clk25;
	assign D5M_XCLKIN  = clk25;
	assign D5M_TRIGGER = 1'b1;

	// ---- reset: hold the camera in reset ~1.3 ms, then configure it ----
	reg [1:0]  key0_s = 2'b11;
	reg [17:0] por    = 0;
	always @(posedge clk50) begin
		key0_s <= {key0_s[0], KEY[0]};
		if (!key0_s[1])   por <= 0;
		else if (!por[17]) por <= por + 1'b1;
	end
	assign D5M_RESET_N = por[17] | por[16];   // high from 1.3 ms on, and stays high
	wire cfg_rst_n = por[17];

	// the same reset in the camera clock: clears the white balance at power-up and on KEY0
	reg [1:0] rst_p = 2'b00;
	always @(posedge D5M_PIXCLK) rst_p <= {rst_p[0], por[17]};

	// ---- camera registers over I2C ----
	reg [9:0] sw_s1, sw_s2;
	always @(posedge clk50) begin sw_s1 <= SW; sw_s2 <= sw_s1; end

	wire [15:0] exp_sw = 16'h0080 << sw_s2[9:7];

	// flicker mode exposure, chosen with KEY1 (exp_i, camera clock): into this clock when two samples agree
	reg  [2:0] exp_i = 3'd0;
	reg  [2:0] ei_s1 = 0, ei_s2 = 0, ei = 0;
	always @(posedge clk50) begin
		ei_s1 <= exp_i;  ei_s2 <= ei_s1;
		if (ei_s1 == ei_s2) ei <= ei_s2;
	end
	reg  [15:0] exp_fl;
	always @(*)
		case (ei)
			3'd0: exp_fl = 16'd24;  3'd1: exp_fl = 16'd16;  3'd2: exp_fl = 16'd12;  3'd3: exp_fl = 16'd8;
			3'd4: exp_fl = 16'd6;   3'd5: exp_fl = 16'd4;   3'd6: exp_fl = 16'd3;   default: exp_fl = 16'd2;
		endcase

	// event camera: exposure = the nearest multiple of 88 rows (88 x 113.3 us = 10 ms), so lamps
	// flickering at 100 Hz look steady instead of making bands of events
	reg [16:0] snap_acc = 0;
	reg [15:0] exp_snap = 16'd88;
	always @(posedge clk50)
		if (snap_acc + 17'd44 >= exp_sw) begin
			exp_snap <= (snap_acc < 17'd88) ? 16'd88 : snap_acc[15:0];
			snap_acc <= 0;
		end else
			snap_acc <= snap_acc + 17'd88;
	wire [15:0] exposure = sw_s2[6] ? exp_fl : sw_s2[5] ? exp_snap : exp_sw;

	wire cfg_done, cfg_nack;
	d5m_i2c_cfg u_cfg(
		.clk     (clk50),
		.rst_n   (cfg_rst_n),
		.exposure(exposure),
		.test_pat(sw_s2[4]),
		.scl     (D5M_SCLK),
		.sda     (D5M_SDATA),
		.done    (cfg_done),
		.nack    (cfg_nack)
	);

	// ---- capture (camera clock) ----
	reg [9:0] sw_p1, sw_p2;          // the switches, into the camera clock
	always @(posedge D5M_PIXCLK) begin sw_p1 <= SW; sw_p2 <= sw_p1; end

	wire        frame_end;
	wire [19:0] fl_bcd;             // flicker frequency x 10, decimal (flicker.v -> HEX and VGA)
	wire        pl_we;              // flicker graph points (flicker.v -> VGA)
	wire [8:0]  pl_addr;
	wire [7:0]  pl_val;
	wire [28:0] sum_r, sum_g, sum_b;
	wire [7:0]  gain_r, gain_b;
	wire        wb_busy;
	white_bal #(.R0(WB_R0), .B0(WB_B0)) u_wb(
		.clk(D5M_PIXCLK), .clear(!rst_p[1]), .start(wb_start), .frame_end(frame_end),
		.sum_r(sum_r), .sum_g(sum_g), .sum_b(sum_b), .gain_r(gain_r), .gain_b(gain_b), .busy(wb_busy));
	wire [15:0] row_period;
	wire [25:0] frame_period;

	// ---- KEY1: next look (camera) / next threshold (event camera) ----
	wire fl_mode = sw_p2[6];
	// display brightness in flicker mode: SW9..7 (x 2^SW) plus ~log2(24 / exposure rows), at most x 128
	reg  [2:0] comp;
	always @(*)
		case (exp_i)
			3'd0: comp = 3'd0;  3'd1: comp = 3'd1;  3'd2: comp = 3'd1;  3'd3: comp = 3'd2;
			3'd4: comp = 3'd2;  3'd5: comp = 3'd3;  3'd6: comp = 3'd3;  default: comp = 3'd4;
		endcase
	wire [3:0] dsum      = sw_p2[9:7] + comp;
	wire [2:0] fl_dshift = dsum[3] ? 3'd7 : dsum[2:0];
	wire ev_mode = sw_p2[5] && !fl_mode;
	reg  [1:0] key1_s = 2'b11;
	reg  [KEY_BITS-1:0] key_div = 0;
	reg  key1_a = 1'b1, key1_b = 1'b1;
	reg        wb_start = 1'b0;
	wire       pc_wb;                           // white balance started from the PC (tools/wb.tcl)
	reg  [2:0] pc_wb_s = 3'b000;
	reg  [2:0] thr_i = 3'd3;
	always @(posedge D5M_PIXCLK) begin
		key1_s  <= {key1_s[0], KEY[1]};
		key_div <= key_div + 1'b1;
		pc_wb_s  <= {pc_wb_s[1:0], pc_wb};
		wb_start <= pc_wb_s[1] && !pc_wb_s[2];
		if (key_div == 0) begin                     // sample every ~10 ms: no bounce
			key1_a <= key1_s[1];
			key1_b <= key1_a;
			if (key1_b && !key1_a) begin             // pressed
				if (fl_mode)      exp_i <= exp_i + 1'b1;
				else if (ev_mode) thr_i <= thr_i + 1'b1;
				else              wb_start <= 1'b1;
			end
		end
	end
	reg [7:0] ev_thr;
	always @(*)
		case (thr_i)        // log steps; 36 = twice the light
			3'd0: ev_thr = 8'd3;   3'd1: ev_thr = 8'd5;   3'd2: ev_thr = 8'd8;   3'd3: ev_thr = 8'd12;
			3'd4: ev_thr = 8'd16;  3'd5: ev_thr = 8'd24;  3'd6: ev_thr = 8'd32;  default: ev_thr = 8'd48;
		endcase

	wire        we;
	wire [16:0] waddr;
	wire [15:0] wdata, wq;
	wire [16:0] ev_count;
	wire [11:0] pixels, lines;
	wire [7:0]  frames;
	d5m_capture #(.LOG_FILE(LOG_FILE)) u_cap(
		.pclk  (D5M_PIXCLK),
		.d     (D5M_D),
		.lval  (D5M_LVAL),
		.fval  (D5M_FVAL),
		.bayer (sw_p2[3:2] ^ BAYER),
		.freeze(sw_p2[1]),
		.avg   (AVG[0]),
		.gain_r(gain_r),
		.gain_b(gain_b),
		.dshift(fl_mode ? fl_dshift : 3'd0),
		.sum_r (sum_r),
		.sum_g (sum_g),
		.sum_b (sum_b),
		.ev_mode(ev_mode),
		.ev_thr(ev_thr),
		.we    (we),
		.waddr (waddr),
		.wdata (wdata),
		.rq    (wq),
		.ev_count(ev_count),
		.pixels(pixels),
		.lines (lines),
		.frames(frames),
		.row_period(row_period),
		.frame_period(frame_period),
		.frame_end(frame_end)
	);

	reg [23:0] pclk_cnt = 0;
	always @(posedge D5M_PIXCLK) pclk_cnt <= pclk_cnt + 1'b1;

	// ---- frame buffer and VGA ----
	wire [16:0] raddr;
	wire [15:0] rdata;
	frame_ram u_ram(
		.wclk (D5M_PIXCLK), .we(we), .waddr(waddr), .wdata(wdata), .wq(wq),
		.rclk (clk25),      .raddr(raddr), .rdata(rdata)
	);

	reg [1:0] sw0_s, sw5_s, sw6_s;
	reg [2:0] ei_v1, ei_v2;
	always @(posedge clk25) begin ei_v1 <= exp_i; ei_v2 <= ei_v1; end
	always @(posedge clk25) begin
		sw0_s <= {sw0_s[0], SW[0]};  sw5_s <= {sw5_s[0], SW[5] && !SW[6]};  sw6_s <= {sw6_s[0], SW[6]};
	end

	vga_out u_vga(
		.clk    (clk25),
		.pattern(sw0_s[1]),
		.events (sw5_s[1]),
		.flick  (sw6_s[1]),
		.f_bcd  (fl_bcd),
		.exp_i  (ei_v2),
		.pw_clk (D5M_PIXCLK),
		.pw_we  (pl_we),
		.pw_addr(pl_addr),
		.pw_val (pl_val),
		.raddr  (raddr),
		.rdata  (rdata),
		.vga_r  (VGA_R),
		.vga_g  (VGA_G),
		.vga_b  (VGA_B),
		.vga_hs (VGA_HS),
		.vga_vs (VGA_VS)
	);

	// ---- status ----
	assign LEDR[0]   = frames[3];
	assign LEDR[1]   = cfg_done;
	assign LEDR[2]   = cfg_nack;
	assign LEDR[3]   = pclk_cnt[23];
	assign LEDR[4]   = D5M_FVAL;
	assign LEDR[5]   = D5M_LVAL;
	assign LEDR[6]   = SW[1];
	assign LEDR[7]   = wb_busy;
	assign LEDR[8]   = gain_r != WB_R0 || gain_b != WB_B0;
	assign LEDR[9]   = ev_mode;

	// events per frame in decimal
	wire [19:0] ev_bcd;
	bin2bcd u_bcd(.clk(D5M_PIXCLK), .start(frame_end), .bin(ev_count), .bcd(ev_bcd));

	// ---- flicker frequency ----
	wire [16:0] f10;
	wire [7:0]  fl_n;
	wire        fl_done;
	wire [22:0] fl_swing;
	wire [24:0] fl_noise;
	flicker u_fl(.clk(D5M_PIXCLK), .d(D5M_D), .lval(D5M_LVAL), .fval(D5M_FVAL), .fast(sw_p2[5]),
	             .f10(f10), .ncross(fl_n), .done(fl_done), .swing(fl_swing), .noise_lvl(fl_noise),
	             .plot_we(pl_we), .plot_addr(pl_addr), .plot_val(pl_val));
	bin2bcd u_bcd2(.clk(D5M_PIXCLK), .start(fl_done), .bin(f10), .bcd(fl_bcd));

`ifndef NO_PIN_MONITOR      // left out of simulation: 36 counters at 50 MHz make it ~10x slower
	// ---- pin monitor, read from the PC (In-System Sources and Probes, tools/pins.tcl) ----
	// every header pin GPIO[0..35]: its level and how many edges it had in the last ~21 ms
	wire [35:0] hdr = {GPIO_X[14:4], D5M_SCLK, D5M_SDATA, D5M_FVAL, D5M_LVAL, D5M_STROBE, D5M_TRIGGER,
	                   GPIO_X[3], D5M_RESET_N, D5M_XCLKIN, GPIO_X[2], GPIO_X[1], D5M_D[0], D5M_D[1], D5M_D[2],
	                   D5M_D[3], D5M_D[4], D5M_D[5], D5M_D[6], D5M_D[7], D5M_D[8], D5M_D[9], D5M_D[10],
	                   GPIO_X[0], D5M_D[11], D5M_PIXCLK};
	reg  [35:0] hs1, hs2, hs3;
	reg  [7:0]  ecnt [0:35];
	reg  [7:0]  elat [0:35];
	reg  [19:0] win = 0;
	integer j;
	always @(posedge clk50) begin
		hs1 <= hdr; hs2 <= hs1; hs3 <= hs2;
		win <= win + 1'b1;
		for (j = 0; j < 36; j = j + 1) begin
			if (win == 0) begin
				elat[j] <= ecnt[j];
				ecnt[j] <= 0;
			end else if (hs2[j] != hs3[j] && ecnt[j] != 8'hFF)
				ecnt[j] <= ecnt[j] + 1'b1;
		end
	end
	wire [287:0] counts;
	genvar gi;
	generate for (gi = 0; gi < 36; gi = gi + 1) begin : g_cnt
		assign counts[gi*8 +: 8] = elat[gi];
	end endgenerate
	altsource_probe #(
		.sld_auto_instance_index("NO"), .sld_instance_index(0), .instance_id("PINS"),
		.probe_width(467), .source_width(1), .source_initial_value("0"), .enable_metastability("NO")
	) u_pins (
		.probe ({ev_mode, 1'b0, wb_busy, thr_i, ev_count, gain_b, gain_r, 8'd64, exposure, frame_period, row_period, counts, 4'b0, cfg_done, cfg_nack, frames, lines, pixels, hs2[35:32], hs2[31:0]}),
		.source(pc_wb)
	);
	// flicker meter, read by tools/pins.tcl as instance 1
	altsource_probe #(
		.sld_auto_instance_index("NO"), .sld_instance_index(1), .instance_id("FLK"),
		.probe_width(73), .source_width(0), .enable_metastability("NO")
	) u_flk (
		.probe ({fl_noise, fl_swing, fl_n, f10}),
		.source()
	);

`else
	assign pc_wb = 1'b0;
`endif

	// camera: lines and pixels in hex.  event camera: threshold 1..8, events per frame.
	// flicker: F and the frequency in Hz with one decimal (dot after HEX1)
	wire [23:0] hexv = fl_mode ? {4'hF, fl_bcd} : ev_mode ? {{1'b0, thr_i} + 4'd1, ev_bcd} : {lines, pixels};
	wire [7:0]  hex1_s;
	hex7 h0(.v(hexv[3:0]),   .seg(HEX0));
	hex7 h1(.v(hexv[7:4]),   .seg(hex1_s));
	assign HEX1 = {!fl_mode, hex1_s[6:0]};
	hex7 h2(.v(hexv[11:8]),  .seg(HEX2));
	hex7 h3(.v(hexv[15:12]), .seg(HEX3));
	hex7 h4(.v(hexv[19:16]), .seg(HEX4));
	hex7 h5(.v(hexv[23:20]), .seg(HEX5));

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

// binary -> 5 decimal digits (double dabble, one bit per clock), started once per frame
module bin2bcd(input clk, input start, input [16:0] bin, output reg [19:0] bcd = 0);
	reg [16:0] sh;
	reg [19:0] acc;
	reg [4:0]  n = 0;
	function [3:0] a3(input [3:0] d); a3 = (d > 4'd4) ? d + 4'd3 : d; endfunction
	wire [19:0] adj = {a3(acc[19:16]), a3(acc[15:12]), a3(acc[11:8]), a3(acc[7:4]), a3(acc[3:0])};
	wire [36:0] nxt = {adj, sh} << 1;
	always @(posedge clk)
		if (start) begin
			sh <= bin; acc <= 0; n <= 5'd17;
		end else if (n != 0) begin
			acc <= nxt[36:17]; sh <= nxt[16:0]; n <= n - 1'b1;
			if (n == 5'd1) bcd <= nxt[36:17];
		end
endmodule
