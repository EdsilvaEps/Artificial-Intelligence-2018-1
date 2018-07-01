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


~ hd(X) <- male(X), parent(Y,X). % X é filho homem de Y. Mas X talvez não tenha filhos, e não está especificado que terá
% o que pode levar a exemplos negativos - C 1
~ hd(X) <- male(X), parent(X,Y). % X é pai de Y, porém não é especificado se tem uma filha ou filhos//mas talvez não tenha filhos - C 2
% o que pode levar a um exemplo negativo se Y for homem (male(Y)), mas pode ser verdadeiro se Y for mulher (female(Y)).
~ hd(X) <- female(X), parent(Y,X). % X não tem filhos, mas Y tem filha, pois Y é mãe/pai de X, e X é mulher. Mas não está definido se X tem filha. - C 3
~ hd(X) <- male(X), parent(Y,X). % X não tem filhos, mas Y tem filho, pois Y é mãe/pai de X. Mas não está definido se X tem filha. - C 4
hd(X) <- female(X), parent(X,Y), female(Y). % X é Mulher, e Y também é mulher. Mas X é mãe de Y. Ou seja, hd(X) é verdade.  % - C 5
~ hd(X) <- male(X), parent(Y,X), female(Y). % X é filho de Y. Y é mãe de X. Mas não está afirmado que X, que é filho de Y(mulher), tem filhas. - C 6
hd(X) <- male(X), parent(X,Y), female(Y). % - X é pai de Y. Y é mulher. Logo, X tem filha.  C 7
~ hd(X) <- female(X), parent(Y,X), male(Y). % X não tem filhos - C 8
hd(X) <- female(X), parent(X,Y), female(Y). % - C 9
~hd(X) <- male(X), parent(Y,X), parent(Y,Z). % X não tem filhos - C 10
hd(X) <- male(X), parent(X,Y), female(Y). % - C 11
hd(X) <- male(X), parent(X,Y), female(Y), parent(Y,Z), male(Z). % - C 12
~ hd(X) <- female(X), parent(Y,X), male(Y), parent(Z,Y), female(Z). % X não tem filhos - C 13
~ hd(X) <- female(X), parent(Y,X), male(Y), parent(Y,Z), female(Z). % X não tem filhos - C 14
~ hd(X) <- female(X), parent(Y,X), male(Y), parent(Y,Z), female(Z), parent(Z,W), male(W). % X não tem filhos - C 15


% modeb clauses (clausulas de corpo):
% male(X), female(X)
% parent(X,Y)

% modeh clasues (clausulas da cabeça):
% male(X)
