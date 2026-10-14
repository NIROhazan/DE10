module tb;
  logic [9:0] SW; logic [1:0] KEY; logic [9:0] LEDR;
  logic [7:0] H0,H1,H2,H3,H4,H5;
  lecture1_top dut(.SW(SW),.KEY(KEY),.LEDR(LEDR),.HEX0(H0),.HEX1(H1),.HEX2(H2),.HEX3(H3),.HEX4(H4),.HEX5(H5));
  function automatic string c(input logic [7:0] s);
    case (s) 8'hC0:c="0";8'hF9:c="1";8'hA4:c="2";8'hB0:c="3";8'h99:c="4";8'h92:c="5";
      8'h82:c="6";8'hF8:c="7";8'h80:c="8";8'h90:c="9";8'hBF:c="-";8'hFF:c=" ";default:c="?"; endcase
  endfunction
  task show(input [1:0] m, input [6:0] x, input k);
    SW={m,1'b0,x}; KEY={1'b1,k}; #1;
    $display("mode %b x=%3d key0=%b | %s%s%s | %s%s%s | LEDR=%b", m, x, k,
      c(H5),c(H4),c(H3),c(H2),c(H1),c(H0),LEDR);
  endtask
  initial begin
    show(0,63,1); show(0,64,1); show(0,127,1); show(0,5,1);
    show(1,40,1); show(1,64,1); show(1,127,1);
    show(2,40,1); show(2,40,0); show(2,127,1); show(2,127,0);
    show(3,7,1); show(3,8,1); show(3,9,1); show(3,127,1); show(3,120,1);
  end
endmodule
