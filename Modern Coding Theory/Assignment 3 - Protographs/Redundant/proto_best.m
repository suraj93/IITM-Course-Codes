clear;clc;

N=3;M=1;

no_edges=10;
eps_best=0;

l=no_edges;
t=1;
p=1;
for i=1:no_edges-2
    for j=1:no_edges-1-i
        for k=1:no_edges-i-j
            H=[i,j,k];

            eps1=proto_thresh_bec_brute(H);
            if eps1>=eps_best
                H_best=H;
                eps_best=eps1;
            end
            t=t+1
            H
        end
    end
end