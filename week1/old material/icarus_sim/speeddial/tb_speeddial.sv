`timescale 1ns/1ps
// Compile with -DSIM and speed_pll_sim.sv (not speed_pll.v).
// Each operation is given a pretend delay: 8-bit add 2 ns, 64-bit add 4 ns, multiply 8 ns,
// divide 15 ns. An operation must show 0% wrong when the clock period is longer than its
// delay, and >0% when the clock is faster.
module tb_speeddial;
    logic clk = 0;
    logic [9:0] SW = '0;
    logic [1:0] KEY = 2'b11;
    logic [9:0] LEDR;
    logic [7:0] HEX0, HEX1, HEX2, HEX3, HEX4, HEX5;
    int errors = 0;

    speeddial_top #(.WINDOW(50), .SIM_D0(2), .SIM_D1(4), .SIM_D2(8), .SIM_D3(15))
        dut (.MAX10_CLK1_50(clk), .*);
    always #10 clk = ~clk;

    function automatic string ch(input logic [7:0] s);
        case (s)
            8'hFF: return " ";  8'hBF: return "-";
            8'hC0: return "0";  8'hF9: return "1";  8'hA4: return "2";  8'hB0: return "3";
            8'h99: return "4";  8'h92: return "5";  8'h82: return "6";  8'hF8: return "7";
            8'h80: return "8";  8'h90: return "9";
            default: return "?";
        endcase
    endfunction
    function automatic string show();
        return {ch(HEX5), ch(HEX4), ch(HEX3), ch(HEX2), ch(HEX1), ch(HEX0)};
    endfunction

    function automatic string op_name(input int op);
        case (op) 0: return "8-bit add"; 1: return "64-bit add"; 2: return "multiply"; default: return "divide"; endcase
    endfunction
    function automatic int period(input int f);       // ns, rounded
        case (f) 0: return 100; 1: return 40; 2: return 20; 3: return 10; 4: return 5; default: return 3; endcase
    endfunction
    function automatic int delay(input int op);
        case (op) 0: return 2; 1: return 4; 2: return 8; default: return 15; endcase
    endfunction

    initial begin
        #250_000;                                       // let every tester finish 2+ windows
        for (int f = 0; f < 6; f++)
            for (int op = 0; op < 4; op++) begin
                bit expect_wrong;
                SW = {5'b0, 2'(op), 3'(f)};
                repeat (4) @(posedge clk);
                #1;
                expect_wrong = delay(op) > period(f);
                if ((dut.pct_shown != 0) !== expect_wrong) begin
                    $display("FAIL %-10s @ period %3d ns: [%s] (expected %s)", op_name(op), period(f), show(),
                             expect_wrong ? "wrong answers" : "0%");
                    errors++;
                end else
                    $display("ok   %-10s @ period %3d ns: [%s]", op_name(op), period(f), show());
            end
        SW = 10'd6; repeat (4) @(posedge clk); #1
        if (show() != "---   ") begin $display("FAIL unused setting shows [%s]", show()); errors++; end
        if (errors) $display("%0d FAILURES", errors); else $display("ALL PASSED");
        $finish;
    end
endmodule
