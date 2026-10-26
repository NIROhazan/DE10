// Written by run.bat - do not edit.
//   Y = (A + B)(A' + C)
module equation(
	input  [3:0] A,
	input  [3:0] B,
	input  [3:0] C,
	output [3:0] Y
	);
	assign Y = ((A | B)) & (((~A) | C));
endmodule
