// Written by Claude from answer.txt - do not edit, run run.bat instead.
// SOP  = A'BC + AB'C + ABC                    (3 minterms, X rows not listed)
// POS  = (A+B+C)(A+B+C')(A+B'+C)              (3 maxterms, X rows not listed)
// MSOP = A + BC        2 terms, 3 literals, unique
// MPOS = (A+B)(C)      2 terms, 3 literals, unique
module student_logic(
	input  A,
	input  B,
	input  C,
	output SOP,
	output POS,
	output MSOP,
	output MPOS
	);
	assign SOP  = (~A & B & C) | (A & ~B & C) | (A & B & C);
	assign POS  = (A | B | C) & (A | B | ~C) & (A | ~B | C);
	assign MSOP = A | (B & C);
	assign MPOS = (A | B) & C;
endmodule
