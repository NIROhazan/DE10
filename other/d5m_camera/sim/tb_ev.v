// tb_ev.v - event camera (SW5) on small frames (128 x 64 sensor pixels -> 32 x 16 output pixels).
//   Grey scene (1000 of 4095).  Frames 1-4 only fill the references; 5-6 still: no events.
//   Frame 7: the patch x 8..15, y 4..7 (32 output pixels) twice as bright -> 32 ON events there, none elsewhere.
//   Frame 8 same: no events, the patch fades (age 7 -> 5).  Frame 9 patch back to 1000 -> 32 OFF events.
//   Frames 10-13 still: ages 5, 3, 1, 0.  Also: exposure snapped to 88 rows, KEY1 raises the threshold,
//   events in decimal for HEX, and the frame buffer is never asked to read and write in the same clock.
`timescale 1ns/1ps
module tb_ev;
	reg clk50 = 0;  always #10 clk50 = ~clk50;
	reg pclk = 0;   initial begin #7; forever #20 pclk = ~pclk; end

	wire [9:0] LEDR;  wire [7:0] HEX0, HEX1, HEX2, HEX3, HEX4, HEX5;
	wire [3:0] VGA_R, VGA_G, VGA_B;  wire VGA_HS, VGA_VS;
	reg  [11:0] D = 0;  reg LVAL = 0, FVAL = 0;
	reg  key1 = 1;
	wire XCLKIN, RESET_N, TRIGGER, SCLK, SDATA;
	pullup(SDATA);
	reg sda_drv = 0;  assign SDATA = sda_drv ? 1'b0 : 1'bz;

	// SW9..7 = 3 (exposure 1024 rows), SW5 = event camera
	d5m_cam_top #(.BAYER(2'd0), .WB_R0(8'd64), .WB_B0(8'd64), .LOG_FILE("../log.hex"), .KEY_BITS(6)) dut(
		.MAX10_CLK1_50(clk50), .KEY({key1, 1'b1}), .SW(10'b011_0_1_00000), .LEDR(LEDR),
		.HEX0(HEX0), .HEX1(HEX1), .HEX2(HEX2), .HEX3(HEX3), .HEX4(HEX4), .HEX5(HEX5),
		.VGA_R(VGA_R), .VGA_G(VGA_G), .VGA_B(VGA_B), .VGA_HS(VGA_HS), .VGA_VS(VGA_VS),
		.D5M_PIXCLK(pclk), .D5M_D(D), .D5M_LVAL(LVAL), .D5M_FVAL(FVAL), .D5M_STROBE(1'b0),
		.D5M_XCLKIN(XCLKIN), .D5M_RESET_N(RESET_N), .D5M_TRIGGER(TRIGGER),
		.D5M_SCLK(SCLK), .D5M_SDATA(SDATA), .GPIO_X(15'h7FFF));

	// I2C slave: remembers R0x09
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

	// sensor: flat grey, the patch at patch_val
	integer patch_val = 1000;
	integer r, c, frame_no = 0;
	function in_patch(input integer rr, input integer cc);
		in_patch = (cc >= 32 && cc < 64 && rr >= 16 && rr < 32);
	endfunction
	task frame;
		begin
			@(negedge pclk); FVAL = 1;
			for (r = 0; r < 64; r = r + 1) begin
				for (c = 0; c < 128; c = c + 1) begin
					@(negedge pclk); LVAL = 1;
					D = in_patch(r, c) ? patch_val : 1000;
				end
				@(negedge pclk); LVAL = 0;  repeat (20) @(negedge pclk);
			end
			FVAL = 0;  repeat (200) @(negedge pclk);
			frame_no = frame_no + 1;
		end
	endtask

	integer errors = 0, i, x, y, bad;
	reg [15:0] w;
	// every output pixel: inside the patch age must be pin_age with polarity pin_pol, outside age 0
	task check_frame(input integer want_events, input integer pin_age, input integer pin_pol);
		begin
			bad = 0;
			for (y = 0; y < 16; y = y + 1)
				for (x = 0; x < 32; x = x + 1) begin
					w = dut.u_ram.mem[y * 320 + x];
					if (x >= 8 && x < 16 && y >= 4 && y < 8) begin
						if (w[2:0] != pin_age || (pin_age != 0 && w[3] != pin_pol)) bad = bad + 1;
					end else if (w[2:0] != 0) bad = bad + 1;
				end
			$display("frame %2d: %0d events (want %0d), patch word %h, outside word %h, wrong pixels %0d",
			         frame_no, dut.ev_count, want_events, dut.u_ram.mem[5 * 320 + 10], dut.u_ram.mem[0], bad);
			if (dut.ev_count != want_events || bad != 0) begin $display("ERROR"); errors = errors + 1; end
		end
	endtask

	initial begin
		wait (LEDR[1] === 1'b1);
		repeat (2000) @(negedge clk50);
		$display("config done, exposure register = %0d (want 1056 = 12 x 88)", exp_reg);
		if (exp_reg != 1056) begin $display("ERROR: exposure not snapped"); errors = errors + 1; end
		for (i = 0; i < 4; i = i + 1) frame;           // priming
		frame; check_frame(0, 0, 0);
		frame; check_frame(0, 0, 0);
		patch_val = 2000;
		frame; check_frame(32, 7, 1);
		repeat (40) @(negedge pclk);
		$display("events on HEX4..HEX0 (BCD) = %h (want 00032)", dut.ev_bcd);
		if (dut.ev_bcd != 20'h00032) begin $display("ERROR: BCD"); errors = errors + 1; end
		frame; check_frame(0, 5, 1);
		patch_val = 1000;
		frame; check_frame(32, 7, 0);
		frame; check_frame(0, 5, 0);
		frame; check_frame(0, 3, 0);
		frame; check_frame(0, 1, 0);
		frame; check_frame(0, 0, 0);
		// KEY1: threshold 4 -> 5
		key1 = 0;  repeat (300) @(negedge pclk);  key1 = 1;  repeat (300) @(negedge pclk);
		$display("threshold after KEY1: %0d (want 5), HEX5 = %b", dut.thr_i + 1, HEX5[6:0]);
		if (dut.thr_i != 4 || HEX5[6:0] != 7'b0010010) begin $display("ERROR: KEY1"); errors = errors + 1; end
		$display("read/write clashes: %0d", dut.u_cap.rw_clash);
		if (dut.u_cap.rw_clash != 0) errors = errors + 1;
		if (errors == 0) $display("ALL CHECKS PASSED"); else $display("%0d CHECK(S) FAILED", errors);
		$finish;
	end
endmodule
