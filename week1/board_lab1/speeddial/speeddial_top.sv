// Speed dial, DE10-Lite. Riddles 7-9: a faster clock gives WRONG answers, and bigger
// operations break first.
//
//   SW[4:3] operation : 00 = 8-bit add, 01 = 64-bit add, 10 = 16x16 multiply, 11 = 16/8 divide
//   SW[2:0] clock     : 0 = 10, 1 = 25, 2 = 50, 3 = 100, 4 = 200, 5 = 300 MHz (6, 7 = ---)
//   HEX5..3 = clock in MHz, HEX1..0 = % wrong answers (99 = 99-100%), LEDR9 = any wrong answers
//
// Every (clock, operation) pair runs all the time in its own tester; the switches only pick
// which result is shown. So nothing is ever switched between clocks.
module speeddial_top #(
    parameter int WINDOW    = 1024,                                 // tests per %, a power of two
    parameter int SIM_D0 = 0, SIM_D1 = 0, SIM_D2 = 0, SIM_D3 = 0   // simulation only (ns)
) (
    input  logic       MAX10_CLK1_50,
    input  logic [9:0] SW,
    input  logic [1:0] KEY,
    output logic [9:0] LEDR,
    output logic [7:0] HEX0, HEX1, HEX2, HEX3, HEX4, HEX5
);
    localparam logic [7:0] BLANK = 8'hFF, DASH = 8'b1011_1111;

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

    // three decimal digits, leading zeros blanked
    function automatic logic [23:0] three(input logic [9:0] v);
        three[23:16] = (v >= 100) ? digit(v / 100)       : BLANK;
        three[15:8]  = (v >= 10)  ? digit((v / 10) % 10) : BLANK;
        three[7:0]   = digit(v % 10);
    endfunction

    logic       clk50;
    logic [4:0] pll_c;
    logic       locked;
    logic [5:0] clk_t;                     // test clocks, slowest first
    assign clk50 = MAX10_CLK1_50;

    speed_pll pll (.inclk0(clk50), .c(pll_c), .locked(locked));
    assign clk_t = {pll_c[4], pll_c[3], pll_c[2], clk50, pll_c[1], pll_c[0]};

    function automatic logic [9:0] mhz(input logic [2:0] f);
        case (f)
            3'd0: mhz = 10;   3'd1: mhz = 25;   3'd2: mhz = 50;
            3'd3: mhz = 100;  3'd4: mhz = 200;  default: mhz = 300;
        endcase
    endfunction

    logic [6:0] pct [6][4];
    genvar f, op;                          // Quartus Standard wants them outside the loop
    generate
        for (f = 0; f < 6; f++) begin : g_clk
            for (op = 0; op < 4; op++) begin : g_op
                localparam int D = (op == 0) ? SIM_D0 : (op == 1) ? SIM_D1 : (op == 2) ? SIM_D2 : SIM_D3;
                op_tester #(.OP(op), .WINDOW(WINDOW), .SIM_DELAY(D))
                    t (.clk(clk_t[f]), .pct(pct[f][op]));
            end
        end
    endgenerate

`ifndef SIM
    // all 24 percentages and the PLL lock, readable from the PC (quartus_stp, In-System Sources and Probes):
    // probe = {locked, pct[5][3], pct[5][2], ..., pct[0][0]}, 7 bits each, clock 0 (10 MHz) in the low bits
    logic [168:0] probe_all;
    always_comb begin
        probe_all[168] = locked;
        for (int fi = 0; fi < 6; fi++)
            for (int oi = 0; oi < 4; oi++)
                probe_all[(fi * 4 + oi) * 7 +: 7] = pct[fi][oi];
    end
    altsource_probe #(
        .sld_auto_instance_index("YES"), .sld_instance_index(0), .instance_id("PCT"),
        .probe_width(169), .source_width(1), .source_initial_value("0"), .enable_metastability("NO")
    ) pct_probe (.probe(probe_all), .source(), .source_clk(clk50), .source_ena(1'b1));
`endif

    logic [2:0] f_sel;
    logic [1:0] op_sel;
    assign f_sel  = SW[2:0];
    assign op_sel = SW[4:3];

    // bring the chosen percentage into the 50 MHz display clock
    logic [6:0] pct_meta = '0, pct_shown = '0;
    always_ff @(posedge clk50) begin
        pct_meta  <= (f_sel <= 3'd5) ? pct[f_sel][op_sel] : '0;
        pct_shown <= pct_meta;
    end

    always_comb begin
        LEDR = '0;
        if (!locked) begin
            {HEX5, HEX4, HEX3, HEX2, HEX1, HEX0} = {6{DASH}};
        end else if (f_sel > 3'd5) begin
            {HEX5, HEX4, HEX3} = {3{DASH}};
            {HEX2, HEX1, HEX0} = {3{BLANK}};
        end else begin
            {HEX5, HEX4, HEX3} = three(mhz(f_sel));
            {HEX2, HEX1, HEX0} = three((pct_shown > 7'd99) ? 10'd99 : {3'b0, pct_shown});  // 99 = 99-100%, keeps a gap after the MHz
            LEDR[9]   = (pct_shown != 0);
            LEDR[4:3] = op_sel;            // echo the switches that chose the operation
            LEDR[2:0] = f_sel;
        end
    end
endmodule
