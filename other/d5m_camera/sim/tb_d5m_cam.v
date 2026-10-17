// tb_d5m_cam.v - Icarus testbench for d5m_cam_top with a model of the D5M:
//   * an I2C slave that acknowledges and logs every register write
//   * a sensor sending 1280 x 960 frames whose pixels encode their own position:
//       a (even row, even col) = x mod 16  in the top 4 bits  -> red
//       d (odd row,  odd col)  = y mod 16  in the top 4 bits  -> blue
//       b, c                   = 0x800                        -> green 8
//     so frame pixel (x, y) must read {x mod 16, 8, y mod 16}.
// Checks: register writes, measured line/frame size, frame-buffer contents, VGA timing.
// Run: iverilog -g2005 -o tb.vvp tb_d5m_cam.v altsource_probe_stub.v ../*.v  && vvp tb.vvp
`timescale 1ns/1ps
module tb_d5m_cam;

	reg        clk50 = 0;
	always #10 clk50 = ~clk50;
	reg        pclk = 0;
	initial begin #7; forever #20 pclk = ~pclk; end   // 25 MHz, unrelated phase

	reg  [1:0]  KEY = 2'b11;
	reg  [9:0]  SW  = 10'b011_0000000;   // exposure 128 << 3 = 1024 rows, bayer 0, live
	wire [9:0]  LEDR;
	wire [7:0]  HEX0, HEX1, HEX2, HEX3, HEX4, HEX5;
	wire [3:0]  VGA_R, VGA_G, VGA_B;
	wire        VGA_HS, VGA_VS;
	reg  [11:0] D = 0;
	reg         LVAL = 0, FVAL = 0;
	wire        XCLKIN, RESET_N, TRIGGER, SCLK, SDATA;

	pullup(SDATA);
	reg sda_drv = 0;                 // slave pulls SDA low when 1
	assign SDATA = sda_drv ? 1'b0 : 1'bz;

	d5m_cam_top #(.BAYER(2'd0), .WB_R0(8'd64), .WB_B0(8'd64), .LOG_FILE("../log.hex")) dut(
		.MAX10_CLK1_50(clk50), .KEY(KEY), .SW(SW), .LEDR(LEDR),
		.HEX0(HEX0), .HEX1(HEX1), .HEX2(HEX2), .HEX3(HEX3), .HEX4(HEX4), .HEX5(HEX5),
		.VGA_R(VGA_R), .VGA_G(VGA_G), .VGA_B(VGA_B), .VGA_HS(VGA_HS), .VGA_VS(VGA_VS),
		.D5M_PIXCLK(pclk), .D5M_D(D), .D5M_LVAL(LVAL), .D5M_FVAL(FVAL), .D5M_STROBE(1'b0),
		.D5M_XCLKIN(XCLKIN), .D5M_RESET_N(RESET_N), .D5M_TRIGGER(TRIGGER),
		.D5M_SCLK(SCLK), .D5M_SDATA(SDATA), .GPIO_X(15'h7FFF)
	);

	integer errors = 0;

	// ---------------- I2C slave ----------------
	reg [7:0] bytes [0:3];
	integer   nb, k, nwrites = 0;
	reg [7:0] by;
	reg       saw_exp = 0;
	always @(negedge SDATA) if (SCLK === 1'b1) begin       // START
		for (nb = 0; nb < 4; nb = nb + 1) begin
			for (k = 0; k < 8; k = k + 1) begin
				@(posedge SCLK); by = {by[6:0], SDATA};
			end
			bytes[nb] = by;
			@(negedge SCLK); sda_drv = 1;                   // ACK
			@(negedge SCLK); sda_drv = 0;
		end
		nwrites = nwrites + 1;
		if (bytes[0] != 8'hBA) begin
			$display("ERROR: device address %h", bytes[0]); errors = errors + 1;
		end
		$display("%0d ns  I2C write R0x%h = 0x%h%h", $time, bytes[1], bytes[2], bytes[3]);
		if (bytes[1] == 8'h09 && {bytes[2], bytes[3]} == 16'h0400) saw_exp = 1;
	end

	// ---------------- sensor ----------------
	integer r, c;
	task frame;
		begin
			FVAL <= 1;
			repeat (20) @(posedge pclk);
			for (r = 0; r < 960; r = r + 1) begin
				for (c = 0; c < 1280; c = c + 1) begin
					@(negedge pclk);                         // data changes on the falling edge
					LVAL = 1;
					if (!r[0] && !c[0])     D = {c[5:2], 8'h00};      // a: x = c/4
					else if (r[0] && c[0])  D = {r[5:2], 8'h00};      // d: y = r/4
					else                    D = 12'h800;
				end
				@(negedge pclk); LVAL = 0; D = 0;
				repeat (100) @(negedge pclk);
			end
			repeat (20) @(negedge pclk);
			FVAL = 0;
			repeat (500) @(negedge pclk);
		end
	endtask

	// ---------------- VGA timing ----------------
	time t_hs0 = 0, hs_period = 0;
	integer hs_in_frame = 0, hs_per_vs = 0, vs_seen = 0;
	always @(negedge VGA_HS) begin
		if (t_hs0 != 0) hs_period = $time - t_hs0;
		t_hs0 = $time;
		hs_in_frame = hs_in_frame + 1;
	end
	always @(negedge VGA_VS) begin
		if (vs_seen > 0) hs_per_vs = hs_in_frame;
		hs_in_frame = 0;
		vs_seen = vs_seen + 1;
	end

	// ---------------- the test ----------------
	integer x, y, bad;
	reg [15:0] want, got;
	initial begin
		wait (RESET_N === 1'b1);
		$display("%0d ns  camera out of reset", $time);
		wait (LEDR[1] === 1'b1);
		$display("%0d ns  config done after %0d writes, nack = %b", $time, nwrites, LEDR[2]);
		if (nwrites != 18) begin $display("ERROR: expected 18 writes (17 table + exposure)"); errors = errors + 1; end
		if (!saw_exp)      begin $display("ERROR: exposure 0x0400 not written");            errors = errors + 1; end
		if (LEDR[2])       begin $display("ERROR: NACK flagged");                           errors = errors + 1; end
		if (RESET_N !== 1'b1) begin $display("ERROR: camera back in reset");                errors = errors + 1; end

		frame;
		if (RESET_N !== 1'b1) begin $display("ERROR: camera back in reset after frame 1");  errors = errors + 1; end
		$display("%0d ns  frame 1 done: lines = %h, pixels = %h, frames = %0d",
		         $time, dut.u_cap.lines, dut.u_cap.pixels, dut.u_cap.frames);
		if (dut.u_cap.lines != 12'd960)   begin $display("ERROR: lines");  errors = errors + 1; end
		if (dut.u_cap.pixels != 12'd1280) begin $display("ERROR: pixels"); errors = errors + 1; end
		if (dut.u_cap.frames != 8'd1)     begin $display("ERROR: frames"); errors = errors + 1; end
		if (HEX5 !== 8'b1011_0000 || HEX4 !== 8'b1100_0110 || HEX3 !== 8'b1100_0000)
			begin $display("ERROR: HEX5..3 should read 3C0"); errors = errors + 1; end

		bad = 0;
		for (y = 0; y < 240; y = y + 1)
			for (x = 0; x < 320; x = x + 1) begin
				want = {x[3:0], 1'b0, 6'b100000, y[3:0], 1'b0};     // RGB565 of {x, 0x800, y}
				got  = dut.u_ram.mem[y * 320 + x];
				if (got !== want) begin
					if (bad < 5) $display("ERROR: fb(%0d,%0d) = %h, want %h", x, y, got, want);
					bad = bad + 1;
				end
			end
		$display("frame buffer: %0d of 76800 pixels wrong", bad);
		errors = errors + (bad != 0);

		// let VGA run for two full frames
		wait (vs_seen >= 3);
		$display("VGA: HS period %0d ns (want 32000), %0d lines per frame (want 525)", hs_period, hs_per_vs);
		if (hs_period != 32000) begin $display("ERROR: HS period"); errors = errors + 1; end
		if (hs_per_vs != 525)   begin $display("ERROR: lines per VGA frame"); errors = errors + 1; end

		// VGA reads the frame buffer: pixel (2x, 2y) on screen shows fb(x, y)
		if (errors == 0) $display("ALL CHECKS PASSED");
		else             $display("%0d CHECK(S) FAILED", errors);
		$finish;
	end

	initial begin #200_000_000; $display("TIMEOUT"); $finish; end

endmodule
