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
        """
        Run experiment for self.hypothesis.
        """
        pass


class HypothesisTest:
    def __init__(self, hypothesis: Hypothesis):
        self.hypothesis = hypothesis

    @abstractmethod
    def __call__(self, results: Results) -> bool:
        pass