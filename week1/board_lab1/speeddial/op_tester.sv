// Runs one operation at the speed of its own clock and reports the % of wrong answers.
//
// Every 32 cycles new random operands are loaded into a/b. The result is captured twice:
//   r_fast: ONE cycle later  (the path under test; wrong if the logic is slower than the clock)
//   r_slow: 24 cycles later  (settled, always right: the divide needs ~40 ns, 24 cycles at 300 MHz are 80 ns)
// A test is wrong when they differ. pct = wrong tests per WINDOW, in percent.
//
// Only a/b -> r_fast may be a one-cycle path. At 300 MHz the judge itself failed timing by up to 2.3 ns
// (mismatch -> wrong, the shared phase counter fanning out to every register), so the board showed 0%
// for divide and multiply however wrong they were. Now:
//   * the phase is a one-hot ring of 32 flip-flops; every step is enabled by its own flip-flop (st_*, a copy
//     of the ring), never by a compare;
//   * the data each step uses was written at least 3 cycles before (multicycle paths in speeddial.sdc);
//   * a, b and the ring are kept per tester (dont_merge): Quartus merged them across the four
//     operations of a clock, which made one register drive all four.
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
    // the steps of one test, by phase (0..31)
    localparam logic [4:0] P_LOAD = 5'd0,  P_FAST = 5'd1, P_SLOW = 5'd24, P_CMP = 5'd27,
                           P_COUNT = 5'd30, P_PCT = 5'd10;

    logic [63:0] lfsr = 64'h0123_4567_89AB_CDEF;   // never all zeros
    (* dont_merge *) logic [31:0] ring = 32'd1;     // one-hot: ring[k] is high during phase k
    // st_X is high during phase X: a copy of ring[X-1] one cycle later, so the ring itself only shifts.
    // maxfan: Quartus duplicates a strobe that would drive more than 16 registers (st_load drives ~190).
    (* dont_merge, maxfan = 16 *) logic st_load = 1'b0, st_fast = 1'b0, st_slow = 1'b0, st_cmp = 1'b0, st_count = 1'b0, st_pct = 1'b0;
    (* dont_merge *) logic [63:0] a = '0, b = '0;
    (* dont_merge *) logic        cin = 1'b0;      // the big add's carry in (random)
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
    // A 64-bit add never failed on the board, even at 300 MHz, and neither did a 256-bit add of random numbers:
    // with random operands a carry stops after ~8 bits, so the long path was never used. Now (OP 1) b = ~a,
    // so every bit passes the carry on, and a random carry in must ripple through all 256 bits to the top.
    // a and b are separate registers, so Quartus cannot see that b = ~a and fold the adder away.
    // Its top 65 bits are kept; they all depend on the carry in.
    assign sum256 = {a, a, a, a} + {b, b, b, b} + 257'(cin);
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
        ring     <= {ring[30:0], ring[31]};         // a shift, no decoding
        st_load  <= ring[5'(P_LOAD  - 5'd1)];
        st_fast  <= ring[5'(P_FAST  - 5'd1)];
        st_slow  <= ring[5'(P_SLOW  - 5'd1)];
        st_cmp   <= ring[5'(P_CMP   - 5'd1)];
        st_count <= ring[5'(P_COUNT - 5'd1)];
        st_pct   <= ring[5'(P_PCT   - 5'd1)];

        if (st_load) begin
            a    <= lfsr;
            b    <= (OP == 1) ? ~lfsr : {lfsr[31:0], lfsr[63:32]} ^ 64'h5A5A_5A5A_A5A5_A5A5;
            cin  <= lfsr[17];
            lfsr <= {lfsr[62:0], lfsr[63] ^ lfsr[62] ^ lfsr[60] ^ lfsr[59]};
        end
        if (st_fast)  r_fast   <= r_seen;                     // the one-cycle path under test
        if (st_slow)  r_slow   <= r_seen;
        if (st_cmp)   mismatch <= (r_fast != r_slow);
        if (st_count) begin
            if (tests == WINDOW - 1) begin                     // close the window, judging the last test too
                wrong_done <= wrong + mismatch;
                wrong      <= '0;
                tests      <= '0;
            end else begin
                wrong <= wrong + mismatch;
                tests <= tests + 1'b1;
            end
        end
        if (st_pct)   pct <= 7'((32'(wrong_done) * 100) >> $clog2(WINDOW));
    end
endmodule
