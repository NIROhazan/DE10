// Reaction-time game, DE10-Lite. Riddle 3: the same chip, reprogrammed into a different circuit.
//
//   rEAdY  -> press KEY0 to start
//   ----   -> wait a random 1-3 s ... all LEDs light up
//   then press KEY1 as fast as you can: your time in ms appears
//   pressing KEY1 too early shows "Err"; KEY0 starts again from any state.
module game_top #(
    parameter int MS_DIV = 50_000             // 50 MHz / 50_000 = 1 ms
) (
    input  logic       MAX10_CLK1_50,
    input  logic [9:0] SW,
    input  logic [1:0] KEY,
    output logic [9:0] LEDR,
    output logic [7:0] HEX0, HEX1, HEX2, HEX3, HEX4, HEX5
);
    localparam logic [7:0] BLANK = 8'hFF, DASH = 8'b1011_1111,
                           R_ = 8'b1010_1111, E_ = 8'b1000_0110, A_ = 8'b1000_1000,
                           D_ = 8'b1010_0001, Y_ = 8'b1001_0001;

    function automatic logic [7:0] digit(input logic [3:0] d);
        case (d)
            4'd0: digit = 8'b1100_0000;  4'd1: digit = 8'b1111_1001;
            4'd2: digit = 8'b1010_0100;  4'd3: digit = 8'b1011_0000;
            4'd4: digit = 8'b1001_1001;  4'd5: digit = 8'b1001_0010;
            4'd6: digit = 8'b1000_0010;  4'd7: digit = 8'b1111_1000;
            4'd8: digit = 8'b1000_0000;  4'd9: digit = 8'b1001_0000;
            default: digit = BLANK;
        endcase
    endfunction

    logic clk;
    assign clk = MAX10_CLK1_50;

    // synchronised key presses (KEY is active-low)
    logic [1:0] k_meta = '0, k = '0, k_prev = '0, press;
    always_ff @(posedge clk) begin
        k_meta <= ~KEY;
        k      <= k_meta;
        k_prev <= k;
    end
    assign press = k & ~k_prev;

    // 1 ms tick
    logic [$clog2(MS_DIV)-1:0] div = '0;
    logic ms;
    always_ff @(posedge clk) div <= (div == MS_DIV - 1) ? '0 : div + 1'b1;
    assign ms = (div == MS_DIV - 1);

    // free-running random source; never seeded with zero
    logic [15:0] lfsr = 16'hACE1;
    always_ff @(posedge clk) lfsr <= {lfsr[14:0], lfsr[15] ^ lfsr[13] ^ lfsr[12] ^ lfsr[10]};

    typedef enum logic [2:0] {READY, WAIT, GO, SHOW, EARLY} state_t;
    state_t state = READY;
    logic [11:0] wait_ms = '0;                  // remaining random wait
    logic [13:0] t = '0;

    always_ff @(posedge clk) begin
        if (press[0]) begin                     // KEY0: (re)start
            state   <= WAIT;
            wait_ms <= 12'd1000 + (lfsr[10:0] % 12'd2000);
            t       <= '0;
        end else case (state)
            WAIT: if (press[1])               state <= EARLY;
                  else if (ms && wait_ms == 0) state <= GO;
                  else if (ms)                 wait_ms <= wait_ms - 1'b1;
            GO:   if (press[1])                  state <= SHOW;
                  else if (ms && t != 14'd9999)  t <= t + 1'b1;
            default: ;
        endcase
    end

    always_comb begin
        LEDR = '0;
        {HEX5, HEX4, HEX3, HEX2, HEX1, HEX0} = {6{BLANK}};
        case (state)
            READY: {HEX5, HEX4, HEX3, HEX2, HEX1} = {R_, E_, A_, D_, Y_};
            WAIT:  {HEX3, HEX2, HEX1, HEX0} = {4{DASH}};
            EARLY: {HEX2, HEX1, HEX0} = {E_, R_, R_};
            default: begin                      // GO (running) and SHOW (frozen)
                LEDR = (state == GO) ? '1 : '0;
                HEX3 = digit(t / 1000);
                HEX2 = digit((t / 100) % 10);
                HEX1 = digit((t / 10) % 10);
                HEX0 = digit(t % 10);
            end
        endcase
    end
endmodule
