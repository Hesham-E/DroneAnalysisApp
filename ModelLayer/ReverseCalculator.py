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
    
    # def calcTailWettedArea(self):
    #     lambdaC = 0.5
    #     cR = 2 * self.wingArea / ( ( lambdaC + 1 ) * self.wingSpan )
    #     cBar = 2 / 3 * cR * ( ( 1 + lambdaC + lambdaC ** 2 ) / ( 1 + lambdaC ) )

    #     Lht = self.fuselageLength / 1.511
    #     Lvt = self.fuselageLength / 1.619

    #     VHT = 0.7
    #     VVT = 0.04

    #     horizontalWettedArea = cBar * self.wingArea * VHT / Lht
    #     verticalWettedArea = self.wingSpan * self.wingArea * VVT / Lvt

    #     return horizontalWettedArea + verticalWettedArea
    
    # def calcFuselageWettedArea(self):
    #     # Fuselage is split into three sections according to page 450, figure 8.28 of Anderson book

    #     secA1 = 2 * 0.6845 * math.pi * self.fuselageRadius ** 2
    #     secA2 = 2 * math.pi * math.sqrt( ( self.fuselageRadius ** 2 + ( 2 * self.fuselageRadius * 0.6845 ) ** 2 ) / 2 )
    #     secA3 = self.fuselageLength * 0.2495

    #     secA = secA1 + secA2 * secA3

    #     secB1 = ( 2 * self.fuselageRadius ) ** 2 * math.pi / 4
    #     secB2 = 2 * math.pi * 0.6845 * self.fuselageRadius ** 2
    #     secB3 = 2 * math.pi * self.fuselageRadius * self.fuselageLength * 0.4177

    #     secB = secB1 - secB2 + secB3

    #     secC = math.pi * self.fuselageRadius ** 3 + self.fuselageLength * 0.33

    #     return secA + secB + secC
    
    # def calcWettedArea(self):
    #     print("Wetted Area: ", self.calcFuselageWettedArea() + self.calcTailWettedArea() + self.wingArea)
    #     print("FuseLage Wetteed Area: ", self.calcFuselageWettedArea())
    #     print("Tail Wetted Area: ", self.calcTailWettedArea())
    #     return self.calcFuselageWettedArea() + self.calcTailWettedArea() + self.wingArea