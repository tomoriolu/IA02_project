# Projet IA02 Gopher + Dodo
## PONTOIRE Julien et RENAUD Augustin


### def_types
Définition du typage du projet


### init_obj
Fichier pour les fonctions communes aux deux jeux : fonctions de conversions de coordonnées, passage de state a grid et inversement
Essai de fonction de symétrie, on ne s'en est pas servi finalement car moins efficace
Fonction de passage de state à tuple pour les caches 
Fonction pprint pour l'affichage

### GOPHER
Mode d'emploi de 
Pour coder Gopher, l'algorithme va récupérer pour le state actuel toutes les cases de l'adversaire. Il va ensuite chercher toutes les cases adjacentes à celles-ci qui sont vides. Pour ces cases, il va ensuite vérifier qu'il y a au plus une case adjacente qui est possédée par l'adversaire et aucune case en la possession du joueur. Il retourne ensuite la liste de ces cases qui sont les coups légaux.
play_gopher permet de retourner le state avec le coup joué

Stratégies disponibles :
- strategy_joueur : pour jouer en mode console
- strategy_first_legal : premier coup possible
- strategy_random_legal : random parmi les coups légaux
- strategy_alphabeta_classique_gopher : alphabeta classique
- strategy_negamax_alpha_beta_gopher : negamax est un algo alphabeta en plus optimisé. Son intérêt est donc de permettre d'augmenter la profondeur de la recherche. On a gardé les coupures alpha et beta. Il s'agit de la fonction que nous avons utilisé pour le tournoi (source utilisée pour l'algorithme : https://www.researchgate.net/figure/Enhanced-NegaMax-with-Alpha-Beta-Property-Pseudo-Code_fig4_262672371)
- strategy_negamax_indeterministe_gopher : negamax qui prends la liste des meilleurs coups possibles et en retourne un aléatoirement. Selon nous un algorithme indéterministe comme celui ci aurait été plus intéressant à utiliser pour le tournoi mais nous n'avons pas eu le temps de faire suffisamment de tests.


Fonction d'évaluations : 
Nous avons laissé nos 2 essais de fonctions d'évaluation différentes
evaluation : soustrait les nombres possible de coup des deux joueurs 
evaluation2 : valorise les coups qui mènent à plus de coups possibles


Fonction de caches : 
Nous avons laissé nos essais de fonctions de caches différentes

main : nous avons fait une boucle pour pouvoir jouer plusieurs parties et obtenir un pourcentage de victoire


### DODO
Pour coder Dodo, on reçoit un state de la part du serveur. On le convertit en tableau avec nos coordonnées (celles d'un tableau classique) qu'on appelle grid. On regarde les actions possibles en fonction du joueur (stocké dans le dictionnaire directions) pour chacune de ses pions et on en choisit une que l'on retourne. Enfin, on convertit le grid en state de coordonnées du serveur.

-> set_grid nous a servi a faire des tests

Stratégies disponibles :
- strategy_joueur : pour jouer en mode console
- strategy_first_legal : premier coup possible
- strategy_random: random parmi les coups légaux
- strategy_alphabeta_classique_dodo : alphabeta classique
- strategy_alphabeta_cache_dodo : comme le précédent mais avec un cache
- strategy_alphabeta_indeterministe_dodo : stratégie alphabeta avec un cache qui prends la liste des meilleurs coups possibles et en retourne un aléatoirement
- strategy_negamax_alpha_beta_dodo : négamax avec cache pour le dodo cette fois-ci (source : https://www.researchgate.net/figure/Enhanced-NegaMax-with-Alpha-Beta-Property-Pseudo-Code_fig4_262672371)
- strategy_monte_carlo : algorithme de recherche par simulation aléatoire. C'est cet algorithme que nous avons utilisé pour le tournoi



Fonction d'évaluations : 
Nous avons laissé nos  essais de fonctions d'évaluation différentes 
eval_coups : soustrait les nombres possible de coup des deux joueurs et retourne la valeur. Cette fonction nous a servi au début 
eval_coups2 : ajoute au principe de eval_coups une valorisation pour les coups qui permettent le moins dd coups possibles par la suite
eval_coups3 : tentative d'amélioration de la fonction précédente

Fonction de caches : 
Nous avons laissé nos 3 essais de fonctions de caches différentes

main : nous avons fait une boucle pour pouvoir jouer plusieurs parties et obtenir un pourcentage de victoire


## Lancement du programme
Pour lancer le server :
```./gndserver-1.0.2-linux -game dodo -rcolor blue -random``` pour Dodo (remplacer blue par red pour joueur en deuxième)
```./gndserver-1.0.2-linux -game gopher -rcolor blue -random``` pour Gopher 

Pour lancer une partie :
- python3 test_client.py 1 t t
Pour relancer une autre partie, changer le numéro ou supprimer le fichier server.json et relancer le server.


Pour tester nos stratégies, il suffit de changer la stratégie associée à STRAT_GOPHER ou STRAT_DODO dans test_client.py et de lancer le serveur puis une partie.


## Bilan :
Pour conclure, nous avons beaucoup aimé travailler sur ce projet et ne regrettons pas notre choix de ne pas faire de final ce semestre. Ce projet nous a permis de mettre en pratique ce que nous avons vu en cours et de découvrir beaucoup d'algorithmes utilisés dans ce type de jeux.

### Ce que nous avons réussi :
- Nous nous sommes bien organisé et nous nous y sommes pris assez tôt pour essayer plein de méthodes différentes
- Nous avons été curieux et nous avons essayé des méthodes autres que celles du cours
- Nous n'avons pas fait de coups illégaux
- Nous avons beaucoup gagné dans le tournoi

### Ce que nous aurions pu mieux faire :
- Nous aurions aimé pouvoir mieux travailler nos fonctions d'évaluations, beaucoup marche bien lorsque la stratégie est utilisé pour un joueur mais pas pour l'autre
- Nous aurions pu mieux travailler l'environnement pour simplifier le changement de fonction d'évaluation
- Nous aurions aimé avoir plus de temps pour régler les problèmes de typage que nous avons dans nos fichiers. La quasi totalité des problèmes restants vienent du fait que dans le fichier init_obj nous utilisons le type Action et cela pose donc des problèmes lorsqu'on effectue des opérations sur ce type.
