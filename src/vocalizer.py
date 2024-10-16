import os

class Vocalizer:
    def __init__(self) -> None:
        pass

    def utter(self, phrase: str, interupt: bool = False) -> None:
        if interupt:
            os.system(f'killall say; say "{phrase}" &')
        else:
            os.system(f'pgrep say || say "{phrase}" &')
