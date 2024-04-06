import math

from .AtmosphereConditions import AtmosphereConditions

class ReverseCalculator:
    G_ACCEL = 9.80665 # m/s^2

    def __init__(self, mission):
        self.atmConditions = AtmosphereConditions()
        self.mission = mission 
    
    def calcWingArea(self, stallSpeed, mass):
        airDensity = self.atmConditions.calcAirDensityAtAltitude(self.mission.parameters["cruiseAltitude"], self.mission.parameters["temperature"])
        maxLiftCoefficient = 0.9 * 1.7 #TODO: Change this

        print("airDensity ", airDensity)
        print("maxLiftCoefficient ", maxLiftCoefficient)
        print("mass ", mass)
        print("stallSpeed ", stallSpeed)

        print("Wing Area ", mass / ( ( stallSpeed ** 2 ) * airDensity * maxLiftCoefficient * 0.5 ))
        return mass * self.G_ACCEL / ( ( stallSpeed ** 2 ) * airDensity * maxLiftCoefficient * 0.5 )
    
    def calcWingSpan(self, aspectRatio, stallSpeed, mass):
        wingArea = self.calcWingArea(stallSpeed, mass)

        print("Wing Span ", math.sqrt( wingArea * aspectRatio ) )
        return math.sqrt( wingArea * aspectRatio )
    
    def calcOswaldEfficicency(self):
        aspectRatio = self.calcAspectRatio()

        print("Oswald Efficicency ", 1.78 * (1 - 0.045 * (aspectRatio ** 0.68)) - 0.64)
        return 1.78 * (1 - 0.045 * (aspectRatio ** 0.68)) - 0.64