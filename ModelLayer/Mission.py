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
    BASIC_FIXED_WING = 2, "Mission Profile #2"
    SWEEP = 3, "Mission Profile #3"
    DOUBLE_CRUISE = 4, "Mission Profile #4"
    
    def __str__(self):
        return self.string

class MissionPerformance(Enum):
    _init_ = 'value string'

    PERFORMANCE = 1, "Performance"
    EFFICIENT = 2, "Efficient"
    
    def __str__(self):
        return self.string

class MissionLeg(Enum):
    _init_ = "value string realName"

    VTOL_TAKEOFF = 1, "calcTakeOff", "VTOL Take Off"
    TRANSITION = 2, "calcAccelerationTransitionPeriod", "Transition"
    ACCELERATION = 3, "calcAccelerationPeriod", "Fixed-Wing Acceleration"
    CRUISE = 4, "calcCruisePeriod", "Cruise"
    VTOL_LANDING = 5, "calcLanding", "VTOL Landing"
    ASCENT = 6, "calcFixedWingClimb", "Fixed-Wing Climb"
    DESCENT = 7, "calcFixedWingDescent", "Fixed-Wing Descent"
    

class Mission:
    def __init__(self, missionType, parameters, profile, performance):
        self.missionType = missionType
        self.parameters = parameters
        self.profile = profile
        self.performance = performance
        self.legs = []

        if profile == MissionProfile.VTOL_STRAIGHT:
            self.legs = [MissionLeg.VTOL_TAKEOFF,
                         MissionLeg.TRANSITION,
                         MissionLeg.ACCELERATION,
                         MissionLeg.CRUISE,
                         MissionLeg.VTOL_LANDING]
            
        elif profile == MissionProfile.BASIC_FIXED_WING:
            self.legs = [MissionLeg.VTOL_TAKEOFF,
                         MissionLeg.TRANSITION,
                         MissionLeg.ACCELERATION,
                         MissionLeg.ASCENT,
                         MissionLeg.CRUISE,
                         MissionLeg.DESCENT,
                         MissionLeg.VTOL_LANDING]
        
        elif profile == MissionProfile.SWEEP:
            self.legs = [MissionLeg.VTOL_TAKEOFF,
                         MissionLeg.TRANSITION,
                         MissionLeg.ACCELERATION,
                         MissionLeg.ASCENT,
                         MissionLeg.CRUISE,
                         MissionLeg.DESCENT,
                         MissionLeg.ACCELERATION,
                         MissionLeg.ASCENT,
                         MissionLeg.CRUISE,
                         MissionLeg.DESCENT,
                         MissionLeg.VTOL_LANDING]
        
        elif profile == MissionProfile.DOUBLE_CRUISE:
            self.legs = [MissionLeg.VTOL_TAKEOFF,
                         MissionLeg.TRANSITION,
                         MissionLeg.ACCELERATION,
                         MissionLeg.CRUISE,
                         MissionLeg.ASCENT,
                         MissionLeg.CRUISE,
                         MissionLeg.DESCENT,
                         MissionLeg.VTOL_LANDING]
        