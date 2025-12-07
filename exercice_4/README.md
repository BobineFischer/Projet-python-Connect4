## Partie 1 : Conception de stratégie de test

### Tâche 4.1 : Concevoir votre plan de test

#### 1.1 Que tester ?

Listez les différentes catégories de tests :

- **Tests fonctionnels** : L'agent fonctionne-t-il correctement ?
  - [ ] Sélection de coup valide
  - [ ] Respect du masque d'action
  - [ ] Gestion de la fin de partie
  - [ ] Gestion des états illégaux (plateau invalide, taille incorrecte…)
  - [ ]  Réinitialisation correcte entre les parties

- **Tests de performance** : Est-il rapide et efficace ?
  - [ ] Temps maximum par coup < 100 ms
  - [ ] Utilisation de la mémoire

- **Tests stratégiques** : Joue-t-il bien ?
  - [ ] Gagne contre un agent aléatoire
  - [ ] Bloque les menaces évidentes
  - [ ] Gagne contre un agent heuristique simple
  - [ ] Taux de victoire stable

#### 1.2 Comment tester ?

- **Coups valides** : Créer des états de plateau spécifiques et vérifier que l'agent choisit des coups légaux
- **Fin de partie** : Créer des états de plateau spécifiques et vérifier que l’agent n’essaie pas de jouer après la fin et renvoie un comportement cohérent (aucune action ou message d'arrêt).
- **Blocage des menaces** : Créer des situations avec 3 pions alignés adverses vérifier que l'agent choisit la colonne qui bloque la victoire adverse.
- **Taux de victoire** : Jouer N parties et mesurer le pourcentage de victoires
- **Tournoi** : Faire jouer plusieurs agents dans un tournoi
- **Performance** : Utiliser `time.time()` et `tracemalloc` pour mesurer les ressources

#### 1.3 Critères de succès

- L'agent doit gagner > 80% contre RandomAgent et > 60% contre WeightedAgent
- Temps moyen par coup < 0.1 secondes
- Utilisation de mémoire < 10 MB
- Fonctionnalité correcte : toujours choisir des coups légaux, gérer correctement la fin de partie et les états invalides
- Réinitialisation correcte entre les parties
- Taux de victoire stable

**Exécution :**
```bash
python test_suite.py

