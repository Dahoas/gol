from abc import abstractmethod
from typing import List, Union, Tuple, Any
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
import imageio


######## GOL Impl ########

@dataclass
class GOLObject:
    """
    Implements a GOL object specified in rle and anchored in space by (x, y)
    """
    x: int  # x coordinate of upper left corner
    y: int  # y coordinat of upper left corner
    rle: str


@dataclass
class GOLState:
    state: np.array  # 2-D numpy array

    def __init__(self, state: np.array):
        assert len(state.shape) == 2
        self.state = state

    def __str__(self):
        return "".join(["".join(["O" if cell else "." for cell in row])+"\n" for row in self.state])

    def to_txt(self, file_path):
        with open(file_path, "w") as f:
            f.write(str(self))

    @classmethod
    def random_init(cls, height=100, width=100, p=[0.5, 0.5]):
        state = np.random.choice([0, 1], size=(height, width), replace=True, p=p)
        return cls(state)

    @classmethod
    def from_object(cls, structure: GOLObject, height=100, width=100):
        state = np.zeros((height, width), dtype=bool)
        lines = structure.rle.split("$")
        for i, line in enumerate(lines):
            row = []
            mul = None
            for c in line:
                if c == "!":
                    break
                if c == "o":
                    row += mul * [True] if mul else [True]
                    mul = None
                if c == "b":
                    row += mul * [False] if mul else [False]
                    mul = None
                if c.isdigit():
                    if mul is None:
                        mul = int(c)
                    else:
                        mul = 10*mul + int(c)
            state[structure.x+i, structure.y:structure.y+len(row)] += np.array(row, dtype=bool)
        return cls(state)

    def __eq__(self, other):
        return (self.state == other.state).all()


@dataclass
class GOLGame:
    trajectory: List[GOLState]

    @classmethod
    def from_gif(cls, gif_path):
        gif = imageio.get_reader(gif_path)
        # load each frame and convert from 3-channel tensor to 2-D bool matrix
        trajectory = [GOLState(np.sum(np.array(frame, dtype=bool), axis=-1, dtype=bool)) for frame in gif]
        return cls(trajectory)

    def __iter__(self):
        self.i = 0
        return self
    
    def __next__(self):
        if self.i >= len(self.trajectory):
            raise StopIteration
        else:
            state = self.trajectory[self.i]
            self.i += 1
            return state

    def __len__(self):
        return len(self.trajectory)
        
    def __get_item__(self, index):
        return self.trajectory[index]
    

######## GOL Strutures ########

class Measurement:
    """
    Defines a qualitative/quantitative measurement of a GOLGame in the Game of Life.
    """
    name: str
    description: str

    @abstractmethod
    def __call__(self, game: GOLGame) -> Any:
        pass


class GOLStructure:
    """
    A GOLObject that satisfies expected_measurements when used to initialize a GOLGame
    """
    name: str
    description: str
    object: GOLObject
    measurements: dict[str, Measurement]
    
    @abstractmethod
    def expected_measurements(self) -> bool:
        """
        Checks that the given object satisfies the expected \
        measurements for the structure.
        """
        pass