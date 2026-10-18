// frame_ram.v - 320 x 240 x 16-bit frame buffer in on-chip memory (M9K).
// Port A (camera clock): read or write at addr_a.  Port B (VGA clock): read.
// The camera side reads too, for the event camera (each word holds that pixel's reference).
// 76800 x 16 = 1,228,800 bits = 160 of the 10M50's 182 M9K blocks (8K x 1 each, 10 deep x 16 wide).
module frame_ram(
	input             wclk,
	input             we,
	input      [16:0] waddr,        // port A address, for the write or the read
	input      [15:0] wdata,
	output reg [15:0] wq,           // port A read data, one clock after waddr
	input             rclk,
	input      [16:0] raddr,
	output reg [15:0] rdata
);
	(* ramstyle = "M9K, no_rw_check" *) reg [15:0] mem [0:76799];

	always @(posedge wclk)
		if (we) begin
			mem[waddr] <= wdata;
			wq <= wdata;
		end else
			wq <= mem[waddr];

	always @(posedge rclk)
		rdata <= mem[raddr];
endmodule
