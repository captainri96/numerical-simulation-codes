%% MAIN

nodes = [13,25,37,49,401,413,425,437,449,801,813,825,837,849];
patterns = {'Diagonal', 'Patches', 'Column strips', 'Row strips', 'Rows_Columns'};
fprintf(['nodes: ' repmat(' %1.0f ',1,numel(nodes)) '\n'], nodes,'\n');

%

tx_varied = input(['\n\nDo you want to look at results that might change over time or' ...
    ' space (''Yes = 0'' or ''No = 1'')?: ']);

if tx_varied == 0 % TIME Plot
    %i = input('\nChoose node position (see "nodes" in Workspace): ');
    i = input('\nChoose node position (13,25,401,413,425,801,849): ');

    for k = [1, 3]
    
        %%_________________________________________________________________________
        %
        % SECOND STEP: Solve Model Function with Sampled Parameters
        %__________________________________________________________________________
    
        % Specify independent var(s) to pass to the model function
        t = linspace(0,99,100);  % time domain for ODEs 
        %Simdata = struct; % initialize struct to store outputs for computing PRCCs
    
    
        %EDIT THE FOLLOWING FUNCTION CALL FOR YOUR OWN MODEL:
    
    
        %k = input('Choose intercropping pattern (see Workspace & choose from 1 to 5): ');
        
        %for i = [13,25,37,49,401,413,425,437,449,801,813,825,837,849]
        read_tab = ['py_files\node_',int2str(i),'_removed_',patterns{k}];
    
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
    
        %end
 
    
        %%_________________________________________________________________________
        %
        % THIRD STEP: Compute & Plot Partial Rank Correlation Coefficients (PRCC)
        %__________________________________________________________________________
    
        %tx_varied = input('Do you want to look at results that might change over time or space (''Yes = 0'' or ''No = 1'')?: ');
        
        %if tx_varied == 0 % TIME Plot
        %if strcmp(tx_varied, Y)  % TIME Plot
    
        t = linspace(0,99,100);  % time domain
        x_index = [];

        prcc = VariedPRCC(M,N,A,OutputOfInterest,t,x_index);

        prccPlot = plotVariedPRCC(M,N,t,labelstring,parameters,prcc,char(patterns(k)),i);
    end

 
elseif tx_varied == 1  % elseif strcmp(tx_varied, N)  % BAR Plot
    t_index = input('Choose specific time t (20,45,65,100): ');

    for i = [13,25,37,49,401,413,425,437,449,801,813,825,837,849]
        for k = [1,3]

            %%_________________________________________________________________________
            %
            % SECOND STEP: Solve Model Function with Sampled Parameters
            %__________________________________________________________________________
            
            % Specify independent var(s) to pass to the model function
            t = linspace(0,99,100);  % time domain for ODEs 
            %Simdata = struct; % initialize struct to store outputs for computing PRCCs
            
            
            %EDIT THE FOLLOWING FUNCTION CALL FOR YOUR OWN MODEL:
            
            
            %k = input('Choose intercropping pattern (see Workspace & choose from 1 to 5): ');
            
            %for i = [13,25,37,49,401,413,425,437,449,801,813,825,837,849]
            read_tab = ['py_files\node_',int2str(i),'_removed_',patterns{k}];
            
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
        
        
            % EDIT INDICES FOR EVALUATING RESULTS:
            % t_index = 90;
            x_index =[];  
        
            prcc = UnvariedPRCC(M,N,A,OutputOfInterest,t_index-1,x_index);
            patts = [1, 3];
            index = find(patts==k);
            disp(index)
            prcc_values(:,index) = prcc(1:7,1);
            %writematrix(prcc, 'prcc_node_813.csv');
        
            paramNames={parameters.name};
            paramNames2=[parameters.name];
        
            %prccPlot = plotUnvariedPRCC(M,N,labelstring,parameters,prcc, num2str(i), char(patterns(k)));
        
            figurelabel1 = ([outFileStr,'-N',num2str(N),'-', labelstring,'-PRCC.fig']); 

            %assign an appropriate filename
            figurelabel2 = ([outFileStr,'-N',num2str(N),'-', labelstring,'-PRCC.png']);

            fil_name = ['prcc_values\prcc_values_',int2str(i),'_t=',int2str(t_index),'.csv'];
            writematrix(prcc_values, fil_name);

            %%t_critical is +-1.962 for student T        
        end
    end

   %
   %
   %
    % Sample data
    
    nodes = [13,25,37,49,401,413,425,437,449,801,813,825,837,849];
    arr_ = {'Diagonal', 'Column Strips'};
   
    for j=1:2 
        prcc_vals_bar = zeros(14,7);
        n = 0;
    
        for nod = [13,25,37,49,401,413,425,437,449,801,813,825,837,849] 
            n = n+1;
            file = ['prcc_values\prcc_values_',int2str(nod),'_t=',int2str(t_index),'.csv'];
            read_data = readtable(file);
            read_data = table2array(read_data);
            %vals = read_data';
            prcc_vals_bar(n,:) = read_data(1:7,j)';
        end
        filen = ['prcc_values\PRCC_values_',char(arr_(j)),int2str(t_index),'.csv'];
        writematrix(prcc_vals_bar, filen);
    
     
        % Plotting
        figure;
        b = bar(prcc_vals_bar','FaceColor','flat', 'EdgeColor', 'flat','BarWidth', 1); % Bar plot  
        
        for k = 1:size(prcc_vals_bar',2)
            b(k).CData = k;
        end
        
        
        %colorbar; % Show colorbar for reference
        %colormap viridis; % Set the colormap
           
        xlabel('Parameters','interpreter','latex');
        ylabel(['PRCC ($t=$ ',int2str(t_index),')'], 'interpreter','latex');     %, ' (t = ', int2str(t_index), ')'
        title(char(arr_(j)), 'fontname','georgia'); 
        yticks([-1 -0.75 -0.5 -0.25 0 0.25 0.5 0.75 1])
        ylim([-1 1])
        xticklabels({'$\sigma$', '$\lambda$', '$\mu$', '$T$','$k_1$', '$k_2$', '$k_3$'}); % Example
        %set(gca, 'FontSize', 14,'TickLabelInterpreter', 'latex'); %'XTickLabelRotation', 45 %'fontname','georgia'
        set(gca, 'FontSize', 14,'TickLabelInterpreter', 'latex')

        legendHandle = legend({'13','25','37','49','401','413','425','437','449','801','813','825','837','849'},...
            'Location','southeast', 'interpreter','latex');
        legendHandle.NumColumns = 3;
        legendHandle.Title.String = "node $i$";
        legendHandle.FontSize = 8;
        
        exportgraphics(gcf,['bar_', char(arr_(j)),'_ ',int2str(t_index),'.png'],'Resolution',500);

end

% Colormap
%colormap viridis; % Replace with 'parula', 'jet', or 'viridis' as needed

disp('Okay!')

              
end

%%
% fil_name = ['prcc_values\prcc_values_',int2str(i),'.csv'];
% writematrix(prcc_values, fil_name);

%prcc_nod = ['prcc_node_',int2str(i)];


%%
%Susan Massey
%Most General version of the LHS code
%Modified Sept 2018 and then Jun 2019 to be more interactive/usable
