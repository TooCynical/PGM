function C = CondIndependence(A,X,Y,Z)
% Returns true if X and Y are conditionally independent given Z and 
% adjacency matrix A.
%
% YOUR TASK:
%   Using the provided functions parents.m and ancestors.m, write the
%   code for graph moralization and conditional independence test. Follow
%   the 4-step recipe provided in the exercise sheet.
%   
% INPUTS:
%   A:   adjacency matrix of size [nNodes x nNodes]
%   X,Y: 1-D matrix containing list of variables, can be an array or a single integer ( > 0 )
%   Z:   1-D matrix containing the conditionals, can be an array, single integer or empty (-1).
% OUTPUT:
%   C:   1-D matrix containing 1 if P(Xi,Yi|Zi) = P(Xi|Zi)P(Yi|Zi) else 0
%
% Author: Soumajit
% Email:  majumder@cs.uni-bonn.de
% Date:   01.11.2016

%Tests

%% Check validity of inputs
Zc = Z; Zc(Z == -1) = [];
assert((size(A,1) >= length(unique(X))) ...
    && (size(A,1) >= length(unique(Y))) ...
    && (size(A,1) >= length(unique(Zc))));
assert((numel(X) == numel(Y)) ...
    && (numel(Z) == numel(X)));
assert(size(A,1) == size(A,2));
assert(all(X>0) && all(Y>0));

%% Your Code Here

C = zeros(1,numel(X));
n = size(A,1);

for var = 1:1:numel(X)
    
    % Current test samples
    u = [X(var) Y(var) Z(var)];
    u(u == - 1) = [];
    x = X(var);
    y = Y(var);
    z = Z(var);
    
    % Copy A for modification.
    T = A;
    
    % Check if the graph is directed, if so, moralize the graph.
    if (isDAG(A))
      % Find ancestors (including u).
      a = sort(unique(union(Ancestors(A, u), u)));
      % Set all edges of A that are not between ancestors to zero.
      T = zeros(n);
      T(a, a) = A(a, a);
      
      % Moralize T.
      T = Moralize(T);      
    end
    
    % Remove all edges neighbouring z.
    if (z > 0)
      T(z, :) = zeros(1, n);
      T(:, z) = zeros(n, 1);
    end
        
    % Find the connections between x and y. To do this, first add an edge
    % between each vertex and itself. Then compute T^n, in which the (i,j)-th
    % entry is equal to the amount of paths of length n between i and j.
    T = T + eye(n);
    T = T^n;
      
    % If there are no paths between x and y, they are independent.
    if (T(x, y) == 0)
      C(var) = 1;
    else
      C(var) = 0; 
    end
end
end

%% Helper Functions
function t = isDAG(A)
% Returns whether A is the adjacency matrix of a directed graph (i.e. not sym.)
  t = ~all((A == A')(:));
end

function T = Moralize(T)
% Returns the moralization of the given DAG T.

% Find new edges N to add (between nodes with shared child).
n = size(T)(1);
N = zeros(n);
for i = [1 : n]
  if (nnz(T(:, i)) > 1)
    % P consists of all pairs of nonzero entries of the ith column of T
    P = nchoosek(find(T(:, i))', 2);
    for j = [1 : size(P)(1)]
      N(P(j, 1), P(j, 2)) = 1;
    end
  end
end

% Add new edges and undirect the graph, using + as an OR operator.
T = T + N;
T = T + T';
end


function p =  Parents(A,x)
% Returns the parents of a single variable 'x' given adjacency matrix A
% USTE: p = Parents(A,x)
p = []; 
for i = x(:)'
    t = find(A(:,i));
    p = [p t(:)']; 
end
p = unique(p);
end

function a = Ancestors(A,x)
% Returns the ancestors of variable x given adjacency matrix A
% Recursively calls Parents.
% USTE: a = Ancestors(A,1);

done = false;
a    = Parents(A,x); % start with the parents of x
while ~done
    aold = a;
    a    = union(a,Parents(A,a));       % include the parents of the current ancestors
    done = isempty(setdiff(a,aold));    % if this doesn't introduce any more nodes, we're done
end
a    = setdiff(a,x);
end
