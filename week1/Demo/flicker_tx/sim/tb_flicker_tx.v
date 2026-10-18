// tb_flicker_tx.v - the LEDs must blink at exactly SW Hz (period measured over 3 cycles, within
// 0.01 %), 50 % duty, HEX showing the number; KEY0 = steady on, KEY1 = off.
// Run: iverilog -g2005 -o tx.vvp tb_flicker_tx.v ../flicker_tx.v && vvp -n tx.vvp
`timescale 1ns/1ps
module tb_flicker_tx;
	reg clk = 0;  always #10 clk = ~clk;
	reg [9:0] SW = 10'd100;
	reg [1:0] KEY = 2'b11;
	wire [9:0] LEDR;
	wire [7:0] HEX0, HEX1, HEX2, HEX3, HEX4, HEX5;
	flicker_tx dut(.MAX10_CLK1_50(clk), .KEY(KEY), .SW(SW), .LEDR(LEDR),
	               .HEX0(HEX0), .HEX1(HEX1), .HEX2(HEX2), .HEX3(HEX3), .HEX4(HEX4), .HEX5(HEX5));

	integer errors = 0;
	realtime t0, t1, t3, ton;
	task measure(input integer f);
		real want, per, duty;
		begin
			SW = f;
			@(posedge LEDR[0]); @(posedge LEDR[0]);          // let it settle
			t0 = $realtime;  @(negedge LEDR[0]);  ton = $realtime - t0;
			@(posedge LEDR[0]); t1 = $realtime;
			@(posedge LEDR[0]); @(posedge LEDR[0]); t3 = $realtime;
			per  = (t3 - t0) / 3.0;
			want = 1e9 / f;
			duty = ton / per;
			$display("SW = %4d: period %0.1f ns (want %0.1f), %0.4f Hz, duty %0.3f", f, per, want, 1e9 / per, duty);
			if (per < want * 0.9999 || per > want * 1.0001) begin $display("ERROR: frequency"); errors = errors + 1; end
			if (duty < 0.49 || duty > 0.51) begin $display("ERROR: duty"); errors = errors + 1; end
		end
	endtask

	initial begin
		measure(100);
		@(posedge LEDR[0]); #100;
		$display("HEX5..0 while on: %h %h %h %h %h %h (want 00 00 00 79 40 40 = 8. 8. 8. 1. 0. 0.)", HEX5, HEX4, HEX3, HEX2, HEX1, HEX0);
		if (HEX5 !== 8'h00 || HEX4 !== 8'h00 || HEX3 !== 8'h00 || HEX2 !== 8'h79 || HEX1 !== 8'h40 || HEX0 !== 8'h40)
			begin $display("ERROR: HEX should read 8. 8. 8. 1. 0. 0."); errors = errors + 1; end
		@(negedge LEDR[0]); #100;
		if ({HEX5, HEX4, HEX3, HEX2, HEX1, HEX0} !== 48'hFFFF_FFFF_FFFF) begin $display("ERROR: HEX should be dark while off"); errors = errors + 1; end
		measure(137);
		measure(1000);
		KEY = 2'b10;  #2_000_000;
		if (LEDR !== 10'h3FF) begin $display("ERROR: KEY0 should give steady on"); errors = errors + 1; end
		KEY = 2'b01;  #1000;
		if (LEDR !== 10'h000) begin $display("ERROR: KEY1 should give off"); errors = errors + 1; end
		if (errors == 0) $display("ALL CHECKS PASSED"); else $display("%0d CHECK(S) FAILED", errors);
		$finish;
	end
endmodule
