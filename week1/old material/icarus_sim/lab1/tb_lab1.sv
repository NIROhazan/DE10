`timescale 1ns/1ps
module tb_lab1;
    logic clk = 0;
    logic [9:0] SW = '0;
    logic [1:0] KEY = 2'b11;
    logic [9:0] LEDR;
    logic [7:0] HEX0, HEX1, HEX2, HEX3, HEX4, HEX5;
    int errors = 0;

    lab1_top #(.TICK_DIV(8)) dut (.MAX10_CLK1_50(clk), .*);
    always #10 clk = ~clk;

    function automatic string ch(input logic [7:0] s);
        string c;
        case (s | 8'h80)
            8'hFF: c = " ";         8'hBF: c = "-";
            8'hC0: c = "0";  8'hF9: c = "1";  8'hA4: c = "2";  8'hB0: c = "3";
            8'h99: c = "4";  8'h92: c = "5";  8'h82: c = "6";  8'hF8: c = "7";
            8'h80: c = "8";  8'h90: c = "9";
            8'hC7: c = "L";  8'hC6: c = "C";  8'h8C: c = "P";  8'h86: c = "E";
            8'hAB: c = "n";  8'hA1: c = "d";  8'h88: c = "A";  8'h83: c = "b";  8'h8E: c = "F";
            default: c = "?";
        endcase
        if (!s[7]) c = {c, "."};
        return c;
    endfunction

    // O and 0, S and 5 look identical on a 7-segment digit, so they decode as 0 and 5.
    function automatic string show();
        return {ch(HEX5), ch(HEX4), ch(HEX3), ch(HEX2), ch(HEX1), ch(HEX0)};
    endfunction

    task automatic expect_hex(input string what, input string want);
        #1;
        if (show() != want) begin
            $display("FAIL %-28s got [%s] want [%s]", what, show(), want);
            errors++;
        end else $display("ok   %-28s [%s]", what, show());
    endtask

    task automatic expect_led(input string what, input logic [9:0] want);
        #1;
        if (LEDR !== want) begin
            $display("FAIL %-28s LEDR %b want %b", what, LEDR, want);
            errors++;
        end else $display("ok   %-28s LEDR %b", what, LEDR);
    endtask

    task automatic card(input int n, input logic [6:0] xval = 0);
        SW = {3'(n - 1), xval};
    endtask

    task automatic press(input int key, input int cycles = 4);
        KEY[key] = 0;
        repeat (cycles) @(posedge clk);
        KEY[key] = 1;
        repeat (4) @(posedge clk);
    endtask

    task automatic wait_tick();
        do @(posedge clk); while (!dut.tick);
        @(posedge clk);
    endtask

    initial begin
        // warm-up: set the switches to ten
        SW = 10'd10;          expect_hex("warmup ten",        "     A");
                              expect_led("warmup lights",     10'b0000001010);
        SW = 10'b0000010000;  expect_hex("warmup '10' is 16", "    10");
        SW = 10'h3FF;         expect_hex("warmup all on",     "   3FF");
        SW = 10'b1000000000;  expect_hex("warmup SW9",        "   200");
        press(0); press(1);   expect_hex("warmup one key at a time stays", "   200");
        KEY = 2'b00; repeat (4) @(posedge clk); KEY = 2'b11; repeat (4) @(posedge clk);
        if (dut.warmup) begin $display("FAIL warmup should end on both keys"); errors++; end
        else $display("ok   warmup ended on both keys");

        // card 1: +1
        card(1, 7'd5);   expect_hex("card1 5+1",      "  5  6");
        card(1, 7'd63);  expect_hex("card1 63+1",     " 63-64");
        card(1, 7'd64);  expect_hex("card1 SW6 alone","-64-63");

        // card 2: moving lights
        card(2, 7'd40);  expect_hex("card2 40/8",     " 40  5");
                         expect_led("card2 40/8 lights", 10'b0000000101);
        KEY[0] = 0;      expect_hex("card2 40/6",     " 40  6");
        KEY[0] = 1;
        KEY[1] = 0;      expect_hex("card2 40x2",     " 40 80");
                         expect_led("card2 40x2 lights", 10'b0001010000);
        card(2, 7'd100); expect_hex("card2 100x2",    "100200");
        KEY[1] = 1;

        // card 3: squeeze into 4 bits
        card(3, 7'd7);   expect_hex("card3 7",        "  7  7");
        card(3, 7'd8);   expect_hex("card3 8",        "  8 -8");
        card(3, 7'd20);  expect_hex("card3 20",       " 20  4");

        // card 4: SR latch (never release both keys in the same instant: zero-delay loop)
        card(4);
        KEY[0] = 0; #5 KEY[0] = 1;  expect_led("card4 after off",   10'b0000000100);
        KEY[1] = 0; #5;             expect_led("card4 holding on",  10'b0000000011);
        KEY[1] = 1;                 expect_led("card4 released",    10'b0000000001);
        KEY = 2'b00; #5;            expect_led("card4 both pressed",10'b0000000010);
        KEY[0] = 1; #5 KEY[1] = 1;  expect_led("card4 release on last", 10'b0000000001);

        // card 5: turnstile
        repeat (4) @(posedge clk);                        // let card 4's key presses settle
        card(5); repeat (2) @(posedge clk);
        expect_hex("card5 start", "L0C  0");
        press(0);           expect_hex("card5 push while locked", "L0C  0");
        press(1);           expect_hex("card5 coin",   "0PEn 0");
                            expect_led("card5 1 coin", 10'b0000000001);
        press(1);           expect_led("card5 2 coins", 10'b0000000011);
        press(0);           expect_hex("card5 walk",   "L0C  1");
                            expect_led("card5 coins cleared", 10'b0000000000);
        press(0);           expect_hex("card5 walk again, no coin", "L0C  1");

        // card 6: instant (Mealy) vs late (Moore)
        card(6);
        wait_tick(); repeat (2) @(posedge clk);
        KEY[0] = 0; repeat (3) @(posedge clk);
        #1 if (LEDR[0] !== 1 || LEDR[1] !== 0) begin $display("FAIL card6 press: instant on, late off, LEDR %b", LEDR); errors++; end
           else $display("ok   card6 press: instant on, late still off");
        wait_tick();
        #1 if (LEDR[0] !== 0 || LEDR[1] !== 1) begin $display("FAIL card6 tick: instant off, late on, LEDR %b", LEDR); errors++; end
           else $display("ok   card6 tick while held: instant off, late on");
        wait_tick();
        #1 if (LEDR[1] !== 0) begin $display("FAIL card6 late light lasts one tick"); errors++; end
           else $display("ok   card6 late light lasted one tick");
        KEY[0] = 1; wait_tick();
        KEY[0] = 0; repeat (3) @(posedge clk);            // short press between ticks
        #1 if (LEDR[0] !== 1) begin $display("FAIL card6 short press instant"); errors++; end
        KEY[0] = 1; wait_tick();
        #1 if (LEDR[1] !== 0) begin $display("FAIL card6 short press should be missed"); errors++; end
           else $display("ok   card6 short press: instant flashed, late missed it");

        // card 7: placeholder
        card(7); expect_hex("card7 placeholder", "5PEEd ");

        // card 8: x 0.1 / x 0.25
        card(8, 7'd10);  expect_hex("card8 10 x 0.1",  "100.976");
        card(8, 7'd1);   expect_hex("card8 1 x 0.1",   " 10.097");
        KEY[0] = 0;
        card(8, 7'd4);   expect_hex("card8 4 x 0.25",  " 41.000");
        KEY[0] = 1;

        if (errors) $display("%0d FAILURES", errors); else $display("ALL PASSED");
        $finish;
    end
endmodule
