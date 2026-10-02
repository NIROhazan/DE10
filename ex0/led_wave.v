// ============================================================
// led_wave.v  -  Digital Systems, Week 1 demo
// Target: Terasic DE10-Lite (MAX 10, 50 MHz clock); on the DE1 it runs via ex0_top.v (CLOCK_50)
//
// A smooth hump of light travels left to right across the
// 10 red LEDs and wraps around forever.
//   - 10 independent PWM channels, one per LED, in parallel
//   - Brightness: 99% peak, then 60%, 30%, 10%, off
//   - One step every 300 ms
//
// Pin mapping (System Builder names):
//   MAX10_CLK1_50 -> clk
//   LEDR[9:0]     -> LEDR   (LEDR[9] is leftmost, LEDR[0] rightmost)
// ============================================================
module led_wave #(
    parameter PWM_DIV  = 500,       // 50 MHz / 500 = 100 kHz tick -> 1 kHz PWM
    parameter MOVE_DIV = 15000000   // 50 MHz / 15M = one step every 300 ms
)(
    input  wire       clk,
    output reg  [9:0] LEDR
);

    // ---- fast PWM counter (0..99) ----
    reg [6:0]  pwm_cnt = 0;
    reg [19:0] pwm_div = 0;
    always @(posedge clk) begin
        if (pwm_div == PWM_DIV - 1) begin
            pwm_div <= 0;
            pwm_cnt <= (pwm_cnt == 7'd99) ? 7'd0 : pwm_cnt + 1'b1;
        end else
            pwm_div <= pwm_div + 1'b1;
    end

    // ---- brightness by distance from the peak ----
    function [6:0] hump;
        input [3:0] dist;
        case (dist)
            4'd0:    hump = 7'd99;
            4'd1:    hump = 7'd60;
            4'd2:    hump = 7'd30;
            4'd3:    hump = 7'd10;
            default: hump = 7'd0;
        endcase
    endfunction

    // ---- circular distance on a ring of 10 LEDs ----
    function [3:0] ring_dist;
        input [3:0] a, b;
        reg   [3:0] d;
        begin
            d = (a > b) ? (a - b) : (b - a);
            ring_dist = (d > 4'd5) ? (4'd10 - d) : d;
        end
    endfunction

    // ---- slow counter: moves the peak left -> right ----
    // LEDR[9] is the leftmost LED, so the peak counts down.
    reg [3:0]  peak     = 4'd9;
    reg [24:0] move_div = 0;
    always @(posedge clk) begin
        if (move_div == MOVE_DIV - 1) begin
            move_div <= 0;
            peak <= (peak == 4'd0) ? 4'd9 : peak - 1'b1;
        end else
            move_div <= move_div + 1'b1;
    end

    // ---- ten PWM comparators running in parallel ----
    integer i;
    always @(*) begin
        for (i = 0; i < 10; i = i + 1)
            LEDR[i] = (pwm_cnt < hump(ring_dist(i[3:0], peak)));
    end

endmodule
