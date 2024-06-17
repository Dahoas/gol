from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple, Union
import numpy as np

from gol import GOLState, GOLStructure, GOLObject, GOLState
from measurements import LongTimeVelocity, BoundingBox
from run_gol import run_gol


@dataclass
class Glider(GOLStructure):
    name = "Glider"
    description = "5 cell glider with fixed velocity"
    measurements = {
                     "bounding_box": BoundingBox(time_range=100), 
                     "long_time_velocity": LongTimeVelocity(time_range=100),
                   }
    def __init__(self, object):
        self.object = object

    def expected_measurements(self) -> bool:
        gol_game = run_gol(GOLState.from_object(self.object))
        bboxes = self.measurements["bounding_box"](gol_game)
        print(bboxes)
        velocity = self.measurements["long_time_velocity"](gol_game)
        print(velocity)
        return np.array([box[1][0] - box[0][0] == 3 and box[1][1] - box[0][1] == 3 for box in bboxes]).all() and np.abs(1/4, velocity) < 1e-3