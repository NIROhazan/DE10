// ex6 board - Terasic DE1 (Cyclone II EP2C20F484C7). Instructor source: students get only board.sof.
// A = SW0, B = SW1, C = SW2, puzzle = SW9..SW6 (HEX0). Y of the hidden CMOS gate on LEDG0 and HEX3.
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

	reg Y;
	always @(*) case ({SW[9:6], SW[2:0]})
		7'd0: Y = 1'b1;
		7'd1: Y = 1'b0;
		7'd2: Y = 1'b1;
		7'd3: Y = 1'b0;
		7'd4: Y = 1'b1;
		7'd5: Y = 1'b0;
		7'd6: Y = 1'b0;
		7'd7: Y = 1'b0;
		7'd8: Y = 1'b1;
		7'd9: Y = 1'b0;
		7'd10: Y = 1'b1;
		7'd11: Y = 1'b0;
		7'd12: Y = 1'b0;
		7'd13: Y = 1'b0;
		7'd14: Y = 1'b0;
		7'd15: Y = 1'b0;
		7'd16: Y = 1'b1;
		7'd17: Y = 1'b0;
		7'd18: Y = 1'b0;
		7'd19: Y = 1'b0;
		7'd20: Y = 1'b0;
		7'd21: Y = 1'b0;
		7'd22: Y = 1'b0;
		7'd23: Y = 1'b0;
		7'd24: Y = 1'b1;
		7'd25: Y = 1'b1;
		7'd26: Y = 1'b1;
		7'd27: Y = 1'b1;
		7'd28: Y = 1'b1;
		7'd29: Y = 1'b1;
		7'd30: Y = 1'b1;
		7'd31: Y = 1'b0;
		7'd32: Y = 1'b0;
		7'd33: Y = 1'b0;
		7'd34: Y = 1'b0;
		7'd35: Y = 1'b1;
		7'd36: Y = 1'b0;
		7'd37: Y = 1'b0;
		7'd38: Y = 1'b0;
		7'd39: Y = 1'b1;
		7'd40: Y = 1'b1;
		7'd41: Y = 1'b1;
		7'd42: Y = 1'b1;
		7'd43: Y = 1'b1;
		7'd44: Y = 1'b1;
		7'd45: Y = 1'b0;
		7'd46: Y = 1'b1;
		7'd47: Y = 1'b0;
		7'd48: Y = 1'b1;
		7'd49: Y = 1'b0;
		7'd50: Y = 1'b0;
		7'd51: Y = 1'b0;
		7'd52: Y = 1'b0;
		7'd53: Y = 1'b0;
		7'd54: Y = 1'b0;
		7'd55: Y = 1'b0;
		7'd56: Y = 1'b1;
		7'd57: Y = 1'b1;
		7'd58: Y = 1'b0;
		7'd59: Y = 1'b0;
		7'd60: Y = 1'b0;
		7'd61: Y = 1'b0;
		7'd62: Y = 1'b0;
		7'd63: Y = 1'b0;
		7'd64: Y = 1'b1;
		7'd65: Y = 1'b1;
		7'd66: Y = 1'b1;
		7'd67: Y = 1'b1;
		7'd68: Y = 1'b1;
		7'd69: Y = 1'b0;
		7'd70: Y = 1'b0;
		7'd71: Y = 1'b0;
		7'd72: Y = 1'b0;
		7'd73: Y = 1'b1;
		7'd74: Y = 1'b0;
		7'd75: Y = 1'b1;
		7'd76: Y = 1'b1;
		7'd77: Y = 1'b1;
		7'd78: Y = 1'b1;
		7'd79: Y = 1'b1;
		7'd80: Y = 1'b1;
		7'd81: Y = 1'b1;
		7'd82: Y = 1'b1;
		7'd83: Y = 1'b1;
		7'd84: Y = 1'b1;
		7'd85: Y = 1'b1;
		7'd86: Y = 1'b1;
		7'd87: Y = 1'b0;
		7'd88: Y = 1'b1;
		7'd89: Y = 1'b1;
		7'd90: Y = 1'b0;
		7'd91: Y = 1'b0;
		7'd92: Y = 1'b1;
		7'd93: Y = 1'b1;
		7'd94: Y = 1'b0;
		7'd95: Y = 1'b0;
		7'd96: Y = 1'b0;
		7'd97: Y = 1'b1;
		7'd98: Y = 1'b0;
		7'd99: Y = 1'b1;
		7'd100: Y = 1'b1;
		7'd101: Y = 1'b1;
		7'd102: Y = 1'b1;
		7'd103: Y = 1'b1;
		7'd104: Y = 1'b1;
		7'd105: Y = 1'b0;
		7'd106: Y = 1'b1;
		7'd107: Y = 1'b0;
		7'd108: Y = 1'b1;
		7'd109: Y = 1'b0;
		7'd110: Y = 1'b0;
		7'd111: Y = 1'b0;
		7'd112: Y = 1'b1;
		7'd113: Y = 1'b1;
		7'd114: Y = 1'b1;
		7'd115: Y = 1'b1;
		7'd116: Y = 1'b1;
		7'd117: Y = 1'b1;
		7'd118: Y = 1'b0;
		7'd119: Y = 1'b0;
		7'd120: Y = 1'b1;
		7'd121: Y = 1'b1;
		7'd122: Y = 1'b1;
		7'd123: Y = 1'b0;
		7'd124: Y = 1'b1;
		7'd125: Y = 1'b0;
		7'd126: Y = 1'b1;
		7'd127: Y = 1'b0;
		default: Y = 1'b0;
	endcase
	hex7seg d0(.x(SW[9:6]), .seg(HEX0));
	hex7seg d3(.x({3'b000, Y}), .seg(HEX3));
	assign HEX1 = 7'b1111111;
	assign HEX2 = 7'b1111111;
	assign LEDR = SW;
	assign LEDG = {7'b0000000, Y};
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
