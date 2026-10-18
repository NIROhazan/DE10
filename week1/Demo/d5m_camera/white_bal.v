// white_bal.v - one-shot white balance ("custom white balance" of a real camera).
//
// Point the camera at something white or grey and pulse start (KEY1).  For the next 3 frames the
// red and blue gains are set so the frame's average red and blue equal its average green:
//     new gain = gain * sum_g / sum_r          (the sums were measured with the old gain)
// Then the gains stay fixed until the next press, so the picture cannot hunt or flicker.
// Gains: 64 = x1, from 16 (x0.25) to 255 (x4).  clear = back to R0 / B0.
module white_bal #(
	parameter [7:0] R0 = 8'd64,     // gains after clear
	parameter [7:0] B0 = 8'd64
)(
	input             clk,
	input             clear,
	input             start,
	input             frame_end,    // sums below are new
	input      [28:0] sum_r,        // last frame, red after its gain
	input      [28:0] sum_g,
	input      [28:0] sum_b,
	output reg [7:0]  gain_r = 8'd64,
	output reg [7:0]  gain_b = 8'd64,
	output            busy
);
	reg [1:0]  left = 0;            // frames still to use
	reg [1:0]  st = 0;              // 0 idle, 1 dividing for red, 2 dividing for blue
	reg [36:0] num;                 // gain * sum_g
	reg [28:0] den;
	reg [36:0] q;
	reg [29:0] rem;
	reg [5:0]  n;
	assign busy = (left != 0) || (st != 0);

	// one bit of a restoring division per clock: 37 clocks per gain
	wire [29:0] trial = {rem[28:0], num[36]};
	wire        fits  = trial >= {1'b0, den};
	wire [7:0]  qclip = (q[36:8] != 0) ? 8'd255 : (q[7:0] < 8'd16) ? 8'd16 : q[7:0];

	always @(posedge clk) begin
		if (clear) begin
			gain_r <= R0; gain_b <= B0; left <= 0; st <= 0;
		end else begin
			if (start) left <= 2'd3;
			case (st)
				2'd0: if (frame_end && left != 0 && !start && sum_r != 0 && sum_b != 0) begin
					num <= sum_g * gain_r;  den <= sum_r;  q <= 0;  rem <= 0;  n <= 6'd37;
					st <= 2'd1;  left <= left - 1'b1;
				end
				default: if (n != 0) begin
					rem <= fits ? trial - {1'b0, den} : trial;
					q   <= {q[35:0], fits};
					num <= {num[35:0], 1'b0};
					n   <= n - 1'b1;
				end else if (st == 2'd1) begin
					gain_r <= qclip;
					num <= sum_g * gain_b;  den <= sum_b;  q <= 0;  rem <= 0;  n <= 6'd37;
					st <= 2'd2;
				end else begin
					gain_b <= qclip;
					st <= 2'd0;
				end
			endcase
		end
	end
endmodule
