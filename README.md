# Projet Python - Connect 4 (Puissance 4)


## Description du Projet

Ce projet a été réalisé dans le cadre du cours de Python par Houlda Bisse Zoobo et Baiyi REN. L'objectif est de développer un agent autonome capable de jouer au **Puissance 4 (Connect 4)** de manière optimale.

Le projet s'appuie sur le framework **PettingZoo** pour la simulation de l'environnement et vise la compétition sur la plateforme **ML-Arena**, avec des contraintes strictes :
* **Temps :** Max 3 secondes par coup.
* **Mémoire :** Max 384 Mo.
* **CPU :** 1 cœur.

---

## Progression du Projet

Nous avons suivi une approche incrémentale, décomposée en 5 exercices, pour passer d'une compréhension basique à une IA compétitive.

### Exercice 1 : Analyse et Modélisation
* **Objectif :** Comprendre l'environnement PettingZoo et les règles.
* **Analyse :**
    * Le plateau est une grille de 6 rangées x 7 colonnes.
    * L'observation est une matrice `(6, 7, 2)` représentant les pions des deux joueurs.
    * L'importance de l'`action_mask` pour filtrer les coups illégaux (colonnes pleines).

### Exercice 2 : Agent Aléatoire (Baseline)
* **Objectif :** Créer un agent jouant des coups valides au hasard pour établir une base de performance.
* **Résultats de l'analyse statistique (sur 600 parties) :**
    * **Avantage du premier joueur (Player 0) :** Gagne entre 50% et 70% des parties.
    * **Durée moyenne :** ~22 coups par partie.
    * **Matchs nuls :** Très rares (< 3%).

### Exercice 3 : Agent "Smart" (Heuristique)
* **Objectif :** Implémenter des règles logiques simples.
* **Stratégie implémentée :**
    1.  **Victoire immédiate :** Si un coup permet d'aligner 4 pions, le jouer.
    2.  **Blocage :** Si l'adversaire peut gagner au prochain tour, le bloquer.
    3.  **Occupation du centre :** Privilégier la colonne centrale (plus d'opportunités d'alignements).

### Exercice 4 : Tests et Tournois (Validation)
* **Objectif :** Mise en place d'une suite de tests (Pytest) et d'un script d'arène pour faire s'affronter nos différentes versions d'agents et valider les améliorations.

### Exercice 5 : Agent Avancé (Minimax & Optimisations)
* **Objectif :** L'agent final soumis sur ML-Arena (`agent.py`), avec nom d'agent: **SmokeFish1.3**
* **Technologies utilisées :**
    * **Bitboards :** Utilisation d'entiers 64-bits pour représenter le plateau, permettant des calculs de victoire ultra-rapides via opérations binaires.
    * **PVS (Principal Variation Search) :** Amélioration de l'Alpha-Beta pour explorer l'arbre de jeu plus efficacement.
    * **Iterative Deepening :** Recherche progressive pour garantir une réponse valide même si le temps est écoulé.
    * **Gestion du Temps :** Système de "Time Bank" pour accumuler du temps sur les coups faciles et réfléchir plus longtemps aux moments critiques.

---

## Installation et Utilisation

### Prérequis
Le projet nécessite Python 3.8+ et les bibliothèques suivantes :

```bash
pip install pettingzoo[classic] numpy pytest
