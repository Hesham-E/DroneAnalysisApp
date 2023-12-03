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

        vMaxSquared = (thrustAreaRatio + wingLoading * math.sqrt((thrustWeightRatio ** 2) - 4 * self.calcZeroLiftDragCoefficient() * coefficientK)) / (airDensity * self.calcZeroLiftDragCoefficient())
        return math.sqrt(vMaxSquared)
    
    def calcLift(self):
        airDensity = self.atmConditions.calcAirDensity(self.pressure, self.temperature)
        liftCoefficient = self.dragLiftInterface.getLiftCoefficient(self.angleOfAttack, self.wingSpan, self.wingArea, self.liftDistribution)

        return 0.5 * airDensity * ( self.calcCruiseSpeed() ** 2 ) * self.wingArea * liftCoefficient
    
    def calcZeroLiftDragCoefficient(self):
        skinFrictionCoefficient = 0.0776 * ((math.log(10000000, 10) - 1.88) ** -2) + 60 / 10000000
        skinFrictionCoefficient = skinFrictionCoefficient * 1.5 # According to Anderson this 1.5 is needed if it is not a flat plane

        wettedAndReferenceAreaRatio = 4 # Can be approximated as this according to Anderson's textbook for single propellor planes
        return wettedAndReferenceAreaRatio * skinFrictionCoefficient

    def calcLiftInducedDrag(self):
        airDensity = self.atmConditions.calcAirDensity(self.pressure, self.temperature)
        weight = self.weight + self.loadWeight + self.batteryWeight
        weightChordRatio = ( weight /  airDensity ) ** 2
        q = 0.5 * airDensity * math.pi * ( self.calcCruiseSpeed() ) ** 2

        return (self.ellipticalDistribution * weightChordRatio) / (q * math.pi)

    def calcParasiticDrag(self):
        airDensity = self.atmConditions.calcAirDensity(self.pressure, self.temperature)
        q = 0.5 * airDensity * math.pi * ( self.calcCruiseSpeed() ) ** 2
        liftCoefficent = self.dragLiftInterface.getLiftCoefficient(self.angleOfAttack, self.wingSpan, self.wingArea, self.liftDistribution)
        wingParasiticDragCoefficient = self.dragLiftInterface.getParasiticDragCoefficient(self.angleOfAttack)

        skinRoughnessFactor = 6.34 * (10 ** -6)
        reynoldsCutoff = 38.21 * ( (self.fuselageLength / skinRoughnessFactor) ** 1.053 )
        reynoldsCutoff = reynoldsCutoff if 200000 > reynoldsCutoff else 200000
        skinFrictionCoefficient = 0.0776 * ((math.log(reynoldsCutoff, 10) - 1.88) ** -2) + 60 / reynoldsCutoff
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
    
    def calcPeriod1(self):
        maxThrust = self.vtolMotorTableInterface.getMaxThrust() * 4
        maxPower = self.vtolMotorTableInterface.getMaxPower() * 4
        underHoverThrust = (self.weight + self.loadWeight + self.batteryWeight) * G_ACCEL * UNDER_HOVER_FORCE
        underHoverPower = self.vtolMotorTableInterface.getPowerAtThrust(underHoverThrust / 4) * 4
        hoverThrust = (self.weight + self.loadWeight + self.batteryWeight) * G_ACCEL
        hoverPower = self.vtolMotorTableInterface.getPowerAtThrust(hoverThrust / 4) * 4
        totalWeight = self.weight + self.loadWeight + self.batteryWeight

        powerHeightRatio = hoverPower * self.targetAltitude / self.ascentDecentSpeed
        maxPowerThrustEnergy = (maxPower - hoverPower / 2) / (maxThrust / totalWeight - G_ACCEL)
        underPowerThrustEnergy = (underHoverPower - hoverPower / 2) / (G_ACCEL - underHoverThrust / totalWeight)
        
        climbEnergy = (maxPowerThrustEnergy + underPowerThrustEnergy) * self.ascentDecentSpeed + powerHeightRatio

        maxThrustTime = 0.5 / (maxThrust / totalWeight - G_ACCEL)
        underThrustTime = 0.5 / (G_ACCEL - underHoverThrust / totalWeight)
        speedHeightRatio = self.targetAltitude / self.ascentDecentSpeed

        climbTime = (maxThrustTime + underThrustTime) * self.ascentDecentSpeed + speedHeightRatio

        return climbTime, climbEnergy
    
    def calcPeriod2(self):
        hoverThrust = (self.weight + self.loadWeight + self.batteryWeight) * G_ACCEL
        hoverPower = self.vtolMotorTableInterface.getPowerAtThrust(hoverThrust / 4) * 4
        cruiseSpeed = self.calcCruiseSpeed()
        cruiseThrust = self.calcCruiseThrust()
        totalWeight = self.weight + self.loadWeight + self.batteryWeight
        stallSpeed = self.calcStallSpeed()

        energy = hoverPower * ( cruiseSpeed / (cruiseThrust / totalWeight) ) *  math.atanh(stallSpeed / cruiseSpeed)
        time = ( cruiseSpeed / (cruiseThrust / totalWeight) ) * math.atanh(stallSpeed / cruiseSpeed)

        return time, energy
    
    def calcPeriod23(self):
        cruiseSpeed = self.calcCruiseSpeed()
        cruiseThrust = self.calcCruiseThrust()
        cruisePower = self.cruiseMotorTableInterface.getPowerAtThrust(cruiseThrust)
        totalWeight = self.weight + self.loadWeight + self.batteryWeight

        time = cruiseSpeed / (cruiseThrust / totalWeight) * math.atanh(0.99)
        distance = (cruiseSpeed ** 2) / (cruiseThrust / totalWeight) * math.log( math.cosh( math.atanh(0.99) ) )
        energy = cruiseSpeed / (cruiseThrust / totalWeight) * cruisePower * math.atanh(0.99)

        return time, distance, energy
    
    def calcPeriod5(self):
        stallSpeed = self.calcStallSpeed()
        cruiseSpeed = self.calcCruiseSpeed()
        dragCoefficient = self.dragLiftInterface.getDragCoefficient(self.angleOfAttack)
        airDensity = self.atmConditions.calcAirDensity(self.pressure, self.temperature)
        totalWeight = self.weight + self.loadWeight + self.batteryWeight

        time = ( (2 * totalWeight) / (airDensity * dragCoefficient * self.wingArea) ) * (1 / stallSpeed - 1 / cruiseSpeed)
        distance = ( (2 * totalWeight) / (airDensity * dragCoefficient * self.wingArea) ) * math.log(stallSpeed / cruiseSpeed)
        return time, distance

    def calcPeriod6(self):
        cruiseSpeed = self.calcCruiseSpeed()
        stallSpeed = self.calcStallSpeed()
        dragCoefficient = self.dragLiftInterface.getDragCoefficient(self.angleOfAttack)
        airDensity = self.atmConditions.calcAirDensity(self.pressure, self.temperature)
        totalWeight = self.weight + self.loadWeight + self.batteryWeight
        time5, distance5 = self.calcPeriod5()

        time6 = ( (2 * totalWeight) / (airDensity * dragCoefficient * self.wingArea) ) * (2 - 1 / cruiseSpeed) - time5
        distance6 = ( (2 * totalWeight) / (airDensity * dragCoefficient * self.wingArea) ) * math.log(stallSpeed / cruiseSpeed) - distance5
        hoverForce = (self.weight + self.loadWeight + self.batteryWeight) * G_ACCEL
        energy6 = time6 * self.vtolMotorTableInterface.getPowerAtThrust( hoverForce / 4 ) * 4

        return time6, distance6, energy6
    
    def calcPeriod7(self):
        maxPower = self.vtolMotorTableInterface.getMaxPower()
        maxThrust = self.vtolMotorTableInterface.getMaxThrust()
        hoverForce = (self.weight + self.loadWeight + self.batteryWeight) * G_ACCEL
        hoverPower = self.vtolMotorTableInterface.getPowerAtThrust(hoverForce / 4) * 4
        underHoverThrust = (self.weight + self.loadWeight + self.batteryWeight) * G_ACCEL * UNDER_HOVER_FORCE
        underHoverPower = self.vtolMotorTableInterface.getPowerAtThrust(underHoverThrust / 4) * 4
        totalWeight = self.weight + self.loadWeight + self.batteryWeight

        # powerHeightRatio = hoverPower * abs(self.targetAltitude - self.cruiseAltitude) / self.ascentDecentSpeed
        powerHeightRatio = hoverPower * self.targetAltitude / self.ascentDecentSpeed # cruiseAltitude is ambigious at the moment
        maxPowerThrustRatio = (maxPower - hoverPower / 2) / (maxThrust / totalWeight - G_ACCEL)
        underPowerThrustRatio = (underHoverPower - hoverPower / 2) / (G_ACCEL - underHoverThrust / totalWeight)
        
        decentEnergy = (maxPowerThrustRatio + underPowerThrustRatio) * self.ascentDecentSpeed + powerHeightRatio

        maxThrustTimeRatio = 0.5 / (maxThrust / totalWeight - G_ACCEL)
        underThrustTimeRatio = 0.5 / (G_ACCEL - underHoverThrust / totalWeight)
        # speedHeightRatio = abs(self.targetAltitude - self.cruiseAltitude) / self.ascentDecentSpeed
        speedHeightRatio = self.targetAltitude / self.ascentDecentSpeed # cruiseAltitude is ambigious at the moment

        decentTime = (maxThrustTimeRatio + underThrustTimeRatio) * self.ascentDecentSpeed + speedHeightRatio

        return decentTime, decentEnergy
    
    def calcPeriod4(self):
        time23, distance23, energy23 = self.calcPeriod23()
        time5, distance5 = self.calcPeriod5()
        time6, distance6, energy6 = self.calcPeriod6()

        cruiseSpeed = self.calcCruiseSpeed()
        cruisePower = self.cruiseMotorTableInterface.getPowerAtThrust(self.calcCruiseThrust())

        distance4 = self.targetDistance - distance23 - distance5 - distance6
        time4 = distance4 / cruiseSpeed
        energy4 = cruisePower * time4

        return time4, distance4, energy4
    
    def calcMaxRange(self):
        time23, dist23, energy23 = self.calcPeriod23()
        time4, dist4, energy4 = self.calcPeriod4()

        return dist4 + dist23
    
    def calcCruiseSpeed(self):
        if self.mission.performance == MissionPerformance.PERFORMANCE:
            return self.calcMaxSpeed()
        elif self.mission.performance == MissionPerformance.EFFICIENT:
            airDensity = self.atmConditions.calcAirDensity(self.pressure, self.temperature)
            thrustWeightRatio = self.calcEfficientThrust() / self.totalWeight # So we get the error checking from cruiseThrust()
            wingLoading = self.totalWeight / self.wingArea

            return math.sqrt(thrustWeightRatio * wingLoading / (airDensity * self.calcZeroLiftDragCoefficient()))
    
    def calcCruiseThrust(self):
        if self.mission.performance == MissionPerformance.PERFORMANCE:
            return self.cruiseMotorTableInterface.getMaxThrust()
        elif self.mission.performance == MissionPerformance.EFFICIENT:
            return self.calcEfficientThrust()
    
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
