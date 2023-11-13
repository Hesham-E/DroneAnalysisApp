class Drone:
    def __init__(self, 
                 wingSpan, wingArea, wingThickness,
                 vStabilizerLen, vStabilizerWidth,
                 fuselageRadius, 
                 weight, loadWeight, 
                 angleOfAttack, 
                 batteryWeight, batteryCapacity,
                 motorTablePath):
        
        self.wingSpan = wingSpan
        self.wingArea = wingArea
        self.wingThickness = wingThickness
        
        self.vStabilizerLen = vStabilizerLen
        self.vStabilizerWidth = vStabilizerWidth

        self.fuselageRadius = fuselageRadius

        self.weight = weight
        self.loadWeight = loadWeight 

        self.angleOfAttack = angleOfAttack

        self.batteryWeight = batteryWeight
        self.batteryCapacity = batteryCapacity

        self.motorTablePath = motorTablePath

        self.ellipticalDistribution = 1.1

    def calcMinAirSpeed():
        # some formula using parameters
        return 0
