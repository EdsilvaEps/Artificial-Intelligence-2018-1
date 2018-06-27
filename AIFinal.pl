%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% TODO: inserir descrição do projeto, quando acharmos uma
%
% Colaboradores: Edson Silva, Andrezza Bonfim, Nader Hauache
% Data: 26/06/2018
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% 1. Descubra quais cláusulas podem gerar os exemplos negativos e coloque o sı́mbolo
% '∼' ao lado da cabeça para identifica-las. Justifique sua escolha.

% Obs: parent(X,Y); X = dad/mom, Y = son/daughter.
% hd(X); X has daughter (X tem filha).


~ hd(X) <- male(X), parent(Y,X). % X não tem filhos, e não está especificado que terá
% o que pode levar a exemplos negativos
~ hd(X) <- male(X), parent(X,Y). % X é pai, porém não é especificado se tem uma filha ou filhos
% o que pode levar a um exemplo negativo se Y for masculino (male(Y))
~ hd(X) <- female(X), parent(Y,X). % X não tem filhos
~ hd(X) <- male(X), parent(Y,X). % X não tem filhos
hd(X) <- female(X), parent(X,Y), female(Y).
hd(X) <- male(X), parent(Y,X), female(Y).
hd(X) <- male(X), parent(X,Y), female(Y).
~ hd(X) <- female(X), parent(Y,X), male(Y). % X não tem filhos
hd(X) <- female(X), parent(X,Y), female(Y).
~hd(X) <- male(X), parent(Y,X), parent(Y,Z). % X não tem filhos
hd(X) <- male(X), parent(X,Y), female(Y).
hd(X) <- male(X), parent(X,Y), female(Y), parent(Y,Z), male(Z).
~ hd(X) <- female(X), parent(Y,X), male(Y), parent(Z,Y), female(Z). % X não tem filhos
~ hd(X) <- female(X), parent(Y,X), male(Y), parent(Y,Z), female(Z). % X não tem filhos
~ hd(X) <- female(X), parent(Y,X), male(Y), parent(Y,Z), female(Z), parent(Z,W), male(W). % X não tem filhos
