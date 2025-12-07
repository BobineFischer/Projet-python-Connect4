## Partie 1 : Planifier votre stratégie

### Tâche 3.1 : Conception de la stratégie

1. 
    - Jouer le coup gagnant
    - Stopper le coup gagnant d'un adversaire
    - Opter pour des actions faisant gagner

.

2.
    - Les actions de l'agent doivent rester dans la zone des actions valides
    - L'agent ne peut pas jouer 2 fois de suite
    - L'agent ne peut pas placer plus d'un pion à la fois

.

3.
    - Favoriser les alignements verticales car plus faciles à réaliser
    - Prévoir la manière dont l'adversaire pourrait utiliser nos coups à son avantage



### Tâche 3.2 : Conception de la stratégie

choose_action()

    ├── get_valid_actions() - Get list of playable columns

    ├── check_winning_move() - Can I win immediately?

    ├── check_blocking_move() - Can opponent win next turn?

    ├── evaluate_position() - Which move is strategically best?

    └── fallback_move() - Default choice if nothing special
