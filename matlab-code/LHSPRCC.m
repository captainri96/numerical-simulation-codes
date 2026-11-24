%Susan Massey
%Most General version of the LHS code
%Modified Sept 2018 and then Jun 2019 to be more interactive/usable

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

%%
A = readmatrix('latin_hypercube_sampling_Results.csv'); 
B = zeros(N,M);
parameters = struct;
prcc_values = zeros(7,5);

parameters(1).name = 'sigma';
parameters(2).name = 'lambda';
parameters(3).name = 'mu';
parameters(4).name = 'T';
parameters(5).name = 'k1';
parameters(6).name = 'k2';
parameters(7).name = 'k3';

for m=1:M
    parameters(m).distribution = 'uniform';
    parameters(m).sample = A(:,m);
end

nodes = [1,13,25,37,49,401,413,425,437,449,801,813,825,837,849];
patterns = {'Diagonal', 'Patches', 'Column strips', 'Row strips', 'Rows_Columns'};

% i = input('Choose node position (see "nodes" in Workspace): ');


%%
% EDIT THE FOLLOWING FOR SAVING YOUR SAMPLES AND SIMULATION DATA:
outFileStr = 'LHS-testlinear'; % give workspace an appropriate unique name
outFileName1 = [outFileStr,'_samples.mat'];
outFileName2 = [outFileStr,'_results.mat'];

save(outFileName1, 'parameters', 'A')


%
for k=1:5

    %%_________________________________________________________________________
    %
    % SECOND STEP: Solve Model Function with Sampled Parameters
    %__________________________________________________________________________

    % Specify independent var(s) to pass to the model function
    t = linspace(0,99,100);  % time domain for ODEs 
    %Simdata = struct; % initialize struct to store outputs for computing PRCCs


    %EDIT THE FOLLOWING FUNCTION CALL FOR YOUR OWN MODEL:


    %k = input('Choose intercropping pattern (see Workspace & choose from 1 to 5): ');

    read_tab = ['removed_outputs\removed_',patterns{k},'_node_',int2str(i)];

    removed_node = readtable(read_tab);
    removed_node = table2array(removed_node);

    for j=1:N
        Simdata(j).y = removed_node(j,:);
    end

    %OutputOfInterest = zeros(N,length(t));
    %OutputOfInterest = Simdata;

    OutputOfInterest = zeros(N,length(t));
    for si = 1:N
        OutputOfInterest(si,:) = Simdata(si).y;
    end


    % EDIT THE FOLLOWING STRING TO NAME OUTPUT DATA:
    labelstring = 'Removed'; % consistent id for plot labels, filenames



    %%_________________________________________________________________________
    %
    % THIRD STEP: Compute & Plot Partial Rank Correlation Coefficients (PRCC)
    %__________________________________________________________________________

    tx_varied = input('Do you want to look at results that might change over time or space (''Y'' or ''N'')?: ');

    if strcmp(tx_varied,'Y')  % TIME Plot

        t = linspace(0,99,100);  % time domain
        x_index = [];

        prcc = VariedPRCC(M,N,A,OutputOfInterest,t,x_index);

        prccPlot = plotVariedPRCC(M,N,t,labelstring,parameters,prcc);



    elseif strcmp(tx_varied,'N')  % BAR Plot

        % EDIT INDICES FOR EVALUATING RESULTS:
        t_index = 90;
        x_index =[];  

        prcc = UnvariedPRCC(M,N,A,OutputOfInterest,t_index,x_index);
        prcc_values(:,k) = prcc(1:7,1);
        %writematrix(prcc, 'prcc_node_813.csv');

        paramNames={parameters.name};
        paramNames2=[parameters.name];

        prccPlot = plotUnvariedPRCC(M,N,labelstring,parameters,prcc, num2str(i), char(patterns(k)));
    end

    figurelabel1=([outFileStr,'-N',num2str(N),'-', labelstring,'-PRCC.fig']); 
    %assign an appropriate filename
    figurelabel2=([outFileStr,'-N',num2str(N),'-', labelstring,'-PRCC.png']);


    %%t_critical is +-1.962 for student T
end

%%
fil_name = ['prcc_values_',int2str(i),'.csv'];
writematrix(prcc_values, fil_name);

%prcc_nod = ['prcc_node_',int2str(i)];


%%
%Susan Massey
%Most General version of the LHS code
%Modified Sept 2018 and then Jun 2019 to be more interactive/usable
