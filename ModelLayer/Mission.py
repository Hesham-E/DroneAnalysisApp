from aenum import Enum

class MissonType(Enum):
    _init_ = 'value string'

    SURVEILLANCE = 1, "Surveillance"
    PAYLOAD_DELIVERY = 2, "Payload Delivery"
    PAYLOAD_DELIVERY_RETURN = 3, "Payload Delivery with Return"
    ALL = 4, "ALL"

    def __str__(self):
        return self.string

class MissionProfile(Enum):
    _init_ = 'value string'

    VTOL_STRAIGHT = 1, "Mission Profile #1"
    
    def __str__(self):
        return self.string

class MissionPerformance(Enum):
    _init_ = 'value string'

    PERFORMANCE = 1, "Performance"
    EFFICIENT = 2, "Efficient"
    
    def __str__(self):
        return self.string

class Mission:
    def __init__(self, missionType, parameters, profile, performance):
        self.missionType = missionType
        self.parameters = parameters
        self.profile = profile
        self.performance = performance