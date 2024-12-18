from __future__ import annotations
import os
import pickle
from typing import Tuple
from numpy.typing import NDArray
import numpy as np

class PhraseTrialData:
    @classmethod
    def load(cls, file_path: str, transformation: NDArray | None = None):
        with open(file_path, 'rb') as file:
            data = pickle.load(file)
            phrase_trial_data = cls(None, None, None, None, None, None,)
            phrase_trial_data.__dict__ = data.__dict__

            if transformation is not None:
                phrase_trial_data.time = np.array(phrase_trial_data.time)
                phrase_trial_data.dt = np.array(phrase_trial_data.dt)
                phrase_trial_data.position = np.array(phrase_trial_data.position) @ transformation.T
                phrase_trial_data.velocity = np.array(phrase_trial_data.velocity) @ transformation.T
                phrase_trial_data.external_force = np.array(phrase_trial_data.external_force) @ transformation.T

            return phrase_trial_data

    def __init__(self, user_id: int, trial_number: int, phrase: str, adverb: str, first_cartesian_direction: str, second_cartesian_direction: str):
        self.user_id = user_id
        self.trial_number = trial_number
        self.phrase = phrase
        self.adverb = adverb
        self.first_cartesian_direction = first_cartesian_direction
        self.second_cartesian_direction = second_cartesian_direction
        self.time = []
        self.dt = [] # this should be shifted back by 1 because dt is measured from t-1 to t but that would implied the dt recorded at t is really the dt starting at t-1
        self.position = []
        self.velocity = []
        self.external_force = []
        self.internal_force = []

    def append(self, time: float, dt: float, position: NDArray, velocity: NDArray, external_force: NDArray, internal_force: NDArray) -> None:
        self.time.append(time)
        self.dt.append(dt)
        self.position.append(position)
        self.velocity.append(velocity)
        self.external_force.append(external_force)
        self.internal_force.append(internal_force)

    def save(self, index: int, dir: str) -> None:
        os.makedirs(dir, exist_ok=True)

        safe_phrase = self.phrase.replace(" ", "_")

        file_name = f"{self.user_id}__{index}__{safe_phrase}.pkl"

        file_path = os.path.join(dir, file_name)

        with open(file_path, 'wb') as file:
            pickle.dump(self, file)
