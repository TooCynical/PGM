%% Test for Graph1 DAG: M -> N -> P
M = 1; N = 2; P = 3;
A = [0,1,0;0,0,1;0,0,0];
X = [M,N,M]; Y = [P,P,N]; Z = [N,M,P];
Ctest = [1,0,0];
assert(all(Ctest == CondIndependence(A,X,Y,Z)));

%% Test for Graph2 DAG: Fig 3.8b Barber
A = 1; B = 2; C = 3; D = 4; E = 5;
Adj = [0,1,0,1,0;
     0,0,1,0,0;
     0,0,0,0,0;
     0,0,1,0,0;
     0,0,0,1,0];
X = A; Y = E; Z = C;
Ctest = 0;
assert(all(Ctest == CondIndependence(Adj,X,Y,Z)));

%% Test for Graph3 DAG: Fig 3.8a Barber
A = 1; B = 2; C = 3; D = 4; E = 5;
Adj = [0,1,0,0,0;
       0,0,0,1,0;
       0,0,0,1,0;
       0,0,0,0,1;
       0,0,0,0,0];
X = [A, B, B, B]; Y = [E, C, C, C]; Z = [B, -1, D, E];
Ctest = [1, 1, 0, 0];
assert(all(Ctest == CondIndependence(Adj,X,Y,Z)));

%% Two 3-clique Markov network graph
A = 1; B = 2; C = 3; D = 4; E = 5;
Adj = [0,1,1,0,0;
       1,0,1,0,0;
       1,1,0,1,1;
       0,0,1,0,1;
       0,0,1,1,0];
X = [A, A, B, B]; Y = [B, E, D, D]; Z = [C, -1, C, E];
Ctest = [0, 0, 1, 0];
assert(all(Ctest == CondIndependence(Adj,X,Y,Z)));
