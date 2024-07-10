Weclome to the Montecarlo simulation package!

## Metadata
This package provides a set of classes to simulate and analyze dice games using the Monte Carlo methods. This package includes three main classes
-- Die
-- Game
-- Anaylzer 

### Instalation
To install the monte carlo package onto your local computer, clone this repo onto your local space. Then in your terminal using bash, navigate to the directory where the repo has been cloned, then run... 
```bash
pip install .
```
## Using the MonteCarlo Package
Step 1: Import the package/classes
```python
from montecarlo import Die, Game, Analyzer
```
Step 2: Must import both numpy and pandas to use this package!

## Synopsis
### Usage of Die Class
```python
import numpy as np
from montecarlo import Die

faces = np.array([1, 2, 3, 4, 5, 6])
die = Die(faces)
die.change_weight(3, 2.5)
outcome = die.roll(5)
print(outcome)
```

### Usage of Game Class
```python
from montecarlo import Die, Game

die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
die2 = Die(np.array([1, 2, 3, 4, 5, 6]))
game = Game([die1, die2])
game.play(10)
results = game.show_results()
print(results)
```
### Usage of Analyzer Class
```python
from montecarlo import Die, Game, Analyzer

die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
die2 = Die(np.array([1, 2, 3, 4, 5, 6]))
game = Game([die1, die2])
game.play(100)
analyzer = Analyzer(game)
jackpot_count = analyzer.jackpot()
combo_counts = analyzer.combo_counts()
print(f"Jackpot count: {jackpot_count}")
print(combo_counts)
```

## Module API

Die Class:
- __init__(self,faces:np.ndarray): Initializes the Die object with faces
- change_weight(self, face: any, weight:float): Changes weight of a signle face on your die object
- roll(self,num_rolls:in =1): rolls die one or more times
- show(self): Shows the current state of the dice and returns private data frame consisting of faces and weights for the Die object

Game Class: 
- __init__(self,dice: List[Die]): initializes the Game object with a list of dice.
- play(self,num_rolls:int): plays the game by rolling all dice a specified number of times
- show_results(self, form:str = 'wide'): Returns the results of the game in wide or narrow form (argument must be lowercase)

Analyzer Class
- __init__(self,game: Game): Initializes the Analyzer object with a Game object
- jackpot(self): Computes the number of times all faces rolled are the same
- face_counts_per_roll(self): Computes the counts of each face per roll
- combo_counts(self): Computes the distinct combinations of faces rolled
- permutation_counts(self): Computes the distinct permutations of faces rolled 




