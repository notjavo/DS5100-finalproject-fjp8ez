"""
Monte Carlo Simulation Package
WARNING: Must need Numpy and Pandas installed and loaded before using montecarlo

*import numpy as np*
*import pandas as pd*

This package includes the following modules:
- Die: A class to represent a die with faces and weights.
- Game: A class to handle multiple dice and play a game with them.
- Analyzer: A class to analyze the results of the game.

Example usage:
    from montecarlo import Die, Game, Analyzer

    # Create a die
    die = Die(faces=np.array([1, 2, 3, 4, 5, 6]))

    # Create a game with two dice
    game = Game(dice=[die, die])

    # Play the game
    game.play(num_rolls=1000)

    # Analyze the results
    analyzer = Analyzer(game=game)
    print(analyzer.face_counts())
"""

print("You have officially installed the Monte Carlo package!")
from .montecarlo import Die, Game, Analyzer

print("you have offically installed the montecarlo package!")
from .montecarlo import Die, Game, Analyzer
