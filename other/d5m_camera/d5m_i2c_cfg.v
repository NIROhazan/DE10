// d5m_i2c_cfg.v - writes the TRDB-D5M (MT9P001) registers over I2C.
//
// Every write is 4 bytes: device address 0xBA, register, data[15:8], data[7:0].
// First the fixed table below, then it keeps watching two live settings and
// rewrites them whenever they change: exposure (R0x09) and the sensor's own
// test pattern (R0xA0).  A missing acknowledge sets nack and retries the write.
//
// SCL is driven push-pull; SDA is open drain (0 or Z, pulled up on the D5M).
module d5m_i2c_cfg #(
	parameter CLK_HZ = 50_000_000,
	parameter I2C_HZ = 50_000
)(
	input             clk,
	input             rst_n,        // low = start over
	input      [15:0] exposure,     // R0x09 shutter width, in rows
	input             test_pat,     // 1 = sensor sends colour bars
	output reg        scl,
	inout             sda,
	output reg        done,         // table written and live settings up to date
	output reg        nack          // some write was not acknowledged (sticky)
);

	// ---- quarter-bit tick: each SCL period is 4 ticks ----
	localparam QDIV = CLK_HZ / (4 * I2C_HZ);
	reg [15:0] qcnt;
	wire       tick = (qcnt == QDIV - 1);
	always @(posedge clk)
		if (!rst_n || tick) qcnt <= 0;
		else                qcnt <= qcnt + 1'b1;

	// ---- fixed register table {register, value} ----
	// Values from Terasic's D5M camera demo (640x480 mode), with the sensor PLL
	// left off: PIXCLK = XCLKIN = 25 MHz.  Output: 1280 x 960 Bayer pixels
	// (2x bin + 2x skip of a 2560 x 1920 window).
	localparam N = 16;
	reg [4:0]  idx;
	reg [23:0] entry;
	always @(*)
		case (idx)
			5'd0:  entry = 24'h20_C000;   // mirror rows and columns
			5'd1:  entry = 24'h05_0000;   // horizontal blanking
			5'd2:  entry = 24'h06_0019;   // vertical blanking
			5'd3:  entry = 24'h0A_8000;   // invert PIXCLK: data stable on its rising edge
			5'd4:  entry = 24'h2B_0013;   // green 1 gain
			5'd5:  entry = 24'h2C_009A;   // blue gain
			5'd6:  entry = 24'h2D_019C;   // red gain
			5'd7:  entry = 24'h2E_0013;   // green 2 gain
			5'd8:  entry = 24'h98_0000;   // disable calibration
			5'd9:  entry = 24'hA0_0000;   // test pattern off
			5'd10: entry = 24'h01_0000;   // start row
			5'd11: entry = 24'h02_0000;   // start column
			5'd12: entry = 24'h03_077F;   // row size    - 1 = 1919
			5'd13: entry = 24'h04_09FF;   // column size - 1 = 2559
			5'd14: entry = 24'h22_0011;   // row mode:    2x bin, 2x skip
			5'd15: entry = 24'h23_0011;   // column mode: 2x bin, 2x skip
			default: entry = 24'h49_01A8; // row black target
		endcase

	// ---- the live settings, as last written ----
	reg [15:0] exp_w;     // 0 = never written (exposure is never 0)
	reg        tp_w;      // the table writes A0 = 0
	reg [15:0] exp_p;     // value being written now
	reg        tp_p;
	reg [1:0]  kind;      // 0 table, 1 exposure, 2 test pattern

	// ---- bit engine ----
	localparam S_IDLE = 3'd0, S_START = 3'd1, S_BIT = 3'd2, S_STOP = 3'd3, S_NEXT = 3'd4;
	reg [2:0]  st;
	reg [1:0]  q;         // quarter of the current bit
	reg [31:0] sh;        // bytes still to send, MSB first
	reg [3:0]  bitn;      // 8..1 data bits, 0 = acknowledge
	reg [1:0]  bytn;      // which of the 4 bytes
	reg        err;       // this write got a NACK
	reg        sda_o;     // 1 = release, 0 = pull low
	assign sda = sda_o ? 1'bz : 1'b0;

	always @(posedge clk) begin
		if (!rst_n) begin
			st <= S_IDLE; q <= 0; scl <= 1'b1; sda_o <= 1'b1;
			idx <= 0; exp_w <= 0; tp_w <= 0; done <= 0; nack <= 0;
			kind <= 0; err <= 0; sh <= 0; bitn <= 0; bytn <= 0; exp_p <= 0; tp_p <= 0;
		end else if (tick) begin
			case (st)
			S_IDLE: begin
				scl <= 1'b1; sda_o <= 1'b1; q <= 0; err <= 0;
				if (idx <= N) begin
					sh <= {8'hBA, entry}; kind <= 2'd0; st <= S_START; done <= 0;
				end else if (exposure != exp_w) begin
					exp_p <= exposure;
					sh <= {8'hBA, 8'h09, exposure}; kind <= 2'd1; st <= S_START; done <= 0;
				end else if (test_pat != tp_w) begin
					tp_p <= test_pat;
					// R0xA0: bit 0 enable, bits 6:3 mode (8 = vertical colour bars)
					sh <= {8'hBA, 8'hA0, test_pat ? 16'h0041 : 16'h0000}; kind <= 2'd2;
					st <= S_START; done <= 0;
				end else
					done <= 1'b1;
			end
			S_START: begin                    // SDA falls while SCL is high
				case (q)
					2'd0: begin scl <= 1'b1; sda_o <= 1'b1; end
					2'd1: begin scl <= 1'b1; sda_o <= 1'b0; end
					2'd2: begin scl <= 1'b0; sda_o <= 1'b0; end
					2'd3: begin st <= S_BIT; bitn <= 4'd8; bytn <= 0; end
				endcase
				q <= q + 1'b1;
			end
			S_BIT: begin
				case (q)
					2'd0: begin scl <= 1'b0; sda_o <= (bitn == 0) ? 1'b1 : sh[31]; end
					2'd1: scl <= 1'b1;
					2'd2: if (bitn == 0 && sda) err <= 1'b1;   // SDA still high: no ACK
					2'd3: begin
						scl <= 1'b0;
						if (bitn != 0) begin
							sh <= {sh[30:0], 1'b0};
							bitn <= bitn - 1'b1;
						end else if (bytn == 2'd3)
							st <= S_STOP;
						else begin
							bytn <= bytn + 1'b1;
							bitn <= 4'd8;
						end
					end
				endcase
				q <= q + 1'b1;
			end
			S_STOP: begin                     // SDA rises while SCL is high
				case (q)
					2'd0: begin scl <= 1'b0; sda_o <= 1'b0; end
					2'd1: begin scl <= 1'b1; sda_o <= 1'b0; end
					2'd2: begin scl <= 1'b1; sda_o <= 1'b1; end
					2'd3: st <= S_NEXT;
				endcase
				q <= q + 1'b1;
			end
			S_NEXT: begin
				if (err)
					nack <= 1'b1;             // retry the same write
				else case (kind)
					2'd0: idx   <= idx + 1'b1;
					2'd1: exp_w <= exp_p;
					default: tp_w <= tp_p;
				endcase
				st <= S_IDLE;
			end
			default: st <= S_IDLE;
			endcase
		end
	end

endmodule
