%Susan Massey
%Most General version of the LHS code
%Modified Sept 2018 and then Jun 2019 to be more interactive/usable

%%
% clear all
% close all
% clc

%%
N = 1000;
M = 7;

A = readmatrix('latin_hypercube_sampling_Results.csv'); 
B = zeros(N,M);
parameters = struct;
prcc_values = zeros(7,2); %7 params x 2 intercropping patterns

parameters(1).name = '$\sigma$';
parameters(2).name = '$\lambda$';
parameters(3).name = '$\mu$';
parameters(4).name = '$T$';
parameters(5).name = '$k_1$';
parameters(6).name = '$k_2$';
parameters(7).name = '$k_3$';

for m=1:M
    parameters(m).distribution = 'uniform';
    parameters(m).sample = A(:,m);
end

%nodes = [1,13,25,37,49,401,413,425,437,449,801,813,825,837,849];
%patterns = {'Diagonal', 'Patches', 'Column strips', 'Row strips', 'Rows_Columns'};

nodes = [13,25,37,49,401,413,425,437,449,801,813,825,837,849];
patterns = {'Diagonal', 'Column strips'};

% i = input('Choose node position (see "nodes" in Workspace): ');


%%
% EDIT THE FOLLOWING FOR SAVING YOUR SAMPLES AND SIMULATION DATA:
outFileStr = 'LHS-testlinear'; % give workspace an appropriate unique name
outFileName1 = [outFileStr,'_samples.mat'];
outFileName2 = [outFileStr,'_results.mat'];

save(outFileName1, 'parameters', 'A')

disp('Okay!')
