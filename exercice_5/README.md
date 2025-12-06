# Agent IA - Puissance 4

Ce projet implémente un agent autonome performant pour le jeu de Puissance 4. L'objectif était de développer une IA capable de jouer en temps réel (sous contrainte de temps stricte) tout en maintenant une profondeur de recherche élevée grâce à des optimisations algorithmiques avancées.

## Fonctionnalités Clés

L'agent repose sur une architecture **Minimax** améliorée par plusieurs techniques d'optimisation :

* **Représentation par Bitboards :** L'état du jeu est stocké sous forme d'entiers 64 bits (et non de tableaux 2D), permettant d'effectuer les opérations (vérification de victoire, génération de coups) via des opérations bit-à-bit (`&`, `|`, `<<`) extrêmement rapides.
* **Principal Variation Search (PVS) :** Une amélioration de l'élagage Alpha-Beta qui part du principe que le premier coup exploré est souvent le meilleur, permettant de réduire la fenêtre de recherche pour les coups suivants.
* **Iterative Deepening (Approfondissement Itératif) :** L'IA explore le jeu à la profondeur 1, puis 2, puis 3, etc., jusqu'à épuisement du temps imparti. Cela garantit qu'une décision est toujours prête, même si le calcul est interrompu.
* **Table de Transposition (TT) :** Mise en cache des positions déjà analysées pour éviter de recalculer des branches identiques de l'arbre (limitée à 5 millions d'entrées pour gérer la mémoire).

## Choix Techniques & Optimisations

### 1. Gestion du Temps (Time Management)
Pour éviter les pénalités de temps (Timeout), l'agent utilise une stratégie dynamique :
* **Temps de base :** ~1.95 secondes par coup.
* **Time Bank :** Si l'agent joue plus vite que prévu sur des coups "faciles" (ou forcés), il accumule du temps en réserve pour réfléchir plus longtemps (jusqu'à 2.4s) lors des phases critiques du milieu de partie.
* **Sécurité GC :** La taille de la table de hachage est contrôlée pour éviter les latences dues au *Garbage Collector* de Python.

### 2. Heuristiques d'Évaluation
Lorsque la profondeur maximale n'est pas atteinte, la fonction d'évaluation prend en compte :
* Le contrôle du centre.
* Les menaces immédiates (alignements de 3 pions).
* **La parité (Odd/Even strategy) :** Une analyse des cases paires/impaires pour anticiper les situations de *Zugzwang* en fin de partie.

### 3. Bibliothèque d'Ouvertures (Opening Book)
Les premiers coups sont joués instantanément grâce à une bibliothèque pré-calculée couvrant les ouvertures classiques, permettant d'économiser du temps pour la suite.

## Installation et Utilisation

### Prérequis
Le projet nécessite `numpy`.

```bash
pip install numpy