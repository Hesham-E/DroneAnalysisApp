class Drone:
    def __init__(self, 
                 wingSpan, wingArea, 
                 weight, loadWeight, 
                 angleOfAttack, 
                 batteryWeight, batteryCapacity):
        
        self.wingSpan = wingSpan
        self.wingArea = wingArea

        self.weight = weight
        self.loadWeight = loadWeight 

        self.angleOfAttack = angleOfAttack

        self.batteryWeight = batteryWeight
        self.batteryCapacity = batteryCapacity

        self.ellipticalDistribution = 1.1

    def calcMinAirSpeed():
        # some formula using parameters
        return 0
