import os
import pickle

class PhraseTrialData:
    def __init__(self, phrase, user_id):
        self.phrase = phrase
        self.user_id = user_id
        self.time = []
        self.position = []
        self.velocity = []
        self.force = []

    def append(self, time, position, velocity, force):
        self.time.append(time)
        self.position.append(position)
        self.velocity.append(velocity)
        self.force.append(force)

    def save(self):
        os.makedirs('phrase_trail_data', exist_ok=True)

        safe_phrase = self.phrase.replace(" ", "_")

        file_name = f"{safe_phrase}_{self.user_id}.pkl"

        file_path = os.path.join('phrase_trail_data', file_name)

        with open(file_path, 'wb') as file:
            pickle.dump(self, file)