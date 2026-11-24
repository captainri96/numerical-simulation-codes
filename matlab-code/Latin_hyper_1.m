%Susan Massey
%Most General version of the LHS code
%Modified Sept 2018 and then Jun 2019 to be more interactive/usable


% NOTE: Run this code only once. Once a csv file 'latin_hypercube_sampling_Results.csv'
% is saved, NEVER run this Matlab code again. 

clear all
close all
clc

%%
%%_________________________________________________________________________
%
% FIRST STEP: Latin Hypercube Sampling of Model Parameters 
%__________________________________________________________________________

% This requests user input via the command line to get started:
M = input('Number of parameters to sample?: '); % Don't include add'l parameters you would like to leave fixed
while rem(M,1)~=0 || M<=0
    M = input('Number of parameters should be an integer > 0. Please re-enter the number of parameters: ');
end

N = input('Number of samples to draw? (recommend 100 to 1000): '); 
while rem(N,1)~=0 || N<=0
    N = input('Number of samples should be an integer > 0. Please re-enter the number of samples: ');
end
%%
% This code will prompt for sample distribution specifics and return 
% drawn and randomly paired parameter samples
[parameters,A] = DrawSamples(M,N);

filename = 'latin_hypercube_sampling_Results.csv';
lhs_result = array2table(A,'VariableNames',{'sigma','lambda','mu','T','k1','k2','k3'});
writetable(lhs_result, filename);
