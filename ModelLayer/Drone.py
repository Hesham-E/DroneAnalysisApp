from .AtmosphereConditions import AtmosphereConditions
from .DragLiftCoefficientInterface import DragLiftCoefficientInterface
from .MotorTableInterface import MotorTableInterface
from .Mission import *
import math


G_ACCEL = 9.80665
UNDER_HOVER_FORCE = 0.5

class Drone:
    def __init__(self, 
                 wingSpan, wingArea,
                 airFoil,
                 fuselageRadius, fuselageLength,
                 weight,
                 angleOfAttack,
                 reynoldsNum,
                 batteryWeight, batteryCapacity, batteryVoltage,
                 cruiseMotorTablePath, vtolMotorTablePath,
                 auxPowerCon,
                 ascentDecentSpeed,
                 mission):
        
        self.wingSpan = wingSpan
        self.wingArea = wingArea
        self.airFoil = int(airFoil)
        self.reynoldsNum = reynoldsNum

        self.fuselageRadius = fuselageRadius
        self.fuselageLength = fuselageLength

        # IMPORTANT NOTE:
        # Anderson's book uses a variable W for weight.
        # This appears to be weight in it's most literal sense.
        # As in order to convert the equations found in this book,
        # we must multiply any W by acceleration of gravity.
        # We surmise this may be to the imperial unit of "slug"
        self.weight = weight
        self.loadWeight = mission.parameters["loadWeight"]
        self.totalMass = weight + batteryWeight + mission.parameters["loadWeight"]
        self.totalWeight = self.totalMass * G_ACCEL # W is used

        self.angleOfAttack = angleOfAttack

        self.batteryWeight = batteryWeight
        self.batteryCapacity = batteryCapacity
        self.batteryVoltage = batteryVoltage
        self.batteryEnergy = batteryVoltage * batteryCapacity * 3.6 * 0.94

        self.cruiseAltitude = mission.parameters["cruiseHeight"] # TODO: Replace this as per a mission profile, for the none simple ones
        self.targetAltitude = mission.parameters["cruiseHeight"]
        self.ascentDecentSpeed = ascentDecentSpeed

        self.targetDistance = mission.parameters["missionDistance"]

        self.auxPowerCon = auxPowerCon

        self.pressure = mission.parameters["pressure"]
        self.temperature = mission.parameters["temperature"]

        self.mission = mission

        self.ellipticalDistribution = 1.1
        self.liftDistribution = 0.95

        self.atmConditions = AtmosphereConditions()
        self.dragLiftInterface = DragLiftCoefficientInterface(f"./ModelLayer/data/airfoils/xf-naca{self.airFoil}-il-{self.adjustReynoldsNumberToValue(reynoldsNum)}_Subset_1.csv")
        self.cruiseMotorTableInterface = MotorTableInterface(cruiseMotorTablePath)
        self.vtolMotorTableInterface = MotorTableInterface(vtolMotorTablePath)

        # For future reverse engineering purposes
        if self.pressure == None:
            self.pressure = self.atmConditions.calcPressure(self.cruiseAltitude, self.temperature)
        elif self.temperature == None:
            self.temperature = self.atmConditions.calcAltitude(self.pressure, self.temperature)
    
    def adjustReynoldsNumberToValue(self, num):
        availableData = [50000, 100000, 200000, 500000, 1000000]
        print(min(availableData, key=lambda x:abs(x - num)))
        return min(availableData, key=lambda x:abs(x - num))
    
    def calcStallSpeed(self):
        airDensity = self.atmConditions.calcAirDensity(self.pressure, self.temperature)
        maxLiftCoefficient = 2.34 #TODO: Change this
        wingloading = self.totalWeight / self.wingArea 

        vStallSquared = 2 * wingloading / ( airDensity * maxLiftCoefficient )
        return math.sqrt(vStallSquared)
    
    def calcMaxSpeed(self):
        thrust = self.cruiseMotorTableInterface.getMaxThrust()
        airDensity = self.atmConditions.calcAirDensity(self.pressure, self.temperature)
        coefficientK = self.calcDragDueToLiftFactor()
        thrustAreaRatio = thrust / self.wingArea
        thrustWeightRatio = thrust / self.totalWeight
        wingLoading = self.totalWeight / self.wingArea

        vMaxSquared = (thrustAreaRatio + wingLoading * math.sqrt( ( thrustWeightRatio ** 2 ) - 4 * self.calcZeroLiftDragCoefficient() * coefficientK ) ) / ( airDensity * self.calcZeroLiftDragCoefficient() )
        return math.sqrt(vMaxSquared)
    
    def calcLift(self):
        airDensity = self.atmConditions.calcAirDensity(self.pressure, self.temperature)
        liftCoefficient = self.dragLiftInterface.getLiftCoefficient(self.angleOfAttack, self.wingSpan, self.wingArea, self.liftDistribution)

        return 0.5 * airDensity * ( self.calcCruiseSpeed() ** 2 ) * self.wingArea * liftCoefficient
    
    def calcTailWettedArea(self):
        lambdaC = 0.5
        cR = 2 * self.wingArea / ( ( lambdaC + 1 ) * self.wingSpan )
        cBar = 2 / 3 * cR * ( ( 1 + lambdaC + lambdaC ** 2 ) / ( 1 + lambdaC ) )

        Lht = self.fuselageLength / 1.511
        Lvt = self.fuselageLength / 1.619

        VHT = 0.7
        VVT = 0.04

        horizontalWettedArea = cBar * self.wingArea * VHT / Lht
        verticalWettedArea = self.wingSpan * self.wingArea * VVT / Lvt

        return horizontalWettedArea + verticalWettedArea
    
    def calcFuselageWettedArea(self):
        # Fuselage is split into three sections according to page 450, figure 8.28 of Anderson book

        secA1 = 2 * 0.6845 * math.pi * self.fuselageRadius ** 2
        secA2 = 2 * math.pi * math.sqrt( ( self.fuselageRadius ** 2 + ( 2 * self.fuselageRadius * 0.6845 ) ** 2 ) / 2 )
        secA3 = self.fuselageLength * 0.2495

        secA = secA1 + secA2 * secA3

        secB1 = ( 2 * self.fuselageRadius ) ** 2 * math.pi / 4
        secB2 = 2 * math.pi * 0.6845 * self.fuselageRadius ** 2
        secB3 = 2 * math.pi * self.fuselageRadius * self.fuselageLength * 0.4177

        secB = secB1 - secB2 + secB3

        secC = math.pi * self.fuselageRadius ** 3 + self.fuselageLength * 0.33

        return secA + secB + secC
    
    def calcWettedArea(self):
        return self.calcFuselageWettedArea() + self.calcTailWettedArea() + self.wingArea
    
    def calcReferenceArea(self):
        lambdaC = 0.5
        cR = 2 * self.wingArea / ( ( lambdaC + 1 ) * self.wingSpan )

        return self.wingArea - cR * self.fuselageRadius
    
    def calcZeroLiftDragCoefficient(self):
        skinFrictionCoefficient = 0.0776 * ( ( math.log( 10000000, 10 ) - 1.88 ) ** -2 ) + 60 / 10000000
        skinFrictionCoefficient = skinFrictionCoefficient * 1.5 # According to Anderson this 1.5 is needed if it is not a flat plane

        wettedAndReferenceAreaRatio = self.calcWettedArea() / self.calcReferenceArea()
        return wettedAndReferenceAreaRatio * skinFrictionCoefficient

    def calcLiftInducedDrag(self):
        airDensity = self.atmConditions.calcAirDensity( self.pressure, self.temperature )
        weight = self.weight + self.loadWeight + self.batteryWeight
        weightChordRatio = ( weight /  airDensity ) ** 2
        q = 0.5 * airDensity * math.pi * ( self.calcCruiseSpeed() ) ** 2

        return (self.ellipticalDistribution * weightChordRatio) / (q * math.pi)

    def calcParasiticDrag(self):
        airDensity = self.atmConditions.calcAirDensity( self.pressure, self.temperature )
        q = 0.5 * airDensity * math.pi * ( self.calcCruiseSpeed() ) ** 2
        liftCoefficent = self.dragLiftInterface.getLiftCoefficient( self.angleOfAttack, self.wingSpan, self.wingArea, self.liftDistribution )
        wingParasiticDragCoefficient = self.dragLiftInterface.getParasiticDragCoefficient( self.angleOfAttack )

        skinRoughnessFactor = 6.34 * ( 10 ** -6 )
        reynoldsCutoff = 38.21 * ( ( self.fuselageLength / skinRoughnessFactor ) ** 1.053 )
        reynoldsCutoff = reynoldsCutoff if 200000 > reynoldsCutoff else 200000
        skinFrictionCoefficient = 0.0776 * ( ( math.log( reynoldsCutoff, 10 ) - 1.88 ) ** -2 ) + 60 / reynoldsCutoff
        skinFrictionCoefficient = skinFrictionCoefficient * 1.5 # According to Anderson this 1.5 is needed if it is not a flat plane

        fuselageFormFactor = 1 + (60 / ((self.fuselageLength / (2 * self.fuselageRadius)) ** 3) + (self.fuselageLength / (2 * self.fuselageRadius) / 400))
        #abs() in fuselage area might be a bandaid
        fuselageArea = math.pi * 2 * self.fuselageRadius * self.fuselageLength * (abs(1 - 2 / (self.fuselageLength / (self.fuselageRadius * 2))) ** (2/3)) * (1 + 1 / ((self.fuselageLength / (2 * self.fuselageRadius)) ** 2))
        fuseLageCoefficient = skinFrictionCoefficient * fuselageFormFactor * (fuselageArea / self.wingArea)
        
        return ( (wingParasiticDragCoefficient + fuseLageCoefficient) + self.ellipticalDistribution * (liftCoefficent ** 2) ) / (q * self.wingArea)

    def calcDrag(self):        
        liftCoefficient = self.dragLiftInterface.getLiftCoefficient(self.angleOfAttack, self.wingSpan, self.wingArea, self.liftDistribution)
        liftInducedDragCoefficient = liftCoefficient ** 2 / (math.pi * self.ellipticalDistribution * self.calcAspectRatio())
        
        dragCoefficient = self.dragLiftInterface.getDragCoefficient(self.angleOfAttack)
        dragCoefficient += liftInducedDragCoefficient

        airDensity = self.atmConditions.calcAirDensity(self.pressure, self.temperature)
        q = 0.5 * airDensity * math.pi * ( self.calcCruiseSpeed() ) ** 2
        return dragCoefficient * q * self.wingArea
    
    def calcRateOfClimb(self):
        velocityROCMax =  2 / self.atmConditions.calcAirDensity() * \
                          math.sqrt(self.liftDistribution / 3 * self.calcZeroLiftDragCoefficient()) * \
                          self.totalWeight / self.wingArea
        velocityROCMax = velocityROCMax ** 0.5

        return self.cruiseMotorTableInterface.getMaxThrust() / self.totalMass \
               - velocityROCMax * 1.155 / ( self.calcLift() / self.calcDrag() )
    
    def calcRateOfDescent(self):
        return math.sqrt( 2 / self.atmConditions.calcAirDensity() \
                          * math.sqrt( self.liftDistribution / self.calcZeroLiftDragCoefficient() ) \
                          * ( self.totalWeight / self.wingArea ) )

    def calcTakeOff1(self):
        thrust = self.vtolMotorTableInterface.getMaxThrust() * 4
        takeOffAccel = thrust / (self.weight + self.loadWeight + self.batteryWeight) - G_ACCEL
        time11 = self.ascentDecentSpeed / takeOffAccel
        dist11 = 0.5 * takeOffAccel * (time11 ** 2)
        energy11 = self.vtolMotorTableInterface.getMaxPower() * 4 * time11
        return time11, dist11, energy11
    
    def calcTakeOff3(self):
        hoverForce = (self.weight + self.loadWeight + self.batteryWeight) * G_ACCEL * UNDER_HOVER_FORCE
        accel = hoverForce / (self.weight + self.loadWeight + self.batteryWeight)
        time13 = -1 * self.ascentDecentSpeed / accel
        dist13 = self.ascentDecentSpeed * time13 + 0.5 * accel * (time13 ** 2)
        energy13 = self.vtolMotorTableInterface.getPowerAtThrust(hoverForce / 4) * time13 * 4

        return time13, dist13, energy13
    
    def calcTakeOff(self):
        time11, dist11, energy11 = self.calcTakeOff1()
        time13, dist13, energy13 = self.calcTakeOff3()

        dist12 = self.targetAltitude - dist11 - dist13
        time12 = dist12 / self.ascentDecentSpeed

        hoverForce = (self.weight + self.loadWeight + self.batteryWeight) * G_ACCEL
        energy12 = time12 * self.vtolMotorTableInterface.getPowerAtThrust(hoverForce / 4) * 4

        totalTime = time11 + time12 + time13
        totalDist = dist11 + dist12 + dist13
        totalEnergy = energy11 + energy12 + energy13
        
        return totalTime, totalDist, totalEnergy
    
    def calcPeriod2(self):
        cruiseThrust = self.calcCruiseThrust()
        cruiseAccel = cruiseThrust / (self.weight + self.loadWeight + self.batteryWeight)
        time2 = ( self.calcCruiseSpeed() / cruiseAccel ) * math.atanh( self.calcStallSpeed() / self.calcCruiseSpeed() )
        
        hoverForce = (self.weight + self.loadWeight + self.batteryWeight) * G_ACCEL
        energy2 = time2 * self.vtolMotorTableInterface.getPowerAtThrust(hoverForce / 4) * 4

        return time2, energy2
    
    def calcPeriod23(self):
        cruiseSpeed = self.calcCruiseSpeed()

        cruiseThrust = self.calcCruiseThrust()
        cruiseAccel = cruiseThrust / (self.weight + self.loadWeight + self.batteryWeight)
        time23 = (cruiseSpeed / cruiseAccel) * math.atanh(0.99)
        dist23 = cruiseSpeed * math.log( math.cosh(time23 * cruiseAccel / cruiseSpeed) ) / (cruiseAccel / cruiseSpeed)
        energy23 = time23 * cruiseThrust

        return time23, dist23, energy23
    
    def calcPeriod5(self):
        stallSpeed = self.calcStallSpeed()
        cruiseSpeed = self.calcCruiseSpeed()
        densityAltitude = self.atmConditions.calcIdealDensityAltitude(self.pressure, self.temperature)
        totalWeight = self.weight + self.loadWeight + self.batteryWeight

        time5 = (1 / stallSpeed - 1 / cruiseSpeed) - ( densityAltitude * self.calcDrag() / (2 * totalWeight))
        return time5

    def calcPeriod6(self):
        cruiseSpeed = self.calcCruiseSpeed()
        densityAltitude = self.atmConditions.calcIdealDensityAltitude(self.pressure, self.temperature)
        totalWeight = self.weight + self.loadWeight + self.batteryWeight
        time5 = self.calcPeriod5()

        time6 = (1 / 0.5 - 1 / cruiseSpeed) - ( densityAltitude * self.calcDrag() / (2 * totalWeight)) - time5
        hoverForce = (self.weight + self.loadWeight + self.batteryWeight) * G_ACCEL
        energy6 = time6 * self.vtolMotorTableInterface.getPowerAtThrust( hoverForce / 4 ) * 4

        return time6, energy6
    
    def calcLanding1(self):
        hoverForce = (self.weight + self.loadWeight + self.batteryWeight) * G_ACCEL * UNDER_HOVER_FORCE
        accel = hoverForce / (self.weight + self.loadWeight + self.batteryWeight) - G_ACCEL
        time71 = -1 * self.ascentDecentSpeed / accel
        dist71 = self.ascentDecentSpeed * time71 + 0.5 * accel * (time71 ** 2)
        energy71 = self.vtolMotorTableInterface.getPowerAtThrust(hoverForce / 4) * 4 * time71

        return time71, dist71, energy71

    def calcLanding3(self):
        maxThrust = self.vtolMotorTableInterface.getMaxThrust() * 4
        accel = maxThrust / (self.weight + self.loadWeight + self.batteryWeight) - G_ACCEL
        time73 = self.ascentDecentSpeed / accel
        dist73 = 0.5 * accel * (time73 ** 2)
        energy73 = self.vtolMotorTableInterface.getMaxPower() * 4 * time73

        return time73, dist73, energy73
    
    def calcLanding(self):
        time71, dist71, energy71 = self.calcLanding1()
        time73, dist73, energy73 = self.calcLanding3()

        dist72 = self.targetAltitude - dist71 - dist73
        time72 = dist72 / self.ascentDecentSpeed
        hoverForce = (self.weight + self.loadWeight + self.batteryWeight) * G_ACCEL
        energy72 = time72 * self.vtolMotorTableInterface.getPowerAtThrust(hoverForce / 4) * 4

        totalTime = time71 + time72 + time73
        totalDist = dist71 + dist72 + dist73
        totalEnergy = energy71 + energy72 + energy73

        return totalTime, totalDist, totalEnergy
    
    def calcPeriod4(self):
        time1, dist1, energy1 = self.calcTakeOff()
        time2, energy2 = self.calcPeriod2()
        time23, dist23, energy23 = self.calcPeriod23()
        time5 = self.calcPeriod5()
        time6, energy6 = self.calcPeriod6()
        time7, dist7, energy7 = self.calcLanding()

        cruisePower = self.cruiseMotorTableInterface.getPowerAtThrust(self.calcCruiseThrust())
        time4 = ( self.batteryEnergy - energy1 - energy2 - energy23 - energy6 - energy7 - self.auxPowerCon * (time1 + time23 + time5 + time6 + time7) ) / (cruisePower + self.auxPowerCon)
        dist4 = time4 * self.calcCruiseSpeed()

        return time4, dist4
    
    def calcMaxRange(self):
        time23, dist23, energy23 = self.calcPeriod23()
        time4, dist4 = self.calcPeriod4()

        return dist4 + dist23
    
    def calcCruiseSpeed(self):
        if self.mission.performance == MissionPerformance.PERFORMANCE:
            return self.calcMaxSpeed()
        elif self.mission.performance == MissionPerformance.EFFICIENT:
            return self.calcEfficientSpeed()
    
    def calcCruiseThrust(self):
        if self.mission.performance == MissionPerformance.PERFORMANCE:
            return self.cruiseMotorTableInterface.getMaxThrust()
        elif self.mission.performance == MissionPerformance.EFFICIENT:
            return self.calcEfficientThrust()
    
    def calcEfficientSpeed(self):
        airDensity = self.atmConditions.calcAirDensity(self.pressure, self.temperature)
        thrustWeightRatio = self.calcEfficientThrust() / self.totalWeight # So we get the error checking from cruiseThrust()
        wingLoading = self.totalWeight / self.wingArea

        return math.sqrt(thrustWeightRatio * wingLoading / (airDensity * self.calcZeroLiftDragCoefficient()))

    def calcEfficientThrust(self):
        maxThrust = self.cruiseMotorTableInterface.getMaxThrust()
        coefficientK = self.calcDragDueToLiftFactor()
        thrustWeightRatio = math.sqrt(4 * self.calcZeroLiftDragCoefficient() * coefficientK)
        thrust = thrustWeightRatio * self.totalWeight
        
        if thrust > maxThrust:
            pass # TODO: Throw an error because the motor/prop combo cannot generate thrust for steady flight

        return thrust
        
    def calcOswaldEfficicency(self):
        aspectRatio = self.calcAspectRatio()
        return 1.78 * (1 - 0.045 * (aspectRatio ** 0.68)) - 0.64
    
    def calcDragDueToLiftFactor(self):
        aspectRatio = self.calcAspectRatio()
        return 1 / (math.pi * aspectRatio * self.calcOswaldEfficicency())
    
    def calcAspectRatio(self):
        return (self.wingSpan ** 2) / self.wingArea
