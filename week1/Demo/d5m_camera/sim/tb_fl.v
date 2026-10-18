// tb_fl.v - flicker mode (SW6): a lamp flickering at FLICK_HZ lights a scene with a brightness
//   gradient; each row's brightness is taken at the moment the row is read (rolling shutter).
//   Small rows (128 pixels + 20 blanking = 5.92 us per row, 480 rows), so the lamp is made faster
//   to keep stripes as wide in rows as a real 100 Hz lamp's (88 rows): 2800 Hz = 60 rows, 1800 Hz =
//   94 rows.  Flicker depth only 15 %, and every row gets a random offset of up to +-3 % (the
//   sensor's row noise, which looks like thin stripes).  Checks: exposure register = 24, frequency
//   within 1 %, HEX shows F and the dot, the high range (SW5) at ~10 rows per period, and a steady
//   lamp reads 0.
`timescale 1ns/1ps
module tb_fl;
	reg clk50 = 0;  always #10 clk50 = ~clk50;
	reg pclk = 0;   initial begin #7; forever #20 pclk = ~pclk; end

	wire [9:0] LEDR;  wire [7:0] HEX0, HEX1, HEX2, HEX3, HEX4, HEX5;
	wire [3:0] VGA_R, VGA_G, VGA_B;  wire VGA_HS, VGA_VS;
	reg  [11:0] D = 0;  reg LVAL = 0, FVAL = 0;
	wire XCLKIN, RESET_N, TRIGGER, SCLK, SDATA;
	pullup(SDATA);
	reg sda_drv = 0;  assign SDATA = sda_drv ? 1'b0 : 1'bz;

	// SW6 = flicker, SW9..7 = 3 (display x8)
	reg  [9:0] SW = 10'b011_1_0_00000;
	reg        key1 = 1;
	d5m_cam_top #(.BAYER(2'd0), .WB_R0(8'd64), .WB_B0(8'd64), .LOG_FILE("../log.hex"), .KEY_BITS(6)) dut(
		.MAX10_CLK1_50(clk50), .KEY({key1, 1'b1}), .SW(SW), .LEDR(LEDR),
		.HEX0(HEX0), .HEX1(HEX1), .HEX2(HEX2), .HEX3(HEX3), .HEX4(HEX4), .HEX5(HEX5),
		.VGA_R(VGA_R), .VGA_G(VGA_G), .VGA_B(VGA_B), .VGA_HS(VGA_HS), .VGA_VS(VGA_VS),
		.D5M_PIXCLK(pclk), .D5M_D(D), .D5M_LVAL(LVAL), .D5M_FVAL(FVAL), .D5M_STROBE(1'b0),
		.D5M_XCLKIN(XCLKIN), .D5M_RESET_N(RESET_N), .D5M_TRIGGER(TRIGGER),
		.D5M_SCLK(SCLK), .D5M_SDATA(SDATA), .GPIO_X(15'h7FFF));

	reg [7:0] bytes [0:3];  reg [7:0] by;  integer nb, k;
	reg [15:0] exp_reg = 0;
	always @(negedge SDATA) if (SCLK === 1'b1) begin
		for (nb = 0; nb < 4; nb = nb + 1) begin
			for (k = 0; k < 8; k = k + 1) begin @(posedge SCLK); by = {by[6:0], SDATA}; end
			bytes[nb] = by;
			@(negedge SCLK); sda_drv = 1;  @(negedge SCLK); sda_drv = 0;
		end
		if (bytes[1] == 8'h09) exp_reg = {bytes[2], bytes[3]};
	end

	real    flick_hz = 2800.0, depth = 0.15, light;
	integer r, c, base, seed = 1, v, rown, ncol = 128;
	task frame;
		begin
			@(negedge pclk); FVAL = 1;
			for (r = 0; r < 480; r = r + 1) begin
				light = 1.0 + depth * $sin(2.0 * 3.14159265 * flick_hz * $realtime * 1e-9);
				base  = 600 + 2 * r;                               // the scene: brighter towards the bottom
				rown  = $random(seed) % 30;                        // row noise, +-3 %
				for (c = 0; c < ncol; c = c + 1) begin
					@(negedge pclk); LVAL = 1;
					v = base * light * (1000 + rown) / 1000 + ($random(seed) % 8);
					D = (v < 0) ? 0 : (v > 4095) ? 4095 : v;
				end
				@(negedge pclk); LVAL = 0;  repeat (20) @(negedge pclk);
			end
			FVAL = 0;  repeat (300) @(negedge pclk);
		end
	endtask

	defparam dut.u_fl.HOLD = 3;      // 3 frames instead of ~2 s, to keep the simulation short
	integer errors = 0, i;
	initial begin
		wait (LEDR[1] === 1'b1);
		repeat (2000) @(negedge clk50);
		$display("exposure register = %0d (want 24)", exp_reg);
		if (exp_reg != 24) begin $display("ERROR: exposure"); errors = errors + 1; end
		for (i = 0; i < 4; i = i + 1) begin
			frame;
			repeat (100) @(negedge pclk);
			$display("frame %0d: %0d stripes, frequency %0d.%0d Hz (lamp %0.1f Hz)",
			         i + 1, dut.fl_n, dut.f10 / 10, dut.f10 % 10, flick_hz);
		end
		if (dut.f10 < 27720 || dut.f10 > 28280) begin $display("ERROR: frequency not within 1 %%"); errors = errors + 1; end
		if (HEX5[6:0] !== 7'b0001110 || HEX1[7] !== 1'b0) begin $display("ERROR: HEX5 should show F and HEX1 its dot"); errors = errors + 1; end
		$display("HEX: %h", dut.fl_bcd);
		flick_hz = 1800.0;
		for (i = 0; i < 6; i = i + 1) frame;           // the first frame still holds the old lamp's stripes
		repeat (100) @(negedge pclk);
		$display("lamp 1800 Hz: %0d stripes, frequency %0d.%0d Hz", dut.fl_n, dut.f10 / 10, dut.f10 % 10);
		if (dut.f10 < 17820 || dut.f10 > 18180) begin $display("ERROR: frequency not within 1 %%"); errors = errors + 1; end
		// high range (SW5): rows of 300 pixels (12.8 us) and an 8 kHz lamp = ~10 rows per period,
		// like ~900 Hz on the real camera (113 us rows)
		SW[5] = 1'b1;  ncol = 300;  flick_hz = 8000.0;
		repeat (3) begin key1 = 0; repeat (300) @(negedge pclk); key1 = 1; repeat (300) @(negedge pclk); end   // exposure 24 -> 16 -> 12 -> 8
		for (i = 0; i < 6; i = i + 1) frame;
		repeat (100) @(negedge pclk);
		$display("high range, lamp 8000 Hz: %0d stripes, frequency %0d.%0d Hz, exposure register %0d (want 8)",
		         dut.fl_n, dut.f10 / 10, dut.f10 % 10, exp_reg);
		if (dut.f10 < 79200 || dut.f10 > 80800) begin $display("ERROR: high-range frequency not within 1 %%"); errors = errors + 1; end
		if (exp_reg != 8) begin $display("ERROR: high-range exposure"); errors = errors + 1; end
		$display("exposure setting %0d, display shift %0d (SW9..7 = 3 + 2)", dut.exp_i, dut.fl_dshift);
		if (dut.fl_dshift != 5) begin $display("ERROR: display brightness"); errors = errors + 1; end
		SW[5] = 1'b0;  ncol = 128;  flick_hz = 1800.0;
		depth = 0.0;
		for (i = 0; i < 6; i = i + 1) frame;           // 1 frame of old stripes + HOLD = 3 frames
		repeat (100) @(negedge pclk);
		$display("steady lamp: %0d stripes, frequency %0d (want 0); stripe size %0d noise %0d, gaps %0d..%0d",
		         dut.fl_n, dut.f10, dut.fl_swing, dut.fl_noise, dut.u_fl.gmin, dut.u_fl.gmax);
		if (dut.f10 != 0) begin $display("ERROR: steady light should read 0"); errors = errors + 1; end
		if (errors == 0) $display("ALL CHECKS PASSED"); else $display("%0d CHECK(S) FAILED", errors);
		$finish;
	end
endmodule
