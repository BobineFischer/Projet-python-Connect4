## Partie 1 : Règles du Puissance 4

### Tâche 1.1 : Analyse des règles du jeu

1. Il y :
    6 rangées (de haut en bas)
    7 colonnes (de gauche à droite)
    2 couches des 2 joueurs

2. Le but est d'aligner une suite de 4 pions de même couleur sur une grille.

3. C'est matcha nul, aucun joueur se voit retirer ou ajouter des points.

4. Non elle est déja remplie.

5. Le joueur reussissant à aligner 4 pions se voit ajouter un +1, le perdant -1 et si match nul chacun obtient 0.


### Tâche 1.2 : Analyse des conditions de victoire

1. 
 
```
|_|_|_|_|_|_|_|  
|_|_|_|_|_|_|_|
|_|_|_|X|_|_|_|
|_|_|_|X|_|_|_|
|_|_|_|X|_|_|_|
|_|_|_|X|_|_|_| 

|_|_|_|_|_|_|_|  
|_|_|_|_|_|_|_|
|_|X|X|X|X|_|_|
|_|_|_|_|_|_|_|
|_|_|_|_|_|_|_|
|_|_|_|_|_|_|_| 

|_|_|_|_|_|_|_|  
|_|_|_|_|_|_|_|
|_|X|_|_|_|_|_|
|_|_|X|_|_|_|_|
|_|_|_|X|_|_|_|
|_|_|_|_|X|_|_|


|_|_|_|_|_|_|_|
|_|_|_|_|_|_|_|
|_|_|_|_|_|X|_|
|_|_|_|_|X|_|_|
|_|_|_|X|_|_|_|
|_|_|X|_|_|_|_|

```

2. Il y la direction horizontale, verticale, diagonale descendante, diagonale montante. Donc, 4 à vérifier.

3. 
  1 - Intialiser la position du pion et sa couleur

  2 - Pour les 4 directions {horizontale, verticale, diagonale descendante, diagonale montante}
        
        - Pour les 2 deplacements {on avance, on recule}
            compteur = 0

            avancer d'une case si elle existe 
                compteur += 1
            
        si compteur >= 4 
            retourner vrai

        sinon changer de sens de deplacement
    
    Si compteur >= 4 pour aucune direction
        retourner faux



## Partie 2 : Comprendre PettingZoo

### Tâche 2.1 :

1. Player_0 et Player_1

2. `env.action_space(agent)` retourne l'espace des actions possibles par l'agent et `.sample(mask)`  est une action aléatoire sur action_space donc ` action ` est un deplacement sur l'espace des états autorisés.

3. `env.agent_iter()` alterne entre les agents player_0 puis player_1 ainsi de suite. `env.step(action)` execute l'action de l'agent actuel dans l'environnemnt.

4. ` env.last()` retourne un tuple des informations concernant l'agent appelant la fonction, observation (la grille de puissance 4), reward (son dernier score), termination (s'il a perdu ou gagné le jeu), truncation (si la partie s'arrete pour une raison externe) et info.

5. L’observation retourne un tableau 2D de taille 6x7, où chaque case indique l’état (vide, player_0, playeur_1).

6. `action_mask` est un vecteur binaire où chaque element representent un action légal (respectant les règles de puissance 4) ou non. Il est important car sans cela le code effectuerait des manipulations impossibles ou inutiles.


### Tâche 2.2 : Analyse de l'espace d'observation

1. Le tableau est de forme (6, 7, 2)

2. Il s'agit de (lignes, colonnes, chaînes)

3. 1 : l'agent actuel occupe la case
   0 : l'agent n'occupe pas la case ou elle est occupée par l'agent adversaire


### Tâche 2.3 : Comprendre la représentation du plateau

``````
Agent: player_0
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .

Agent: player_1
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . . O . . .

``````

### Tâche 2.4 : Créer une boucle de jeu simple

Le script `simple_game.py` initialise un environnement avec la commande env.reset(seed=42), un plateau vide est crée.

La boucle `for agent in env.agent_iter():` indique l'on choisit un agent, commençant par `Player_O`, à tour de rôle pour qu'il joue son coup.

À chaque tour, la fonction env.last() retourne l’observation actuelle du plateau, le reward de l’agent depuis son dernier coup, et les indicateurs termination et truncation qui signalent si le jeu est terminé ou interrompu. 

Si le jeu n’est pas terminé, l’agent choisit une action aléatoire parmi les colonnes disponibles en utilisant `action_mask` fourni par l’observation, puis cette action est appliquée avec `env.step(action)`. 

Le plateau est alors mis à jour et passe le tour au prochain agent.

La boucle continue jusqu’à ce qu’un agent gagne ou que la partie se termine par égalité, draw. 
Lorsque cela se produit, le script affiche le résultat et l’environnement est fermé avec env.close().


## Partie 3 : Décomposition du problème

### Tâche 3.1 : Décomposer l'implémentation de l'agent

 **Analyse des entrées** : L'agent reçoit

- truncation ou termination; l'état d'avancement du jeu, s'il est terminé ou non 
- l'espace de coups acceptable via `observation["action_mask"]`

**Détection des coups valides** :
L'état des colonnes est caractérisé par `observation["action_mask"]`.

n-ieme valeur = 0 la colonne est remplie et que le coup n'y est pas jouable

n-ième valeur = 1 la colonne n'est pas remplie et que le coup y est pas jouable

**Sélection du coup** : 

Pour choisir un coup, l’agent peut utiliser l’action mask fourni par l’environnement afin de sélectionner uniquement les colonnes valides, et choisit aléatoirement l’une d’entre elles. Mais le mieux serait d'utiliser un algorithme heuristique effectuant le meilleur coup ou bloquant celui de l'adversaire.


**Sortie** :

L'agent doit retourner un coup (une action) choisi qui sera transmis à l'environnement, via `env.step(action)`, pour être effectué. 


### Tâche 3.2 : Conception d'algorithme - Progression

1. **Niveau 0** : _____ l'agent choisi n'importe quelle colonne même si cela peut lui être refuser par PettingZoo
2. **Niveau 1** : _____ l'agent choisi une colonne disponible dans `observation["action_mask"]`
3. **Niveau 2** : _____ l'agent cherche la première opportunité de placer 4 jetons de suite
4. **Niveau 3** : _____ l'agent peut contrer les possibles coups gagnants de l'adversaire
5. **Niveau 4** : _____ l'agent optimise son positionnement comme se placer au centre
6. **Niveau 5+** : _____ Algorithmes avancés comme minimax ou recherche arborescente Monte Carlo (MCTS)


### Tâche 3.3 : Définir l'interface de l'agent

**Class Agent** : 

- attributs : un nom, l'environnement

- méthodes :  l'initialisation, une action associée à un algorithme de choix de coup, une mise à jour après un coup d'adversaire, __str__