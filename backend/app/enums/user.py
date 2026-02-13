from enum import Enum

class ActivityLevel(str, Enum):
    SEDENTARY = "sedentary"
    LIGHTLY_ACTIVE = "lightly_active"
    MODERATELY_ACTIVE = "moderately_active"
    VERY_ACTIVE = "very_active"
    EXTREMELY_ACTIVE = "extremely_active"

    @property
    def multiplier(self) -> float:
        mapping = {
            "sedentary": 1.2,
            "lightly_active": 1.375,
            "moderately_active": 1.55,
            "very_active": 1.725,
            "extremely_active": 1.9
        }
        return mapping[self.value]

class GoalStrategy(str, Enum):
    AGGRESSIVE_CUT = "aggressive_cut"
    MODERATE_CUT = "moderate_cut"
    MAINTENANCE = "maintenance"
    MUSCLE_GAIN = "muscle_gain"

    @property
    def protein_factor(self) -> float:
        mapping = {
            "aggressive_cut": 1.8,
            "moderate_cut": 1.6,
            "maintenance": 1.4,
            "muscle_gain": 2.0
        }
        return mapping[self.value]

    @property
    def calorie_offset(self) -> int:
        mapping = {
            "aggressive_cut": -1000,
            "moderate_cut": -500,
            "maintenance": 0,
            "muscle_gain": 300
        }
        return mapping[self.value]