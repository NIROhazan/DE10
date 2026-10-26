// ex4 board - Terasic DE1 (Cyclone II EP2C20F484C7). Instructor source: students get only board.sof.
// X = SW3..0 (HEX0). E = X extended to 8 bits on HEX3..HEX2 and LEDG7..0: sign-extension, or zero-extension while SW9 is up.
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

	wire [3:0] X = SW[3:0];
	wire [7:0] E = SW[9] ? {4'b0000, X} : {{4{X[3]}}, X};
	hex7seg d0(.x(X), .seg(HEX0));
	hex7seg d2(.x(E[3:0]), .seg(HEX2));
	hex7seg d3(.x(E[7:4]), .seg(HEX3));
	assign HEX1 = 7'b1111111;
	assign LEDR = SW;
	assign LEDG = E;
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
