`timescale 1ns/1ps
module tb_game;
    logic clk = 0;
    logic [9:0] SW = '0;
    logic [1:0] KEY = 2'b11;
    logic [9:0] LEDR;
    logic [7:0] HEX0, HEX1, HEX2, HEX3, HEX4, HEX5;
    int errors = 0;

    game_top #(.MS_DIV(4)) dut (.MAX10_CLK1_50(clk), .*);   // 1 "ms" = 4 clocks
    always #10 clk = ~clk;

    function automatic string ch(input logic [7:0] s);
        case (s)
            8'hFF: return " ";  8'hBF: return "-";
            8'hC0: return "0";  8'hF9: return "1";  8'hA4: return "2";  8'hB0: return "3";
            8'h99: return "4";  8'h92: return "5";  8'h82: return "6";  8'hF8: return "7";
            8'h80: return "8";  8'h90: return "9";
            8'hAF: return "r";  8'h86: return "E";  8'h88: return "A";  8'hA1: return "d";
            8'h91: return "Y";
            default: return "?";
        endcase
    endfunction
    function automatic string show();
        return {ch(HEX5), ch(HEX4), ch(HEX3), ch(HEX2), ch(HEX1), ch(HEX0)};
    endfunction
    task automatic expect_hex(input string what, input string want);
        #1 if (show() != want) begin $display("FAIL %-22s got [%s] want [%s]", what, show(), want); errors++; end
           else $display("ok   %-22s [%s]", what, show());
    endtask
    task automatic press(input int key);
        KEY[key] = 0; repeat (4) @(posedge clk); KEY[key] = 1; repeat (4) @(posedge clk);
    endtask

    initial begin
        repeat (2) @(posedge clk);
        expect_hex("ready", "rEAdY ");

        press(0);  expect_hex("waiting", "  ----");
        press(1);  expect_hex("pressed too early", "   Err");

        press(0);
        wait (dut.state == dut.GO);
        #1 if (LEDR !== '1) begin $display("FAIL go: all LEDs on"); errors++; end
           else $display("ok   go: all LEDs on");
        repeat (4 * 237) @(posedge clk);       // react after ~237 "ms"
        press(1);
        #1 if (LEDR !== '0 || show() == "      ") begin $display("FAIL result shown"); errors++; end
           else $display("ok   reaction time shown [%s] (expect ~0237-0240)", show());

        if (errors) $display("%0d FAILURES", errors); else $display("ALL PASSED");
        $finish;
    end
endmodule
