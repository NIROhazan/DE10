// tb_wb.v - one-shot white balance (KEY1 in camera mode) on small frames (128 x 64 -> 32 x 16).
//   A grey card that the sensor sees as red = green / 2, blue = green * 3/4 (a colour cast).
//   Before KEY1: gains x1 and the picture is tinted.  After KEY1: red x2, blue x1.33 and the picture is grey.
//   Then the light changes: the gains must stay where they are (one-shot, no hunting).
//   KEY0 puts them back to x1.
`timescale 1ns/1ps
module tb_wb;
	reg clk50 = 0;  always #10 clk50 = ~clk50;
	reg pclk = 0;   initial begin #7; forever #20 pclk = ~pclk; end

	wire [9:0] LEDR;  wire [7:0] HEX0, HEX1, HEX2, HEX3, HEX4, HEX5;
	wire [3:0] VGA_R, VGA_G, VGA_B;  wire VGA_HS, VGA_VS;
	reg  [11:0] D = 0;  reg LVAL = 0, FVAL = 0;
	reg  key0 = 1, key1 = 1;
	wire XCLKIN, RESET_N, TRIGGER, SCLK, SDATA;
	pullup(SDATA);
	reg sda_drv = 0;  assign SDATA = sda_drv ? 1'b0 : 1'bz;

	d5m_cam_top #(.BAYER(2'd0), .WB_R0(8'd64), .WB_B0(8'd64), .LOG_FILE("../log.hex"), .KEY_BITS(6)) dut(
		.MAX10_CLK1_50(clk50), .KEY({key1, key0}), .SW(10'b011_0_0_00000), .LEDR(LEDR),
		.HEX0(HEX0), .HEX1(HEX1), .HEX2(HEX2), .HEX3(HEX3), .HEX4(HEX4), .HEX5(HEX5),
		.VGA_R(VGA_R), .VGA_G(VGA_G), .VGA_B(VGA_B), .VGA_HS(VGA_HS), .VGA_VS(VGA_VS),
		.D5M_PIXCLK(pclk), .D5M_D(D), .D5M_LVAL(LVAL), .D5M_FVAL(FVAL), .D5M_STROBE(1'b0),
		.D5M_XCLKIN(XCLKIN), .D5M_RESET_N(RESET_N), .D5M_TRIGGER(TRIGGER),
		.D5M_SCLK(SCLK), .D5M_SDATA(SDATA), .GPIO_X(15'h7FFF));

	// I2C slave: acknowledges everything
	reg [7:0] by;  integer nb, k;
	always @(negedge SDATA) if (SCLK === 1'b1) begin
		for (nb = 0; nb < 4; nb = nb + 1) begin
			for (k = 0; k < 8; k = k + 1) begin @(posedge SCLK); by = {by[6:0], SDATA}; end
			@(negedge SCLK); sda_drv = 1;  @(negedge SCLK); sda_drv = 0;
		end
	end

	integer gval = 2000, rval = 1000, bval = 1500;
	integer r, c;
	task frame;
		begin
			@(negedge pclk); FVAL = 1;
			for (r = 0; r < 64; r = r + 1) begin
				for (c = 0; c < 128; c = c + 1) begin
					@(negedge pclk); LVAL = 1;
					if (!r[0] && !c[0])     D = rval;      // a = red   (bayer 0)
					else if (r[0] && c[0])  D = bval;      // d = blue
					else                    D = gval;
				end
				@(negedge pclk); LVAL = 0;  repeat (20) @(negedge pclk);
			end
			FVAL = 0;  repeat (200) @(negedge pclk);
		end
	endtask

	integer errors = 0, i;
	function [15:0] rgb565(input integer r, input integer g, input integer b);
		rgb565 = ((r >> 7) << 11) | ((g >> 6) << 5) | (b >> 7);
	endfunction
	task show(input [8*20-1:0] what);
		$display("%0s: gain R x%0.2f B x%0.2f, pixel RGB = %h, LEDR7 measuring = %b, LEDR8 set = %b",
		         what, dut.gain_r / 64.0, dut.gain_b / 64.0, dut.u_ram.mem[5 * 320 + 10], LEDR[7], LEDR[8]);
	endtask
	task press1; begin key1 = 0; repeat (300) @(negedge pclk); key1 = 1; repeat (300) @(negedge pclk); end endtask

	initial begin
		wait (LEDR[1] === 1'b1);
		repeat (3) frame;
		show("before KEY1");
		if (dut.gain_r != 64 || dut.gain_b != 64 || dut.u_ram.mem[5 * 320 + 10] != rgb565(1000, 2000, 1500)) begin
			$display("ERROR: want x1 and pixel %h", rgb565(1000, 2000, 1500)); errors = errors + 1; end
		press1;
		if (LEDR[7] !== 1'b1) begin $display("ERROR: LEDR7 not on while measuring"); errors = errors + 1; end
		for (i = 0; i < 5; i = i + 1) frame;
		show("after KEY1");
		if (dut.gain_r < 126 || dut.gain_r > 130 || dut.gain_b < 84 || dut.gain_b > 87) begin
			$display("ERROR: want R x2 (128), B x1.33 (85)"); errors = errors + 1; end
		if (dut.u_ram.mem[5 * 320 + 10] != rgb565(2000, 2000, 1500 * 85 / 64)) begin
			$display("ERROR: pixel not grey, want %h", rgb565(2000, 2000, 1500 * 85 / 64)); errors = errors + 1; end
		if (LEDR[8:7] !== 2'b10) begin $display("ERROR: LEDs"); errors = errors + 1; end
		rval = 2000; bval = 2000;                       // the light changes
		for (i = 0; i < 4; i = i + 1) frame;
		show("light changed");
		if (dut.gain_r < 126 || dut.gain_r > 130) begin $display("ERROR: gains moved by themselves"); errors = errors + 1; end
		key0 = 0;  repeat (300) @(negedge pclk);  key0 = 1;
		wait (LEDR[1] === 1'b0);  wait (LEDR[1] === 1'b1);
		frame;
		show("after KEY0");
		if (dut.gain_r != 64 || dut.gain_b != 64) begin $display("ERROR: KEY0 did not clear"); errors = errors + 1; end
		if (errors == 0) $display("ALL CHECKS PASSED"); else $display("%0d CHECK(S) FAILED", errors);
		$finish;
	end
endmodule
