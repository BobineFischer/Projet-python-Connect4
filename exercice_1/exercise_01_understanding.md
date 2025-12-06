# Activité 1 : Comprendre le Puissance 4 et le framework Python PettingZoo

## Objectifs d'apprentissage

- Comprendre les règles du Puissance 4 et les conditions de victoire
- Apprendre comment PettingZoo représente les états du jeu
- Analyser l'espace d'observation et l'espace d'action
- Décomposer le problème en tâches algorithmiques

## Partie 1 : Règles du Puissance 4

### Tâche 1.1 : Analyse des règles du jeu

Répondez aux questions suivantes dans un fichier texte ou un document markdown :

1. Quelles sont les dimensions d'un plateau de Puissance 4 ?
2. Comment un joueur gagne-t-il la partie ?
3. Que se passe-t-il si le plateau est complètement rempli sans gagnant ?
4. Un joueur peut-il placer un pion dans une colonne qui est déjà pleine ?
5. Quels sont les résultats possibles d'une partie ?

### Tâche 1.2 : Analyse des conditions de victoire

Listez toutes les différentes façons dont un joueur peut gagner au Puissance 4 :

1. Dessinez un diagramme montrant les quatre motifs de victoire différents
2. Pour une position donnée, combien de directions doivent être vérifiées pour une victoire ?
3. Pour chacune de ces directions, quel est l'algorithme pour vérifier l'alignement de 4 pions ? Décrire l'algorithme sans le coder (pseudo-code)

**Indice** : Réfléchissez à la façon dont vous vérifieriez chaque position après avoir placé un pion.

## Partie 2 : Comprendre PettingZoo

### Tâche 2.1 : Lire la documentation

Lisez la [documentation PettingZoo de Puissance 4](https://pettingzoo.farama.org/environments/classic/connect_four/) et répondez à ces questions :

1. Quels sont les noms des deux agents dans l'environnement ?
2. Que représente la variable `action` dans le code proposé par la documentation ? Quel est son type ?
3. Que fait `env.agent_iter()` et `env.step(action)` ?
4. Quelles informations sont retournées par `env.last()` ?
5. Quelle est la structure de l'observation retournée ?
6. Qu'est-ce qu'un "action mask" et pourquoi est-il important ?

### Tâche 2.2 : Analyse de l'espace d'observation

Créez un script appelé `explore_observations.py` avec le code suivant :

```python
from pettingzoo.classic import connect_four_v3
import numpy as np

# TODO: Create environment
env = connect_four_v3.env()
env.reset(seed=42)

# TODO: Get first observation
for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    if termination or truncation:
        break

    # TODO: Print the observation structure
    print("Agent:", agent)
    print("Observation keys:", observation.keys())
    print("Observation shape:", observation['observation'].shape)
    print("Action mask:", observation['action_mask'])

    # TODO: Take a random action (column 3)
    env.step(3)
    break

env.close()
```

Répondez à ces questions :

1. Quelle est la forme du tableau d'observation ?
2. Que représente chaque dimension ?
3. Quelles sont les valeurs possibles dans le tableau d'observation ?

### Tâche 2.3 : Comprendre la représentation du plateau

**Exercice** : Créez un script qui visualise l'état du plateau :

```python
from pettingzoo.classic import connect_four_v3
import numpy as np

def print_board(observation):
    """
    Print a human-readable version of the board

    observation: numpy array of shape (6, 7, 2)
        observation[:,:,0] = current player's pieces
        observation[:,:,1] = opponent's pieces
    """
    # TODO: Implement this function
    # Hint: Loop through rows and columns
    # Use symbols like 'X', 'O', and '.' for current player, opponent, and empty
    pass

# Test your function
env = connect_four_v3.env()
env.reset(seed=42)

for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    if termination or truncation:
        break

    print(f"\nAgent: {agent}")
    print_board(observation['observation'])

    # Make a few moves to see the board change
    env.step(3)
    if agent == env.agents[0]:
        break

env.close()
```

### Tâche 2.4 : Créer une boucle de jeu simple

Pour consolider votre compréhension, créez un jeu simple où les deux joueurs jouent aléatoirement :

```python
# simple_game.py
from pettingzoo.classic import connect_four_v3

env = connect_four_v3.env(render_mode="human") # ou render_mode="rdb_array" ou bien None
env.reset(seed=42)

for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    if termination or truncation:
        action = None
        if reward == 1:
            print(f"{agent} wins!")
        elif reward == 0:
            print("It's a draw!")
    else:
        # Take a random valid action
        mask = observation["action_mask"]
        action = env.action_space(agent).sample(mask)
        print(f"{agent} plays column {action}")

    env.step(action)

input("Press Enter to close...")
env.close()
```

Exécutez ce script et observez comment la partie progresse. Ce sera la base pour vos propres agents !

## Partie 3 : Décomposition du problème

### Tâche 3.1 : Décomposer l'implémentation de l'agent

Un agent doit choisir quelle colonne jouer. Décomposez cela en sous-tâches :

1. **Analyse des entrées** : Quelles informations l'agent reçoit-il ?
2. **Détection des coups valides** : Comment déterminez-vous quelles colonnes sont jouables ?
3. **Sélection du coup** : Quel algorithme utiliserez-vous pour choisir un coup ?
4. **Sortie** : Que doit retourner l'agent ?

Créez un document avec vos réponses.

### Tâche 3.2 : Conception d'algorithme - Progression

A votre avis, quels seraients les algorithmes à implémenter dans les agents (différentes stratégies de jeu), par ordre de complexité croissante :

1. **Niveau 0** : _____ (Agent le plus simple possible)
2. **Niveau 1** : _____ (Légèrement plus intelligent - éviter les coups invalides)
3. **Niveau 2** : _____ (Chercher des opportunités immédiates)
4. **Niveau 3** : _____ (Jeu défensif)
5. **Niveau 4** : _____ (Positionnement stratégique)
6. **Niveau 5+** : _____ (Algorithmes avancés)

**Objectif** : Vous devriez avoir une progression de "aléatoire" à "expert". Cela guidera votre implémentation dans les exercices suivants.

### Tâche 3.3 : Définir l'interface de l'agent

Dans la suite, l'objectif est d'implémenter des agents selon les stratégies décrites ci-dessus. Chaque agent doit ainsi choisir une action en fonction de l'état du jeu (c-à-d la position des jetons). L'idée est d'implémenterez une classe `Agent` par stratégie.

Quel serait le squelette de cette classe (attributs, méthodes, etc.) ?

## Livrables

À la fin de cet exercice, vous devriez avoir :

1. ✅ Un document `README.md` répondant à toutes les questions sur les règles du jeu et les conditions de victoire
2. ✅ Un script (`explore_observations.py`) qui explore l'espace d'observation
3. ✅ Une fonction `print_board()` qui visualise l'état du jeu
4. ✅ Un texte de décomposition du problème avec votre plan de progression d'agent
5. ✅ Un squelette de classe d'agent avec des méthodes documentées

## Questions d'auto-vérification

Avant de passer à l'exercice 2, assurez-vous de pouvoir répondre :

1. Comment le plateau est-il représenté dans l'observation de PettingZoo ?
2. Quel est l'espace d'action pour le Puissance 4 ?
3. Comment déterminez-vous si une colonne est jouable ?
4. Quelles sont les quatre directions à vérifier pour une victoire ?
5. Quelles informations un agent reçoit-il lorsqu'il est temps de faire un coup ?

## Prochaines étapes

Une fois que vous comprenez le problème et le framework, passez à :
- [Exercice 2 : Implémenter un agent aléatoire](./exercise_02_random_agent.md)

## Ressources supplémentaires

- [Documentation PettingZoo de Puissance 4](https://pettingzoo.farama.org/environments/classic/connect_four/)
- [Indexation de tableaux NumPy](https://numpy.org/doc/stable/user/basics.indexing.html)

## Conseils

- **Visualisez** : Dessiner le plateau sur papier aide à comprendre le système de coordonnées
- **Expérimentez** : Exécutez le code plusieurs fois et observez différents états de jeu
- **Demandez "Pourquoi ?"** : Comprendre les décisions de conception dans PettingZoo vous aidera plus tard
- **Documentez** : Notez votre compréhension - ce sera utile pour l'implémentation
