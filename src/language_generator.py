from __future__ import annotations
import numpy as np
from numpy.typing import NDArray
from typing import List, Tuple
import random


class TranslationalLanguageGenerator:
    def __init__(self, direction_pairs: List[Tuple[str, str]], misaligned_phrases: List[str],
                 aligned_phrases: List[str], urgency_thresholds: Tuple[float, float]) -> None:
        self.aligned_threshold = min(urgency_thresholds)
        self.misaligned_threshold = max(urgency_thresholds)
        self.direction_pairs = direction_pairs
        self.misaligned_phrases = misaligned_phrases
        self.aligned_phrases = aligned_phrases

    def _get_movement_directions(self, translation: NDArray) -> List[str]:
        directions = []

        for i in range(len(translation)):
            direction_pair = self.direction_pairs[i]
            direction = direction_pair[0 if translation[i] > 0.0 else 1]
            directions.append(direction)

        return directions

    def _stringify_list(self, items: List[str]) -> str:
        string = ""

        for i in range(len(items)):
            if i > 0:
                # all my homies hate the oxford comma
                string += ", " if i != len(items) - 1 else "and "

            string += items[i]

        return string

    def _get_composite_misaligned_direction(self, urgencies: NDArray, directions: List[str]) -> str:
        composite_directions = [direction for urgency, direction in zip(
            urgencies, directions) if urgency > 0.5 * self.misaligned_threshold]
        return self._stringify_list(composite_directions)

    def _get_composite_aligned_direction(self, urgencies: NDArray, directions: List[str]) -> str:
        composite_directions = [direction for urgency, direction in zip(
            urgencies, directions) if urgency < 0.5 * self.aligned_threshold]
        return self._stringify_list(composite_directions)

    def _generate_misaligned_utterance(self, urgencies: NDArray, translation: NDArray) -> str:
        if len(self.misaligned_phrases) == 0:
            return ""

        movement_directions = self._get_movement_directions(translation)
        composite_direction = self._get_composite_misaligned_direction(
            urgencies, movement_directions)

        phrase = random.choice(self.misaligned_phrases)
        phrase = phrase.replace('<direction>', composite_direction)

        return phrase

    def _generate_aligned_utterance(self, urgencies: NDArray, translation: NDArray) -> str:
        if len(self.aligned_phrases) == 0:
            return ""

        movement_directions = self._get_movement_directions(translation)
        composite_direction = self._get_composite_aligned_direction(
            urgencies, movement_directions)

        phrase = random.choice(self.aligned_phrases)
        phrase = phrase.replace('<direction>', composite_direction)

        return phrase

    def generate_utterance(self, urgencies: float | NDArray, translation: float | NDArray) -> Tuple[str, float]:
        if not isinstance(urgencies, np.ndarray):
            urgencies = np.array([urgencies])
        if not isinstance(translation, np.ndarray):
            translation = np.array([translation])

        max_urgency = np.max(urgencies)
        min_urgency = np.min(urgencies)

        if abs(max_urgency) >= abs(min_urgency) and max_urgency > self.misaligned_threshold:
            return self._generate_misaligned_utterance(urgencies, translation), max_urgency
        elif min_urgency < self.aligned_threshold:
            return self._generate_aligned_utterance(urgencies, translation), min_urgency
        else:
            return "", 0.0
