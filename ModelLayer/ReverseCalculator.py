import math

from .AtmosphereConditions import AtmosphereConditions

class ReverseCalculator:
    G_ACCEL = 9.80665 # m/s^2

    def __init__(self, mission):
        self.atmConditions = AtmosphereConditions()
        self.mission = mission
        self.reynoldsNum = 100000 # Reynolds number for model aircrafts
    
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
    
    def calcOswaldEfficicency(self, aspectRatio):
        print("Oswald Efficicency ", 1.78 * (1 - 0.045 * (aspectRatio ** 0.68)) - 0.64)
        return 1.78 * (1 - 0.045 * (aspectRatio ** 0.68)) - 0.64
    
    def calcDragDueToLiftFactor(self, aspectRatio):
        print("Drag due to lift factor ", 1 / (math.pi * aspectRatio * self.calcOswaldEfficicency(aspectRatio)))
        return 1 / (math.pi * aspectRatio * self.calcOswaldEfficicency(aspectRatio))
    
    def calcFuselageDimensions(self, mass, wingArea, aspectRatio, speed, numberOfVTOLProps, vtolPropellorDiameter, vtolMotorHeight, vtolMotorDiameter):
        airDensity = self.atmConditions.calcAirDensityAtAltitude(self.mission.parameters["cruiseAltitude"], self.mission.parameters["temperature"])
        weight = mass * self.G_ACCEL
        wingLoading = weight / wingArea
        dragDueToLiftFactor = self.calcDragDueToLiftFactor(aspectRatio)
        skinFrictionCoeff = self.calcSkinFrictionCoefficient()
        CDMR = self.calcMotorDragCoefficient(wingArea, numberOfVTOLProps, vtolPropellorDiameter, vtolMotorHeight, vtolMotorDiameter)
        qInf = 0.5 * math.pi * airDensity * ( speed ** 2 ) 

        print("Wing Loading ", wingLoading)
        print("Wing Area ", wingArea)
        print("dragDuetoLiftFactor ", dragDueToLiftFactor)
        print("wingArea ", wingArea)
        print("skinFrictionCoeff", skinFrictionCoeff)
        print("K ", dragDueToLiftFactor)
        print("mass ", mass)
        print("airDensity ", airDensity)
        print("CDMR ", CDMR)

        wettedArea = ( ( wingLoading ** 2 ) * 3 * dragDueToLiftFactor - CDMR ) * wingArea
        wettedArea = wettedArea / ( skinFrictionCoeff * ( qInf ** 2 ) )

        print("wettedArea ", wettedArea)

        fuselageArea =  ( wettedArea - wingArea ) / 1.21

        fuselageLength = fuselageArea * 3.43
        fuselageRadius = fuselageArea * 0.312

        return(fuselageLength, fuselageRadius)
    
    def calcSkinFrictionCoefficient(self):
        skinFrictionCoefficient = 0.42 / ( math.log(0.056 * self.reynoldsNum ) ** 2 )
        return skinFrictionCoefficient * 1.5 # According to Anderson this 1.5 is needed if it is not a flat plane

    def calcMotorDragCoefficient(self, wingArea, numberOfVTOLProps, vtolPropellorDiameter, vtolMotorHeight, vtolMotorDiameter):
        C07R = 0.038

        firstTerm = 0.1 * numberOfVTOLProps * vtolPropellorDiameter * C07R / wingArea
        secondTerm = 1.2 * vtolMotorHeight * vtolMotorDiameter * numberOfVTOLProps / wingArea

        print("CDMR ", firstTerm + secondTerm)
        return firstTerm + secondTerm
    
    def calcZeroLiftDragCoefficient(self, wingArea):
        skinFrictionCoefficient = 0.42 / ( math.log(0.056 * self.reynoldsNum ) ** 2 )
        skinFrictionCoefficient = skinFrictionCoefficient * 1.5 # According to Anderson this 1.5 is needed if it is not a flat plane

        print("skinFrictionCoefficient ", skinFrictionCoefficient)
        print("Wetted Area ", self.calcWettedArea())
        print("Reference Area ", self.calcReferenceArea())

        wettedAndReferenceAreaRatio = self.calcWettedArea() / wingArea
        CDMR = self.calcMotorDragCoefficient()

        print("CD0 ", wettedAndReferenceAreaRatio * skinFrictionCoefficient + CDMR)
        return wettedAndReferenceAreaRatio * skinFrictionCoefficient + CDMR
    
    def calcMaxSpeedDrag(self, maxSpeed, stallSpeed, mass, aspectRatio):
        airDensity = self.atmConditions.calcAirDensityAtAltitude(self.mission.parameters["cruiseAltitude"], self.mission.parameters["temperature"])
        wingArea = self.calcWingArea(stallSpeed, mass)
        CD0 = self.calcZeroLiftDragCoefficient(wingArea)
        K = self.calcDragDueToLiftFactor(aspectRatio)
        wingLoading = ( mass * self.G_ACCEL ) / wingArea

        firstTerm = 0.5 * airDensity * ( maxSpeed ** 2 ) * wingArea * CD0
        secondTerm = 2 * K * wingArea / ( airDensity * ( maxSpeed ** 2 ) ) * ( wingLoading ** 2 )

        return firstTerm + secondTerm
