import unittest
import numpy as np
import pandas as pd
from montecarlo import Die, Game, Analyzer

class TestDie(unittest.TestCase):
    def setUp(self):
        self.faces = np.array([1, 2, 3, 4, 5, 6])
        self.die = Die(self.faces)

    def test_initialization(self):
        self.assertTrue(isinstance(self.die.faces, np.ndarray))
        self.assertEqual(len(self.die.faces), len(self.faces))
        self.assertEqual(len(self.die.weights), len(self.faces))
        self.assertTrue((self.die.weights == 1).all())

    def test_change_weight(self):
        self.die.change_weight(1, 5)
        self.assertEqual(self.die.die_df.loc[self.die.die_df['faces'] == 1, 'weights'].values[0], 5)

    def test_roll(self):
        rolls = self.die.roll(10)
        self.assertEqual(len(rolls), 10)
    
    def test_show(self):
        self.die.roll(10)
        die_df = self.die.show()
        self.assertIsInstance(die_df, pd.DataFrame)
        expected_columns = ['faces', 'weights']
        self.assertTrue(all(col in die_df.columns for col in expected_columns))
        self.assertEqual(len(die_df), len(self.faces))

        
class TestGame(unittest.TestCase):
    def setUp(self):
        self.faces = np.array([1, 2, 3, 4, 5, 6])
        self.dice = [Die(self.faces) for _ in range(5)]
        self.game = Game(self.dice)

    def test_initialization(self):
        self.assertTrue(all(isinstance(die, Die) for die in self.game.dice))

    def test_play(self):
        self.game.play(10)
        self.assertEqual(len(self.game._play_df), 10)

    def test_show(self):
        self.game.play(10)
        df = self.game.show()
        self.assertEqual(df.shape, (10, 5))

class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        self.faces = np.array([1, 2, 3, 4, 5, 6])
        self.dice = [Die(self.faces) for _ in range(5)]
        self.game = Game(self.dice)
        self.game.play(10)
        self.analyzer = Analyzer(self.game)

    def test_init(self):
        with self.assertRaises(ValueError):
            Analyzer("not_a_game_object")

    def test_jackpot(self):
        self.game._play_df.iloc[0] = [1, 1, 1, 1, 1]
        self.assertEqual(self.analyzer.jackpot(), 1)

    def test_face_counts(self):
        face_counts = self.analyzer.face_counts()
        self.assertIsInstance(face_counts, pd.DataFrame)
        self.assertEqual(face_counts.shape[0], 10)  # 10 rolls
        self.assertEqual(face_counts.shape[1], len(self.faces))  
        self.assertTrue((face_counts.sum(axis=1) == len(self.dice)).all())

    def test_combo_counts(self):
        combo_counts = self.analyzer.combo_counts()
        self.assertGreater(len(combo_counts), 0)

    def test_permutation_counts(self):
        permutation_counts = self.analyzer.permutation_counts()
        self.assertGreater(len(permutation_counts), 0)

if __name__ == '__main__':
    unittest.main()