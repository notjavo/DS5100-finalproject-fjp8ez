import numpy as np
import pandas as pd

class Die:
    """
    This class represents a die with N faces and W weights.
    """
    def __init__(self, faces):
        """
        This init function initializes the Die object with corresponding faces and weights.
        """
        #code below is checking to see if faces are indeed a Numpy array
        if not isinstance(faces, np.ndarray):
            raise TypeError("Faces must be a NumPy array")
        
        #Code below is checking if the elements in faces are unique
        if len(faces) != len(set(faces)):
            raise ValueError("Faces must contain unique values")
        
        #Initialize the faces and weights
        self.faces = faces
        self.weights = np.ones(len(faces))

        #Lastly, the code below is storing the faces and weights in a DataFrame using pandas
        self.die_df = pd.DataFrame({'faces': self.faces, 'weights': self.weights})

    def change_weight(self, face, weight):
        '''
        This method is used to change the wieght of a single face on the die

        Parameters:
        face: The face whos weight needs to be changed
        weight: The new weight of the face (signaled by a Float)
        '''
        #Code below checks to see if the face is valid
        if face not in self.faces:
            raise IndexError("Face is not found on the die")
        #Check if weight is a valid numer (int or float)
        if not isinstance(weight, (int,float)) or weight <= 0:
            raise TypeError("Weight is wrong type or weight must be a positive number")
        self.die_df.loc[self.die_df['faces'] == face, 'weights'] = weight


    def roll(self, num_rolls=1):
        '''
        This method was created to roll the die one or more times

        Parameters:
        num_rolls(int): The number of times to roll the die

        Returns:
        List: A list of outcomes from the rolles '''

        #Code first checks if num_rolls entered is a valid integer 
        if not isinstance(num_rolls,int) or num_rolls <= 0:
            raise TypeError ("Number of rolls given must be an integer and a positive numnber")
        
        # Code below rolls the die using the weights specified 
        outcomes = np.random.choice(self.die_df['faces'], size=num_rolls, p=self.die_df['weights']/self.die_df['weights'].sum())
        return outcomes.tolist()
    

    def show(self):
        '''
        This method shows the current state of the die

        Returns:
        Data Frame: A copy of the private DataFrame with faces and weights '''

        return self.die_df.copy()

class Game:
    ''' This class represents a game consisting of rolling one or more similar dice '''
    def __init__(self,dice):
        '''
        Initializes the Game object with a list of Die objects.

        Parameters:
        dice (list): a list of already instantiated similar Die objects 
        '''
        # Code below checks if the dice list contains only Die objects
        if not all (isinstance(die,Die) for die in dice):
            raise TypeError("All items present in the dice list must be Die objects")
        
        #Code below initializes the list of dice
        self.dice = dice

        #Initialize a DataFrame to store the results of the most recent play
        self._play_df = pd.DataFrame()

    def play(self,num_rolls):
        '''
        Plays the game by rolling all of the dice a given number of time
        Parameters:
        num_rolls (int): The number of times the dice should be rolled
        '''
        #Code below checks to see if number of rolls is an integer, if not, raises a type error
        if not isinstance(num_rolls,int) or num_rolls<=0:
            raise TypeError("Number of rolls should be a positive integer")
        
        #Roll each die and store the outcome
        roll = {f'Die_{i}': die.roll(num_rolls) for i, die in enumerate(self.dice)}

        #Convert results to a DataFrame in wide format
        self._play_df = pd.DataFrame(roll)

    def show(self, form='wide'):
        '''
        Shows the results of the most recent play 
        
        parameters: 
        form (str): The format in which to return the results (input 'wide' or 'narrow')
        ** Form is automatically set to wide but the user can change to narrow if needed**

        Returns:
        DataFrame: The results of the most recent play.

        '''

        #Code below validates the form parameter 
        if form not in ['wide','narrow']:
            raise ValueError("'form must be in either 'wide' or 'narrow' format")
        
        if form == 'wide':
            return self._play_df
        else:
            return self._play_df.stack().reset_index(name='outcome').rename(columns={'level_0': 'roll_number', 'level_1': 'die_number'})
                            
        

class Analyzer:
    """
    A class to analyze the results of a single game and compute various descriptive statistical properties about it.
    """
    
    def __init__(self, game):
        """
        Initializes the Analyzer object with a Game object.
        
        Parameters:
        game (Game): A game object whose results are to be analyzed.
        """
        # Check if the game parameter is an instance of Game
        if not isinstance(game, Game):
            raise ValueError("The input parameter must be a Game object")
        
        # Initialize the game object
        self.game = game
    
    def jackpot(self):
        """
        Computes how many times the game resulted in a jackpot.
        
        A jackpot is a result in which all faces are the same.
        
        Returns:
        int: The number of jackpots.
        """
        # Check if the game has been played
        if self.game._play_df.empty:
            return 0
        
        # Compute the number of jackpots
        jackpots = (self.game._play_df.nunique(axis=1) == 1).sum()
        return jackpots
    
    def face_counts(self):
        """
        Computes how many times a given face is rolled in each event.
        
        Returns:
        DataFrame: A DataFrame with the roll number as index, face values as columns, and count values in the cells.
        """
        # Check if the game has been played
        if self.game._play_df.empty:
            return pd.DataFrame()
        
        # Compute the face counts per roll
        face_counts = self.game._play_df.apply(pd.Series.value_counts, axis=1).fillna(0).astype(int)
        face_counts.index.name = 'roll_number'
        return face_counts
    
    def combo_counts(self):
        """
        Computes the distinct combinations of faces rolled, along with their counts.
        
        Combinations are order-independent and may contain repetitions.
        
        Returns:
        DataFrame: A DataFrame with a MultiIndex of distinct combinations and a column for the associated counts.
        """
        # Check if the game has been played
        if self.game._play_df.empty:
            return pd.DataFrame()
        
        # Compute the combinations and their counts
        combos = self.game._play_df.apply(lambda x: tuple(sorted(x)), axis=1).value_counts().reset_index()
        combos.columns = ['combo', 'count']
        combos.set_index('combo', inplace=True)
        return combos
    
    def permutation_counts(self):
        """
        Computes the distinct permutations of faces rolled, along with their counts.
        
        Permutations are order-dependent and may contain repetitions.
        
        Returns:
        DataFrame: A DataFrame with a MultiIndex of distinct permutations and a column for the associated counts.
        """
        # Check if the game has been played
        if self.game._play_df.empty:
            return pd.DataFrame()
        
        # Compute the permutations and their counts
        perms = self.game._play_df.apply(tuple, axis=1).value_counts().reset_index()
        perms.columns = ['permutation', 'count']
        perms.set_index('permutation', inplace=True)
        return perms
