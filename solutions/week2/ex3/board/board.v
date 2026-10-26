// ex3 board - Terasic DE1 (Cyclone II EP2C20F484C7). Instructor source: students get only board.sof.
// X = SW3..0 (HEX0), Y = SW7..4 (HEX1), S = X+Y on HEX3 and LEDG3..0, LEDG6 = carry out, LEDG7 = signed overflow.
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

	wire [3:0] X = SW[3:0], Y = SW[7:4];
	wire [4:0] T = X + Y;
	wire V = (X[3] == Y[3]) && (T[3] != X[3]);
	hex7seg d0(.x(X), .seg(HEX0));
	hex7seg d1(.x(Y), .seg(HEX1));
	hex7seg d3(.x(T[3:0]), .seg(HEX3));
	assign HEX2 = 7'b1111111;
	assign LEDR = SW;
	assign LEDG = {V, T[4], 2'b00, T[3:0]};
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
