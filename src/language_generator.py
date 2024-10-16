import numpy as np
from numpy.typing import NDArray
from typing import List, Tuple
import random


class UrgencyLanguageGenerator:
    def __init__(self, urgency_thresholds: Tuple[float]) -> None:
        self.aligned_threshold = min(urgency_thresholds)
        self.misaligned_threshold = max(urgency_thresholds)
    
    def _stringify_list(self, items: List[str]) -> str:
        string = ""

        for i in range(len(items)):
            if i > 0:
                # all my homies hate the oxford comma
                string += ", " if i != len(items) - 1 else "and "
            
            string += items[i]
        
        return string


class TranslationalLanguageGenerator(UrgencyLanguageGenerator):
    def __init__(self, direction_pairs: List[Tuple[str, str]], urgency_thresholds: Tuple[float, float] = (-0.5, 0.5)) -> None:
        super().__init__(urgency_thresholds)
        self.direction_pairs = direction_pairs

    def _get_movement_directions(self, delta_x: NDArray) -> List[str]:
        directions = []

        for i in range(len(delta_x)):
            direction_pair = self.direction_pairs[i]
            direction = direction_pair[0 if delta_x[i] > 0.0 else 1]
            directions.append(direction)

        return directions

    def _get_composite_misaligned_direction(self, urgencies: NDArray, directions: List[str]) -> str:
        composite_directions = [direction for urgency, direction in zip(urgencies, directions) if urgency > 0.5 * self.misaligned_threshold]

        return self._stringify_list(composite_directions)

    def _get_composite_aligned_direction(self, urgencies: NDArray, directions: List[str]) -> str:
        composite_directions = [direction for urgency, direction in zip(urgencies, directions) if urgency < 0.5 * self.aligned_threshold]
        return self._stringify_list(composite_directions)
    
    def _generate_misaligned_utterance(self, urgencies: NDArray, delta_x: NDArray) -> str:
        movement_directions = self._get_movement_directions(delta_x)
        composite_direction = self._get_composite_misaligned_direction(urgencies, movement_directions)

        phrases_mean = [
            f"move {composite_direction} bitch",
            f"move the hell {composite_direction}",
            f"get your ass {composite_direction}",
            f"stop fucking around and move {composite_direction}",
            f"you better move {composite_direction} before i beat your ass",
            f"i'm done with you",
            f"dumb ass won't move {composite_direction}",
            f"were you born this dumb? move {composite_direction}",
            f"are you crippled? move {composite_direction}",
            f"i hate you, just move {composite_direction}",
            f"if i could kill myself i would",
        ]
    
        phrases_nice = [
            f"move {composite_direction} please",
            f"please move your hand {composite_direction}",
            f"the goal is {composite_direction} from here",
        ]

        return random.choice(phrases_nice)

    def _generate_aligned_utterance(self, urgencies: NDArray, delta_x: NDArray) -> str:
        movement_directions = self._get_movement_directions(delta_x)
        composite_direction = self._get_composite_aligned_direction(urgencies, movement_directions)

        phrases = [
            f"keep moving {composite_direction}",
        ]

        return random.choice(phrases)

    def generate_utterance(self, urgencies: float | NDArray, delta_x: float | NDArray) -> Tuple[str, float]:
        if type(urgencies) is float:
            urgencies = np.array(urgencies)
        if type(delta_x) is float:
            delta_x = np.array(delta_x)

        max_urgency = np.max(urgencies)
        min_urgency = np.min(urgencies)

        if abs(max_urgency) > abs(min_urgency) and max_urgency > self.misaligned_threshold:
            return self._generate_misaligned_utterance(urgencies, delta_x), max_urgency
        elif min_urgency < self.aligned_threshold:
            return self._generate_aligned_utterance(urgencies, delta_x), min_urgency
        else:
            return "", 0.0
