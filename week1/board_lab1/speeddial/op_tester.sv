// Runs one operation at the speed of its own clock and reports the % of wrong answers.
//
// Every 16 cycles new random operands are loaded into a/b. The result is captured twice:
//   r_fast: ONE cycle later  (the path under test; wrong if the logic is slower than the clock)
//   r_slow: 13 cycles later  (settled, always right)
// A test is wrong when they differ. pct = wrong tests per WINDOW, in percent.
// Only r_fast is a one-cycle path. Everything that judges it gets several cycles, so at 300 MHz the
// judge itself never fails (on the board it did: mult showed 32% and div 1% at 300 MHz):
//   r_fast vs r_slow compared at phase 15 (r_slow stable since phase 13),
//   the count closed at phase 0, the % worked out at phase 8, with WINDOW a power of two (a shift, not a divider).
//
// OP: 0 = 8-bit add, 1 = 256-bit add (the "big add"), 2 = 16x16 multiply, 3 = 16 / 8 divide
(* multstyle = "logic" *)        // keep the multiplier in logic elements, not the DSP blocks
module op_tester #(
    parameter int OP        = 0,
    parameter int WINDOW    = 1024,   // a power of two: pct = wrong * 100 / WINDOW is then a shift
    parameter int SIM_DELAY = 0      // simulation only: pretend the operation takes this many ns
) (
    input  logic       clk,
    output logic [6:0] pct
);
    logic [63:0] lfsr = 64'h0123_4567_89AB_CDEF;   // never all zeros
    logic [3:0]  phase = '0;
    logic [63:0] a = '0, b = '0;
    logic [64:0] r, r_seen, r_fast = '0, r_slow = '0;
    logic [10:0] tests = '0, wrong = '0, wrong_done = '0;
    logic        mismatch = 1'b0;
    initial pct = '0;

    // each result gets its full width before padding (a product inside {...} would be cut to 16 bits)
    logic [8:0]  sum8;
    logic [64:0] sum64;                  // "big add": really 256 bits, see below
    logic [256:0] sum256;
    logic [31:0] prod;
    logic [15:0] quot;
    assign sum8  = a[7:0] + b[7:0];
    // A 64-bit add never failed on the board, even at 300 MHz: the MAX 10 carry chain is that fast. A 256-bit
    // add makes the carry ripple 4x as far. Its top 65 bits are kept; they depend on the carry from bit 0.
    assign sum256 = {a, b, a ^ b, ~a} + {b, a, ~b, a ^ b};
    assign sum64  = sum256[256:192];
    assign prod  = a[15:0] * b[15:0];
    assign quot  = a[15:0] / {8'b0, b[7:0] | 8'd1};

    always_comb
        case (OP)
            0:       r = {56'b0, sum8};
            1:       r = sum64;
            2:       r = {33'b0, prod};
            default: r = {49'b0, quot};
        endcase

`ifdef SIM
    assign #(SIM_DELAY) r_seen = r;
`else
    assign r_seen = r;
`endif

    always_ff @(posedge clk) begin
        phase <= phase + 1'b1;
        if (phase == 4'd0) begin
            a    <= lfsr;
            b    <= {lfsr[31:0], lfsr[63:32]} ^ 64'h5A5A_5A5A_A5A5_A5A5;
            lfsr <= {lfsr[62:0], lfsr[63] ^ lfsr[62] ^ lfsr[60] ^ lfsr[59]};
            if (tests == WINDOW - 1) begin                     // close the window, judging the last test too
                wrong_done <= wrong + mismatch;
                wrong      <= '0;
                tests      <= '0;
            end else begin
                if (mismatch) wrong <= wrong + 1'b1;           // judge the previous test
                tests <= tests + 1'b1;
            end
        end
        if (phase == 4'd1)  r_fast   <= r_seen;               // the one-cycle path under test
        if (phase == 4'd13) r_slow   <= r_seen;
        if (phase == 4'd15) mismatch <= (r_fast != r_slow);
        if (phase == 4'd8)  pct      <= 7'((32'(wrong_done) * 100) >> $clog2(WINDOW));
    end
endmodule
