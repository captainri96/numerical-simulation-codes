%{'Diagonal', 'Patches', 'Column strips', 'Row strips', 'Rows_Columns'};

%%
% Sample data

nodes = [13,25,37,49,401,413,425,437,449,801,813,825,837,849];
arr_ = {'Diagonal', 'Column Strips'};

%read_tab = ['py_files\node_',int2str(i),'_removed_',arr_{k}];

t_index = input('Choose specific time t (1-100): ');

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
    ylim([-1 1])
    xticklabels({'$\sigma$', '$\lambda$', '$\mu$', '$T$','$k_1$', '$k_2$', '$k_3$'}); % Example
    set(gca, 'FontSize', 14,'TickLabelInterpreter', 'latex'); %'XTickLabelRotation', 45 %'fontname','georgia'
    f = gca;
    exportgraphics(f,['bar_', char(arr_(j)),'_',int2str(t_index),'.jpg'],'Resolution',500);

end

% Colormap
%colormap viridis; % Replace with 'parula', 'jet', or 'viridis' as needed

disp('Okay!')



