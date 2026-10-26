// ex1 board - Terasic DE1 (Cyclone II EP2C20F484C7). Instructor source: students get only board.sof.
// N = SW9..0 on LEDR and in hex on HEX2..0. KEY3 held: secret byte of puzzle SW5..0 on LEDG7..0.
module board(
	input  [9:0] SW,
	input  [3:0] KEY,
	output [9:0] LEDR,
	output [7:0] LEDG,
	output [6:0] HEX0,
	output [6:0] HEX1,
	output [6:0] HEX2,
	output [6:0] HEX3
	);

	wire secret = ~KEY[3];
	reg [7:0] S;
	always @(*) case (SW[5:0])
		6'd0: S = 8'h8E;
		6'd1: S = 8'h24;
		6'd2: S = 8'hBC;
		6'd3: S = 8'h59;
		6'd4: S = 8'hFA;
		6'd5: S = 8'h59;
		6'd6: S = 8'h92;
		6'd7: S = 8'h42;
		6'd8: S = 8'hD8;
		6'd9: S = 8'h9F;
		6'd10: S = 8'h4B;
		6'd11: S = 8'h96;
		6'd12: S = 8'hB0;
		6'd13: S = 8'h96;
		6'd14: S = 8'hC5;
		6'd15: S = 8'h9B;
		6'd16: S = 8'hEC;
		6'd17: S = 8'hD1;
		6'd18: S = 8'hD2;
		6'd19: S = 8'h18;
		6'd20: S = 8'h2B;
		6'd21: S = 8'h12;
		6'd22: S = 8'h4C;
		6'd23: S = 8'h2D;
		6'd24: S = 8'h24;
		6'd25: S = 8'hCD;
		6'd26: S = 8'h51;
		6'd27: S = 8'h86;
		6'd28: S = 8'hA3;
		6'd29: S = 8'h7D;
		6'd30: S = 8'h6E;
		6'd31: S = 8'hF0;
		6'd32: S = 8'h47;
		6'd33: S = 8'h11;
		6'd34: S = 8'h25;
		6'd35: S = 8'h39;
		6'd36: S = 8'h8F;
		6'd37: S = 8'h32;
		6'd38: S = 8'h46;
		6'd39: S = 8'h30;
		6'd40: S = 8'h3A;
		6'd41: S = 8'hCB;
		6'd42: S = 8'hB5;
		6'd43: S = 8'h85;
		6'd44: S = 8'h1F;
		6'd45: S = 8'h17;
		6'd46: S = 8'hBA;
		6'd47: S = 8'h28;
		6'd48: S = 8'hC6;
		6'd49: S = 8'h7F;
		6'd50: S = 8'h20;
		6'd51: S = 8'h3E;
		6'd52: S = 8'h55;
		6'd53: S = 8'h2F;
		6'd54: S = 8'h73;
		6'd55: S = 8'h8C;
		6'd56: S = 8'h4A;
		6'd57: S = 8'h38;
		6'd58: S = 8'hFB;
		6'd59: S = 8'h6B;
		6'd60: S = 8'h4A;
		6'd61: S = 8'h19;
		6'd62: S = 8'h92;
		6'd63: S = 8'hF2;
		default: S = 8'h00;
	endcase
	wire [6:0] h0, h1, h2;
	hex7seg d0(.x(SW[3:0]), .seg(h0));
	hex7seg d1(.x(SW[7:4]), .seg(h1));
	hex7seg d2(.x({2'b00, SW[9:8]}), .seg(h2));
	assign LEDR = SW;
	assign LEDG = secret ? S : 8'h00;
	assign HEX0 = secret ? 7'b0111111 : h0;
	assign HEX1 = secret ? 7'b0111111 : h1;
	assign HEX2 = secret ? 7'b0111111 : h2;
	assign HEX3 = secret ? 7'b0111111 : 7'b1111111;
endmodule

// Hex digit to 7-segment, active low, seg[6:0] = g f e d c b a
module hex7seg(input [3:0] x, output reg [6:0] seg);
	always @(*) case (x)
		4'h0: seg = 7'b1000000;
		4'h1: seg = 7'b1111001;
		4'h2: seg = 7'b0100100;
		4'h3: seg = 7'b0110000;
		4'h4: seg = 7'b0011001;
		4'h5: seg = 7'b0010010;
		4'h6: seg = 7'b0000010;
		4'h7: seg = 7'b1111000;
		4'h8: seg = 7'b0000000;
		4'h9: seg = 7'b0010000;
		4'hA: seg = 7'b0001000;
		4'hB: seg = 7'b0000011;
		4'hC: seg = 7'b1000110;
		4'hD: seg = 7'b0100001;
		4'hE: seg = 7'b0000110;
		4'hF: seg = 7'b0001110;
		default: seg = 7'b1111111;
	endcase
endmodule
