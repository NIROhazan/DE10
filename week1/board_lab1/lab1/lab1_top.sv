// Lab 1 board — DE10-Lite. One pre-flashed design, 8 cards, selected by SW[9:7].
// Cards are numbered in the order the course answers them (see ../lab1_board_challenges.md).
//
// Warm-up first: at power-on the board shows "set the switches to ten" mode, LEDR = SW and
// HEX2..HEX0 = SW[9:0] in hex (000-3FF). Holding KEY0 and KEY1 together leaves it for good
// (until power-off), and the cards below start.
//
//   SW9 SW8 SW7   card                       answered
//    0   0   0    1 +1                       wk 2
//    0   0   1    2 moving lights            wk 2 (+ wk 10)
//    0   1   0    3 squeeze into 4 bits      wk 2
//    0   1   1    4 the light that remembers wk 5
//    1   0   0    5 turnstile                wk 6
//    1   0   1    6 instant / late light     wk 7
//    1   1   0    7 speed dial               wk 8-10  (placeholder: needs PLL + board prototype)
//    1   1   1    8 x 0.1                    wk 11
//
// Port names match the Terasic DE10-Lite golden top.
module lab1_top #(
    parameter int TICK_DIV = 50_000_000,         // 1 Hz tick from the 50 MHz clock
    parameter int CARD     = -1                  // -1: warm-up, then SW9..SW7 pick the card (the pre-flashed board)
                                                 // 0..7: that card only, no warm-up (one .sof per step of lab1_kit)
) (
    input  logic       MAX10_CLK1_50,
    input  logic [9:0] SW,
    input  logic [1:0] KEY,
    output logic [9:0] LEDR,
    output logic [7:0] HEX0, HEX1, HEX2, HEX3, HEX4, HEX5
);
    localparam logic [7:0] BLANK = 8'hFF;
    // {dp, g, f, e, d, c, b, a}, active-low
    localparam logic [7:0] L_ = 8'b1100_0111, O_ = 8'b1100_0000, C_ = 8'b1100_0110,
                           P_ = 8'b1000_1100, E_ = 8'b1000_0110, N_ = 8'b1010_1011,
                           S_ = 8'b1001_0010, D_ = 8'b1010_0001;

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

    logic       clk;
    logic [2:0] card;
    logic [6:0] x;
    assign clk  = MAX10_CLK1_50;
    assign card = (CARD < 0) ? SW[9:7] : 3'(CARD);
    assign x    = SW[6:0];

    // ---- keys: raw (combinational cards), synchronised, and one-cycle press pulses ----
    logic [1:0] held;                                 // 1 = pressed, raw
    logic [1:0] k_meta = '0, k = '0, k_prev = '0;
    logic [1:0] press;
    assign held = ~KEY;
    always_ff @(posedge clk) begin
        k_meta <= held;
        k      <= k_meta;
        k_prev <= k;
    end
    assign press = k & ~k_prev;

    // ---- warm-up: on at power-on, off once both keys are held ----
    logic warmup = (CARD < 0);
    always_ff @(posedge clk) if (k == 2'b11) warmup <= 1'b0;

    function automatic logic [7:0] hexdigit(input logic [3:0] d);
        case (d)
            4'hA: hexdigit = 8'b1000_1000;  4'hB: hexdigit = 8'b1000_0011;
            4'hC: hexdigit = 8'b1100_0110;  4'hD: hexdigit = 8'b1010_0001;
            4'hE: hexdigit = 8'b1000_0110;  4'hF: hexdigit = 8'b1000_1110;
            default: hexdigit = digit(d);
        endcase
    endfunction

    // ---- 1 Hz tick ----
    logic [$clog2(TICK_DIV)-1:0] tcnt = '0;
    logic tick, blink;
    always_ff @(posedge clk) tcnt <= (tcnt == TICK_DIV - 1) ? '0 : tcnt + 1'b1;
    assign tick  = (tcnt == TICK_DIV - 1);
    assign blink = (tcnt < TICK_DIV / 2);

    // ---- cards 1-3: two decimal displays ----
    logic signed [8:0] left, right;
    logic [7:0] l2, l1, l0, r2, r1, r0;
    decimal3 left_display  (.value(left),  .hundreds(l2), .tens(l1), .ones(l0));
    decimal3 right_display (.value(right), .hundreds(r2), .tens(r1), .ones(r0));

    logic [6:0] x_plus_1, quotient;
    assign x_plus_1 = x + 7'd1;
    assign quotient = held[0] ? x / 7'd6 : x / 7'd8;

    // ---- card 4: a real SR latch, two cross-coupled NOR gates, fed by the raw keys ----
    (* keep *) logic q, qb;
    logic set_in, reset_in;
    assign set_in   = held[1];
    assign reset_in = held[0];
    assign q  = ~(reset_in | qb);
    assign qb = ~(set_in   | q);

    // ---- card 5: turnstile (KEY1 = coin, KEY0 = push) ----
    logic       is_open = 1'b0;
    logic [3:0] coins   = '0;
    logic [6:0] passes  = '0;
    always_ff @(posedge clk)
        if (card == 3'd4 && !warmup) begin
            if (press[1]) begin
                is_open <= 1'b1;
                if (coins != 4'd10) coins <= coins + 1'b1;
            end else if (press[0] && is_open) begin
                is_open <= 1'b0;
                coins   <= '0;
                passes  <= (passes == 7'd99) ? '0 : passes + 1'b1;
            end
        end

    // ---- card 6: Harris's Mealy vs Moore, input sampled on the 1 Hz tick ----
    logic a_prev = 1'b0, moore = 1'b0;
    logic mealy;
    always_ff @(posedge clk)
        if (tick) begin
            a_prev <= k[0];
            moore  <= ~a_prev & k[0];
        end
    assign mealy = ~a_prev & k[0];

    // ---- card 8: x times 0.1 (stored as 25/256) or 0.25 (64/256, exact) ----
    logic [3:0]  xs;
    logic [9:0]  prod;
    logic [17:0] thousandths;
    assign xs          = SW[3:0];
    assign prod        = xs * (held[0] ? 10'd64 : 10'd25);
    assign thousandths = (prod[7:0] * 18'd1000) >> 8;

    // ---- output mux ----
    always_comb begin
        left  = '0;
        right = '0;
        LEDR  = '0;
        {HEX5, HEX4, HEX3, HEX2, HEX1, HEX0} = {6{BLANK}};

        case (card)
            3'd0: begin                                   // 1: +1
                left  = {{2{x[6]}}, x};
                right = {{2{x_plus_1[6]}}, x_plus_1};
                LEDR[6:0] = x;
            end
            3'd1: begin                                   // 2: moving lights
                left = {2'b00, x};
                if (held[1] && !held[0]) begin            // KEY1: x2
                    right     = {1'b0, x, 1'b0};
                    LEDR[7:0] = {x, 1'b0};
                end else begin                            // none: /8, KEY0: /6
                    right     = {2'b00, quotient};
                    LEDR[6:0] = quotient;
                end
            end
            3'd2: begin                                   // 3: squeeze into 4 bits
                left  = {{2{x[6]}}, x};
                right = {{5{x[3]}}, x[3:0]};
                LEDR[6:0] = x;
            end
            3'd3: begin                                   // 4: the light that remembers
                LEDR[0] = q;
                LEDR[1] = set_in;
                LEDR[2] = qb;
            end
            3'd4: begin                                   // 5: turnstile
                {HEX5, HEX4, HEX3, HEX2} = is_open ? {O_, P_, E_, N_} : {L_, O_, C_, BLANK};
                HEX1 = (passes >= 10) ? digit(passes / 10) : BLANK;
                HEX0 = digit(passes % 10);
                LEDR = (10'b1 << coins) - 1'b1;
            end
            3'd5: begin                                   // 6: instant / late light
                LEDR[9] = blink;
                LEDR[0] = mealy;
                LEDR[1] = moore;
            end
            3'd6: begin                                   // 7: speed dial placeholder
                {HEX5, HEX4, HEX3, HEX2, HEX1} = {S_, P_, E_, E_, D_};
            end
            default: begin                                // 8: x 0.1
                HEX5 = (xs >= 10) ? digit(xs / 10) : BLANK;
                HEX4 = digit(xs % 10);
                HEX3 = digit(prod[9:8]) & 8'b0111_1111;   // decimal point on
                HEX2 = digit(thousandths / 100);
                HEX1 = digit((thousandths / 10) % 10);
                HEX0 = digit(thousandths % 10);
            end
        endcase

        if (card <= 3'd2) {HEX5, HEX4, HEX3, HEX2, HEX1, HEX0} = {l2, l1, l0, r2, r1, r0};

        if (warmup) begin                                 // warm-up: set the switches to ten
            LEDR = SW;
            {HEX5, HEX4, HEX3} = {3{BLANK}};
            HEX2 = hexdigit({2'b00, SW[9:8]});
            HEX1 = hexdigit(SW[7:4]);
            HEX0 = hexdigit(SW[3:0]);
        end
    end
endmodule


// A signed value (-99..255) on three active-low digits, minus sign, leading blanks.
module decimal3 (
    input  logic signed [8:0] value,
    output logic [7:0] hundreds, tens, ones
);
    localparam logic [7:0] BLANK = 8'hFF, MINUS = 8'b1011_1111;

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

    logic negative;
    logic [8:0] magnitude;
    always_comb begin
        negative  = value < 0;
        magnitude = negative ? -value : value;
        ones = digit(magnitude % 10);
        if (magnitude >= 10) tens = digit((magnitude / 10) % 10);
        else                 tens = negative ? MINUS : BLANK;
        if (magnitude >= 100)                 hundreds = digit(magnitude / 100);
        else if (negative && magnitude >= 10) hundreds = MINUS;
        else                                  hundreds = BLANK;
    end
endmodule
