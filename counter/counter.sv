`timescale 1ns/1ns

module counter(
    input bit clk,
    input bit reset_n,
    output byte unsigned count
    );
    
    always @(posedge clk)
    begin
        if(!reset_n)
            count <= 'b0;
        else
            count <= count + 1;
    end
endmodule