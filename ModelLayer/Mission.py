from enum import Enum

class MissonType(Enum):
    SURVEILLANCE = 1
    PAYLOAD_DELIVERY = 2
    PAYLOAD_DELIVERY_RETURN = 3
    ALL = 4

class MissionProfile(Enum):
    VTOL_STRAIGHT = 1

class MissionPerformance(Enum):
    PERFORMANCE = 1
    EFFICIENT = 2
    MINIMAL = 3

class Mission:
    def __init__(self, missionType, parameters, profile, performance):
        self.missionType = missionType
        self.parameters = parameters
        self.profile = profile
        self.performance = performance