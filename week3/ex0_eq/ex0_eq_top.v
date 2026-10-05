// Exercise 0 (equation) - Terasic DE1 (Cyclone II EP2C20F484C7)
//   A = SW3..SW0  (0-F)     shown on HEX0
//   B = SW6..SW4  (0-7)     shown on HEX1
//   C = SW9..SW7  (0-7)     shown on HEX2
//   Y = your equation       shown on HEX3, and on LEDG3..LEDG0 (one LED per bit)
//   LEDR9..LEDR0 = the switches
// Do not edit: run.bat writes equation.v from equation.txt.
module ex0_eq_top(
	input  [9:0] SW,
	output [7:0] LEDG,
	output [9:0] LEDR,
	output [6:0] HEX0,
	output [6:0] HEX1,
	output [6:0] HEX2,
	output [6:0] HEX3
	);

	wire [3:0] A = SW[3:0];
	wire [3:0] B = {1'b0, SW[6:4]};
	wire [3:0] C = {1'b0, SW[9:7]};
	wire [3:0] Y;

	equation eq(.A(A), .B(B), .C(C), .Y(Y));

	assign LEDR      = SW;
	assign LEDG[3:0] = Y;
	assign LEDG[7:4] = 4'b0000;

	hex7seg h0(.x(A), .seg(HEX0));
	hex7seg h1(.x(B), .seg(HEX1));
	hex7seg h2(.x(C), .seg(HEX2));
	hex7seg h3(.x(Y), .seg(HEX3));
endmodule

// Hex digit to 7-segment, active low, seg[6:0] = g f e d c b a
module hex7seg(
	input      [3:0] x,
	output reg [6:0] seg
	);
	always @(*) begin
		case (x)
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
			default: seg = 7'b0001110;	// F
		endcase
	end
endmodule
