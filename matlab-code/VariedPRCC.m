function [prcc]=VariedPRCC(M,N,A,OutputOfInterest,xt,idx)
    % M is the number of parameters sampled
    % N is the number of samples drawn using Latin Hypercube Sampling
    % A contains the result for all sampled parameters
    % OutputOfInterest is an array/cell containing the desired value or
    % state variable that we are interested in
    % xt refers to the number of nodes for a spatially varied SEIR model
    % t_index = [] for a spatially varied SEIR model

    K=zeros(N,M+1); % number of samples drawn N x number of model parameters (M) + 1 output column
    R=zeros(N,M+1); % initializing the rank matrix

    prcc=zeros(M+1,length(xt)); % initializing matrix to hold PRCC statistic for each parameter at each time

    % if N>=250
    %     studentT=zeros(M+1,length(t)); % initializing matrix to hold the studentT statistic for each parameter at each time
    K([1:N],[1:M])=A([1:N],[1:M]); %Taking the information from A and putting it into K

    % else
    %     studentT = [];
    %     fprintf(['Not enough samples (<250) for computing studentT statistic. \n'])
    % end

    for steps=1:length(xt)  % loop through time (or space) - TO DO: would like to be able to do both and get surfaces..

        for n=1:N %loop through each of the N samples
            if isempty(idx)
                K(n,M+1)=OutputOfInterest(n,steps); 
                %Output results go in the last column, the M+1st column.
            else
                K(n,M+1)=OutputOfInterest(n,idx,steps); 
                %Output results go in the last column, the M+1st column.
            end
        end

        
        for m=1:M+1 %for each parameter rank the data, including the output data
            for n=1:N
    %          select parameter column m
                [s,i]=sort(K(:,m));  %sort according to the rank of column m; 
                % s contains the sorted values; 
                % i contains the indices of the original values in the sorted order.
                r(i,1)=[1:N]';  %r(i, 1) assigns ranks based on the indices from sort(); 
                                %This ensures the ranks correspond to the original positions of the values in K
             R(n,m)=r(n,1); %store the ranking of the parameter at it's position in K; 
            end
        end


        C=corrcoef(R);
        if det(C)<=10^-16 %If the determinant is singular or very nearly singular
            B=pinv(C);    %must use pseudo inverse (as inv will not be accurate).
            ST=num2str(steps); %Report the timestep of the singularity (since space is fixed).
            fprintf(['C is singular at timestep ', ST,'. \n'])
        else
            B=inv(C); %The dterminant is not singular, so the inverse is valid.
        end

        % if N>=250
        %     for w=1:M %iterate thru the M parameters to calculate PRCCs for each with ratio
                % prcc(w,steps)=(-B(w,M+1))/sqrt(B(w,w)*B(M+1,M+1)); % the PRCC between the wth parameter and the ratio
        %         studentT(w,steps)=prcc(w,steps)*sqrt((N-2)/(1-prcc(w,steps))); % the studentT statistic corresponding to the PRCC
        %     end
        % else
            for w=1:M %iterate thru the M parameters to calculate PRCCs for each with ratio
                prcc(w,steps)=(-B(w,M+1))/sqrt(B(w,w)*B(M+1,M+1)); % the PRCC between the wth parameter and the ratio                
            end
        % end;
        % % Each studentT is the distribution (showing the significance of) the corresponding gamma/PRCC. 
    end
end



% function [prcc] = VariedPRCC(M, N, A, OutputOfInterest, xt, selected_nodes)
%     % M: Number of parameters sampled
%     % N: Number of samples drawn using Latin Hypercube Sampling
%     % A: N x M matrix of sampled parameter values
%     % OutputOfInterest: N x T x num_nodes matrix of model outputs
%     % xt: Array of time points for analysis
%     % selected_nodes: Indices of the nodes/plants to analyze
% 
%     num_nodes = length(selected_nodes);  % Number of nodes to analyze
%     prcc = zeros(M, length(xt), num_nodes);  % PRCC values for each parameter, time point, and node
% 
%     for node_idx = 1:num_nodes
%         node = selected_nodes(node_idx);  % Current node index
% 
%         % Initialize rank matrices
%         K = zeros(N, M+1);  % Parameter values and output values
%         R = zeros(N, M+1);  % Ranks of parameters and output
% 
%         for t_idx = 1:length(xt)  % Loop through each time point
%             time_step = xt(t_idx);
% 
%             % Fill the K matrix with parameter samples and output at the selected node and time step
%             K(:, 1:M) = A(:, 1:M);  % Copy parameter values
%             K(:, M+1) = OutputOfInterest(:, time_step, node);  % Copy output of interest for this node and time
% 
%             % Rank transformation
%             for m = 1:(M+1)
%                 [s, i] = sort(K(:, m));  % Sort column m
%                 r(i, 1) = (1:N)';  % Assign ranks
%                 R(:, m) = r;  % Store ranks
%             end
% 
%             % Compute correlation matrix
%             C = corrcoef(R);
%             if det(C) <= 10^-16  % Check for singular matrix
%                 B = pinv(C);  % Use pseudo-inverse
%                 fprintf('C is singular at time step %d for node %d.\n', time_step, node);
%             else
%                 B = inv(C);  % Use regular inverse
%             end
% 
%             % Compute PRCC
%             for w = 1:M
%                 prcc(w, t_idx, node_idx) = -B(w, M+1) / sqrt(B(w, w) * B(M+1, M+1));
%             end
%         end
%     end
% end
