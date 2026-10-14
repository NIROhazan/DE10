// Lecture 1 board demo — DE10-Lite, purely combinational (no clock).
//
//   SW[9:8] = mode, SW[6:0] = x, KEY[0] (held) = show x/6 instead of x/8 in mode 10
//   HEX5..HEX3 = left value (always x), HEX2..HEX0 = right value, both decimal
//
//   mode 00: x (signed)   | x + 1 (7-bit, wraps 63 -> -64) | LEDs = x      slides 13-14
//   mode 01: x (unsigned) | 2x (7-bit, wraps past 127)     | LEDs = 2x     slides 11-12
//   mode 10: x (unsigned) | x/8, or x/6 while KEY0 held    | LEDs = result slides 9-10
//   mode 11: x (signed)   | x squeezed into 4 bits         | LEDs = x      slide 15
//
// Port names match the Terasic DE10-Lite System Builder / golden top, so its .qsf
// pin assignments apply unchanged.
module lecture1_top (
    input  logic [9:0] SW,
    input  logic [1:0] KEY,
    output logic [9:0] LEDR,
    output logic [7:0] HEX0, HEX1, HEX2, HEX3, HEX4, HEX5
);
    logic [1:0] mode;
    logic [6:0] x, x_plus_1, x_times_2, quotient;
    logic signed [8:0] left, right;

    assign mode      = SW[9:8];
    assign x         = SW[6:0];
    assign x_plus_1  = x + 7'd1;
    assign x_times_2 = {x[5:0], 1'b0};
    assign quotient  = KEY[0] ? x / 7'd8 : x / 7'd6;   // KEY is active-low

    always_comb begin
        LEDR = '0;
        case (mode)
            2'b00: begin
                left  = {{2{x[6]}}, x};
                right = {{2{x_plus_1[6]}}, x_plus_1};
                LEDR[6:0] = x;
            end
            2'b01: begin
                left  = {2'b00, x};
                right = {2'b00, x_times_2};
                LEDR[7:0] = {x, 1'b0};      // the pattern visibly moves one place left
            end
            2'b10: begin
                left  = {2'b00, x};
                right = {2'b00, quotient};
                LEDR[6:0] = quotient;       // /8: pattern slid right by 3; /6: scrambled
            end
            default: begin
                left  = {{2{x[6]}}, x};
                right = {{5{x[3]}}, x[3:0]};  // the Ariane 5 narrowing
                LEDR[6:0] = x;
            end
        endcase
    end

    decimal3 left_display  (.value(left),  .hundreds(HEX5), .tens(HEX4), .ones(HEX3));
    decimal3 right_display (.value(right), .hundreds(HEX2), .tens(HEX1), .ones(HEX0));
endmodule


// Shows a signed value (-99..199) on three active-low 7-segment digits, with a
// leading minus sign and leading-zero blanking.
module decimal3 (
    input  logic signed [8:0] value,
    output logic [7:0] hundreds, tens, ones
);
    localparam logic [7:0] BLANK = 8'b1111_1111;
    localparam logic [7:0] MINUS = 8'b1011_1111;   // segment g only

    function automatic logic [7:0] digit(input logic [3:0] d);
        case (d)                                   // {dp, g..a}, active-low
            4'd0: digit = 8'b1100_0000;
            4'd1: digit = 8'b1111_1001;
            4'd2: digit = 8'b1010_0100;
            4'd3: digit = 8'b1011_0000;
            4'd4: digit = 8'b1001_1001;
            4'd5: digit = 8'b1001_0010;
            4'd6: digit = 8'b1000_0010;
            4'd7: digit = 8'b1111_1000;
            4'd8: digit = 8'b1000_0000;
            4'd9: digit = 8'b1001_0000;
            default: digit = BLANK;
        endcase
    endfunction

    logic negative;
    logic [7:0] magnitude;

    always_comb begin
        negative  = value < 0;
        magnitude = negative ? -value : value;

        ones = digit(magnitude % 10);

        if (magnitude >= 10) tens = digit((magnitude / 10) % 10);
        else                 tens = negative ? MINUS : BLANK;

        if (magnitude >= 100)                  hundreds = digit(magnitude / 100);
        else if (negative && magnitude >= 10)  hundreds = MINUS;
        else                                   hundreds = BLANK;
    end
endmodule
