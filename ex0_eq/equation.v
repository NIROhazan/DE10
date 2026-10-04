// Written by run.bat from equation.txt - edit equation.txt, not this file.
//   Y = A + B*C
module equation(
	input  [3:0] A,
	input  [3:0] B,
	input  [3:0] C,
	output [3:0] Y
	);
	assign Y = A | (B & C);
endmodule
