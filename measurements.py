from typing import List, Tuple
import numpy as np
from dataclasses import dataclass

from gol import Measurement, GOLGame


@dataclass
class BoundingBox(Measurement):
    name = "bounding_box"
    description = "Bounding box of all live cells."
    time_range: int  # max time from initial condition to compute bbox

    def frame_bbox(self, frame: np.array) -> np.array:
        """
        + frame: frame to compute bbox of
        return: np.array of size (2, 2) where res[0] is the upper left point
        """
        ys, xs = frame.nonzero()
        return np.array(((np.min(xs), ys[0]), (np.max(xs), ys[-1]))) if len(xs) > 0 else np.array([[0, 0], [0, 0]])

    def __call__(self, game: GOLGame) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        return [self.frame_bbox(frame.state) for i, frame in enumerate(game) if i < self.time_range]


@dataclass
class PerStepVelocity(Measurement):
    name = "per_step_velocity"
    description = "Computes list of per time-step velocity of structure by computing the distance \
between initial bbox and next bbox."
    time_range: int  # max time from initial condition to track velocity

    def bbox_dist(self, box1, box2):
        return np.max(np.linalg.norm(box1 - box2, ord=2, axis=1))

    def __call__(self, game: GOLGame) -> List[float]:
        bbox_m = BoundingBox(time_range=self.time_range)
        bboxes = bbox_m(game)
        return [self.bbox_dist(box1, box2) for box1, box2 in zip(bboxes[:-1], bboxes[1:])]


@dataclass
class LongTimeVelocity(Measurement):
    name = "long_time_velocity"
    description = "Computes velocity of structure by computing the distance \
between initial bbox and bbox at 'time_range' future step and dividing by 'time_range'"
    time_range: int  # max time from initial condition to track velocity

    def bbox_dist(self, box1, box2):
        return np.max(np.linalg.norm(box1 - box2, ord=2, axis=1))

    def __call__(self, game: GOLGame) -> List[float]:
        bbox_m = BoundingBox(time_range=self.time_range)
        bboxes = bbox_m(game)
        return self.bbox_dist(bboxes[0], bboxes[-1])# / self.time_range