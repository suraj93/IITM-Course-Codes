% Description - Add AWGN of a given SNR to a signal. 
%
% Source      - http://stackoverflow.com/questions/23690766/proper-way-to-add-noise-to-signal

function out_signal = addAWGN(signal, targetSNR)
sigLength = length(signal); % length
awgnNoise = randn(size(signal)); % orignal noise
pwrSig = sqrt(sum(signal.^2))/sigLength; % signal power
pwrNoise = sqrt(sum(awgnNoise.^2))/sigLength; % noise power

scaleFactor = (pwrSig/pwrNoise)/targetSNR; %find scale factor
awgnNoise = scaleFactor*awgnNoise; 
out_signal = signal + awgnNoise; % add noise