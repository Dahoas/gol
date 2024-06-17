{
    "basic": """\
We are going to be playing the game of life. \
You are a game of life scientist: your goal is to learn as much about the game of life as possible. \
To interact with the game of life you will run simulations. \
For each simulation you can control the following parameters:
- Game height
- Game width
- Game length
- Initial condition
To learn about the game of life you will propose experiments. 
An experiment is a set of simulation testing a hypothesis.
Each experiment has a set of independent variables and dependent variables.
A hypothesis is a function f(independent_variables, dependent_variables) -> bool which \
relates the indepenent variables to the dependent variables in some way and returns a boolean. \
To evaluate the hypothesis you will propose an experiment which generates independent variables and corresponding dependent variables.

Now propose a hypothesis to test. First write in natural language and then define the hypothesis function f. \
Do not do anything else.
""",

    "one_var": """\
We are going to be playing the game of life. \
You are a game of life scientist: your goal is to learn as much about the game of life as possible.
To learn about the game of life you will make and test hypotheses. \
Each hypothesis will conjecture a relationship between a dependent variable and an independent variable. 
To test hypotheses you will run an experiment which collects a set of \
results of (indepdent_variable, dependent_variable) data points.
Each experiment will consist of 50 simulations run per independent_variable value. \
Each simulation will be fixed to a 100x100 board for 1000 time steps.
Once the experimental results are collected, a hypothesis test function HypothesisTest(results) -> will \
evaluate whether or not the hypothesis was correct given the experimental results.
Formal definitions of these objects are given in python code below:

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple, Union


@dataclass
class Hypothesis:
    text: str


@dataclass
class IndependentVariable:
    value: Union[bool, int, float]
    description: str


@dataclass
class DependentVariable:
    value: Union[bool, int, float]
    description: str


@dataclass
class Results:
    results: List[Tuple[IndependentVariable, DependentVariable]]


class Experiment:
    def __init__(self, hypothesis: Hypothesis):
        self.hypothesis = hypothesis

    @abstractmethod
    def __call__(self) -> Results:
        \"""
        Run experiment for self.hypothesis.
        \"""
        pass


class HypothesisTest:
    def __init__(self, hypothesis: Hypothesis):
        self.hypothesis = hypothesis

    @abstractmethod
    def __call__(self, results: Results) -> bool:
        pass
        

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

    def __eq__(self, other):
        return (self.state == other.state).all()


@dataclass
class GOLGame:
    trajectory: List[GOLState]  # 

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
```

Now propose a hypothesis to test. First write in natural language and then \
define the Hypothesis, Experiment, and HypothesisTest in python. 
Note: You are given access to a simulation function `batched_run_gol` which takes in a \
list of initial_states: List[GOLState] and outputs a list of GOLGames.
""",

    "structure_generation": """\
We are going to be playing the game of life. \
You are a game of life scientist: your goal is to construct as many diverse structure as possible. \
Think of a known structure and generate it in RLE format.
""",

    "structure_property": """\
We are going to be playing the game of life. \
Each game is defined via the python objects:
```python
@dataclass
class GOLState:
    state: np.array  # 2-D numpy array

@dataclass
class GOLGame:
    trajectory: List[GOLState]
```
You are a game of life scientist: your goal is to construct as many diverse structure as possible. \
You will start by constructing a glider using the following GOLObject:
```python
@dataclass
class GOLObject:
    \"""
    Implements a GOL object specified in rle and anchored in space by (x, y)
    \"""
    x: int  # x coordinate of upper left corner
    y: int  # y coordinat of upper left corner
    rle: str
```
You will also define a list of expected Measurements that the glider should satisfy:
```python
@dataclass
class Measurement:
    \"""
    Defines a qualitative/quantitative measurement of a GOLGame in the Game of Life.
    \"""
    name: str
    description: str

    @abstractmethod
    def __call__(self, structure: GOLGame) -> Any:
        pass

```
These will be combined in the GOLStructure object:
```python
@dataclass
class GOLStructure(GOLObject):
    \"""
    A GOLObject that satisfies expected_measurements when used to initialize a GOLGame
    \"""
    name: str
    description: str
    object: GOLObject
    expected_measurements: List[Tuple[Measurement, Any]]  # list of (measurement, expected value) pairs
```
Note: You do not have to re-implement any of these classes. 
You also do not have to implement game of life. This will be provided for you.
"""
}