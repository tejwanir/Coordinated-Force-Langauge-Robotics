import os
import pickle


class PhraseTrialData:
    @classmethod
    def load(cls, file_path: str):
        with open(file_path, 'rb') as file:
            data = pickle.load(file)
            phrase_trial_data = cls(data.phrase, data.user_id)
            phrase_trial_data.__dict__ = data.__dict__
            return phrase_trial_data

    def __init__(self, phrase, user_id):
        self.phrase = phrase
        self.user_id = user_id
        self.time = []
        self.dt = []
        self.position = []
        self.velocity = []
        self.force = []

    def append(self, time, dt, position, velocity, force):
        self.time.append(time)
        self.dt.append(dt)
        self.position.append(position)
        self.velocity.append(velocity)
        self.force.append(force)

    def get_direction(self) -> str:
        directions = ['left', 'right', 'up', 'down', 'forward', 'backward']

        for direction in directions:
            if direction in self.phrase:
                return direction

        return ''

    def save(self, index):
        os.makedirs('phrase_trial_data', exist_ok=True)

        safe_phrase = self.phrase.replace(" ", "_")

        file_name = f"{self.user_id}__{index}__{safe_phrase}.pkl"

        file_path = os.path.join('phrase_trial_data', file_name)

        with open(file_path, 'wb') as file:
            pickle.dump(self, file)
