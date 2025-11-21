import random

class Dice:
    def __init__(self):
        self._face_value = random.randint(1, 6)
    
    @property
    def face_value(self):
        return self._face_value
    
    @face_value.setter
    def face_value(self, value):
        if 1 <= value <= 6:
            self._face_value = value
        else:
            raise ValueError("Face value must be between 1 and 6")
    
    def roll(self):
        self._face_value = random.randint(1, 6)
        return self._face_value