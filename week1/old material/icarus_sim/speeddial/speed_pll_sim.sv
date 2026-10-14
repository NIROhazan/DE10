// Simulation-only stand-in for speed_pll (Intel's altpll cannot run in Icarus).
// Do NOT add this file to the Quartus project.
`timescale 1ns/1ps
module speed_pll (
    input  wire       inclk0,
    output logic [4:0] c = '0,
    output logic       locked = 1'b0
);
    always #50.000 c[0] = ~c[0];   //  10 MHz
    always #20.000 c[1] = ~c[1];   //  25 MHz
    always #5.000  c[2] = ~c[2];   // 100 MHz
    always #2.500  c[3] = ~c[3];   // 200 MHz
    always #1.667  c[4] = ~c[4];   // 300 MHz
    initial #500 locked = 1'b1;
endmodule
