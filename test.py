import unittest
import numpy as np

from temp_experiment import compute_entropy
from gol import GOLState, GOLGame, GOLStructure, GOLObject
from structures import Glider

class TestMathFunctions(unittest.TestCase):

    def xtest_entropy(self):
        print("ENTROPY TEST")
        x = [0, 1]
        p = [0.3, 0.7]
        grid = np.random.choice(x, (100, 100), replace=True, p=p)
        print("Shape: ", grid.shape)
        print("Mean ones: ", np.mean(grid))
        ent = compute_entropy(grid)
        print("Entropy: ", ent)

    def xtest_gol_state(self):
        # test to_txt
        p = [0.3, 0.7]
        grid = GOLState.random_init(p=p).state
        print(grid)
        gol_state = GOLState(grid)
        gol_state.to_txt("artifacts/initial_state.txt")

        # test __eq__
        gol_1 = GOLState.random_init()
        gol_2 = GOLState.random_init()
        print(gol_1 == gol_2)
        print(gol_1 == gol_1)

        # test from_structure
        glider = GOLStructure(3, 3, "bob$2bo$3o!")
        gol_state = GOLState.from_structure(glider, height=7, width=7)
        print(gol_state.state)
    
    def test_glider(self):
        glider_object = GOLObject(x=0, y=0, rle="bob$2bo$3o!s")
        glider = Glider(object=glider_object)
        assert glider.expected_measurements()



# If the script is run directly, run the tests
if __name__ == '__main__':
    unittest.main()
