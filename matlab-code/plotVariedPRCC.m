function prccPlot = plotVariedPRCC(M,N,x,labelstring,parameters,prcc, pattern,i)

    figure()
    hold on
    box on
    for mm=1:M
        plot(x, prcc(mm,:),'LineWidth',2.0);
    end
    
    prccPlot = gca; 

    xlabel('time (days)', 'interpreter','latex');
    ylabel(['PRCC ($i=$ ',int2str(i),')'], 'interpreter','latex');
    title(pattern,  'fontname','georgia');
    %yticks([-1 -0.75 -0.5 -0.25 0 0.25 0.5 0.75 1])
    ylim([-1 1])
    %title(['Time  Plot of the ',labelstring,' compartment from LHS simulations w/ ',num2str(N),' samples']);
    set(gca, 'FontSize', 16, 'TickLabelInterpreter', 'latex'); %'fontname','georgia'


    legend(parameters.name,'Location','South', 'Orientation','horizontal','FontSize', 16,'interpreter','latex'); %EastOutside
    legend('boxoff')
    
    set(gca, 'Position', [0.1 0.10 0.7 0.8]); % Adjust axes to fit the legend
    set(gcf, 'Position', [100, 100, 900, 500]); % Increase figure size % [x y width height]
    exportgraphics(gcf, ['_time_', pattern, '_', int2str(i), '.png'], 'Resolution', 500);

    %exportgraphics(gcf, ['time_', pattern,'_ ',int2str(i),'.png'],'Resolution',500 );

end