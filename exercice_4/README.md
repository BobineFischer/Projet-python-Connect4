# Partie 4 : Stratégie de Tests, Performance et Tournois

## Objectifs de l'exercice
L'objectif de cette partie est de valider la robustesse et la performance de nos agents avant la compétition finale. Nous avons mis en place une suite de tests complète couvrant :
1.  **Tests Unitaires :** Vérifier que le `SmartAgent` respecte ses règles heuristiques (gagner, bloquer, centre).
2.  **Tests de Performance :** Mesurer le temps d'exécution et la consommation mémoire pour respecter les contraintes (3s / 384Mo).
3.  **Tournois :** Comparer les agents entre eux sur un grand nombre de parties pour établir un classement statistique.

---

## Description des Fichiers

* **`timed_smart_agent.py`** : Contient les classes des agents.
    * `SmartAgent` : Agent heuristique (Victoire > Blocage > Centre > Aléatoire).
    * `TimedSmartAgent` : Version instrumentée du SmartAgent pour mesurer le temps et la mémoire (via `tracemalloc`).
    * `RandomAgent` : Joue uniformément au hasard.
    * `WeightedRandomAgent` : Joue au hasard mais privilégie le centre (poids statistiques).
* **`test_suite.py`** : Tests unitaires fonctionnels. Vérifie des situations de jeu spécifiques (ex: alignement de 3 pions).
* **`test_Timed_Smart_Agent.py`** : Script de profiling. Lance des centaines de parties pour calculer le temps moyen par coup et le taux de victoire.
* **`tournament.py`** : Moteur de tournoi. Fait s'affronter tous les agents en mode "Round-Robin" (chacun contre chacun) avec alternance du premier joueur.

---

## 1. Tests Unitaires (`test_suite.py`)

Nous avons implémenté des assertions pour valider les priorités du `SmartAgent`. Le script crée des plateaux artificiels pour vérifier si l'agent :

| Scénario | Résultat Attendu |
| :--- | :--- |
| **Victoire Immédiate** | L'agent détecte 3 pions alignés et complète la ligne (colonne 3). |
| **Blocage Adversaire** | L'agent détecte une menace adverse et joue pour bloquer. |
| **Priorité Centre** | Sur un plateau vide, l'agent joue au centre (colonne 3). |
| **Coup Valide** | Si aucune règle ne s'applique, l'agent joue un coup légal (pas de colonne pleine). |

**Exécution :**
```bash
python test_suite.py
