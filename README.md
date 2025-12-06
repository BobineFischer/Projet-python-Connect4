# Projet Python Connect 4

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Numpy](https://img.shields.io/badge/Numpy-Required-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## Introduction

Bienvenue dans le dépôt **Projet-python-Connect4**. Ce projet implémente un agent d'intelligence artificielle performant pour le jeu de **Puissance 4** (Connect 4).

L'objectif principal était de concevoir une IA capable de jouer en temps réel avec des contraintes de temps strictes, tout en maximisant la profondeur de recherche grâce à des techniques d'optimisation avancées comme les **Bitboards** et la recherche **PVS (Principal Variation Search)**.

---

## Fonctionnalités Clés

L'agent (`agent.py`) intègre plusieurs stratégies d'optimisation algorithmique :

### Algorithmes de Recherche
* **Principal Variation Search (PVS) :** Une variante optimisée de l'algorithme Minimax Alpha-Beta. Elle assume que le premier coup exploré est le meilleur, réduisant ainsi la fenêtre de recherche pour les coups suivants.
* **Approfondissement Itératif (Iterative Deepening) :** L'IA explore le jeu profondeur par profondeur (1, 2, 3...) jusqu'à épuisement du temps imparti, garantissant toujours une réponse valide même en cas d'interruption.
* **Table de Transposition (TT) :** Mise en cache des positions déjà évaluées (limitée à 5 millions d'entrées) pour éviter les recalculs coûteux.

### Optimisation des Performances
* **Bitboards (Opérations Binaires) :** Le plateau de jeu est représenté par deux entiers de 64 bits (un pour le joueur, un pour le masque global). Cela permet de vérifier les victoires et de générer les coups via des opérations bit à bit (`&`, `|`, `<<`) extrêmement rapides.
* **Gestion du Temps Dynamique :**
    * **Time Bank :** L'agent accumule du temps lorsqu'il joue rapidement les coups forcés, pour le réinvestir dans les phases critiques du milieu de jeu.
    * **Sécurité GC :** La taille des structures de données est contrôlée pour éviter les latences dues au Garbage Collector de Python.

### Connaissances de Jeu
* **Bibliothèque d'Ouvertures :** Les premiers coups sont joués instantanément grâce à une base de données d'ouvertures pré-calculées.
* **Heuristiques :** Évaluation positionnelle basée sur le contrôle du centre, les menaces immédiates et la parité (stratégie pair/impair pour les fins de partie).

---

## Installation et Prérequis

Ce projet nécessite **Python 3** et la bibliothèque **NumPy**.

1.  **Cloner le dépôt :**
    ```bash
    git clone [https://github.com/BobineFischer/Projet-python-Connect4.git](https://github.com/BobineFischer/Projet-python-Connect4.git)
    cd Projet-python-Connect4
    ```

2.  **Installer les dépendances :**
    ```bash
    pip install numpy
    ```

---

## Utilisation

L'agent est encapsulé dans la classe `Agent` située dans le fichier `agent.py`. Voici un exemple d'intégration :

```python
from agent import Agent
import numpy as np

# Initialisation de l'agent
ai_player = Agent()

# Exemple d'observation (format tableau numpy 6x7x2 ou dictionnaire)
# Ici, une grille vide pour l'exemple
observation = np.zeros((6, 7, 2))

# L'IA choisit une colonne (0-6)
colonne_choisie = ai_player.choose_action(observation)

print(f"L'IA a choisi de jouer dans la colonne : {colonne_choisie}")
