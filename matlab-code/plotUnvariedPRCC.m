function prccPlot = plotUnvariedPRCC(M,N,labelstring,parameters,prcc, node, pattern)

    figure()
    hold on
    box on

    p=categorical({parameters.name});

    prccPlot = bar(p,prcc(1:M));

    ylabel('PRCC value');
    title(['Correlation Plot for node ', node, ' (', pattern, ')']);
    %title(['Correlation Plot of ',labelstring,' from LHS simulations, ',num2str(N),' samples']);

    for i = 1:7
    text(i, prcc(i), num2str(prcc(i)), ...
        'HorizontalAlignment', 'center', ...
        'VerticalAlignment', 'bottom', ...
        'FontSize', 7);
    end

end

