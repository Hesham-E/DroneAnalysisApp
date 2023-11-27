from .AtmosphereConditions import AtmosphereConditions
from .DragLiftCoefficientInterface import DragLiftCoefficientInterface
from .MotorTableInterface import MotorTableInterface
from .Mission import *
import math


G_ACCEL = 9.80665
UNDER_HOVER_FORCE = 0.5

class Drone:
    def __init__(self, 
                 wingSpan, wingArea, wingThickness,
                 vStabilizerLen, vStabilizerWidth,
                 airFoil,
                 fuselageRadius, 
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
        self.wingThickness = wingThickness
        self.airFoil = int(airFoil)
        self.reynoldsNum = int(reynoldsNum)
        
        self.vStabilizerLen = vStabilizerLen
        self.vStabilizerWidth = vStabilizerWidth

        self.fuselageRadius = fuselageRadius

        self.weight = weight
        self.loadWeight = mission.parameters["loadWeight"]

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
        self.dragLiftInterface = DragLiftCoefficientInterface(f"./ModelLayer/data/airfoils/xf-naca{self.airFoil}-il-{self.reynoldsNum}_Subset_1.csv")
        self.cruiseMotorTableInterface = MotorTableInterface(cruiseMotorTablePath)
        self.vtolMotorTableInterface = MotorTableInterface(vtolMotorTablePath)

        if self.pressure == None:
            self.pressure = self.atmConditions.calcPressure(self.cruiseAltitude, self.temperature)
        elif self.temperature == None:
            self.temperature = self.atmConditions.calcAltitude(self.pressure, self.temperature)

    def calcFrontalArea(self):
        wingArea = (self.wingSpan - self.fuselageRadius * 2) * self.wingThickness
        fuselageArea = (self.fuselageRadius * math.pi) ** 2
        vStabilizerArea = self.vStabilizerLen * self.vStabilizerWidth

        return wingArea + fuselageArea + vStabilizerArea
    
    def calcStallSpeed(self):
        airDensity = self.atmConditions.calcIdealDensityAltitude(self.pressure, self.temperature)
        liftCoefficient = self.dragLiftInterface.getLiftCoefficient(self.angleOfAttack, self.wingSpan, self.wingArea, self.liftDistribution)
        
        vStallSquared = ( 2 * (self.weight + self.loadWeight + self.batteryWeight) ) / ( self.wingArea * airDensity * liftCoefficient )
        return math.sqrt(vStallSquared)
    
    def calcMaxSpeed(self):
        thrust = self.cruiseMotorTableInterface.getMaxThrust()
        airDensity = self.atmConditions.calcIdealDensityAltitude(self.pressure, self.temperature)
        dragCoefficient = self.dragLiftInterface.getDragCoefficient(self.angleOfAttack)
        
        vMaxSquared = (2 * thrust) / (airDensity * dragCoefficient * self.calcFrontalArea())

        return math.sqrt(vMaxSquared)
    
    def calcLift(self):
        airDensity = self.atmConditions.calcIdealDensityAltitude(self.pressure, self.temperature)
        liftCoefficient = self.dragLiftInterface.getLiftCoefficient(self.angleOfAttack, self.wingSpan, self.wingArea, self.liftDistribution)

        return 0.5 * airDensity * ( self.calcMaxSpeed() ** 2 ) * self.wingArea * liftCoefficient

    def calcLiftInducedDrag(self):
        airDensity = self.atmConditions.calcIdealDensityAltitude(self.pressure, self.temperature)
        weight = self.weight + self.loadWeight + self.batteryWeight
        weightChordRatio = ( weight /  airDensity ) ** 2
        q = 0.5 * airDensity * math.pi * ( self.calcMaxSpeed() ) ** 2

        return (self.ellipticalDistribution * weightChordRatio) / (q * math.pi)

    def calcParasiticDrag(self):
        airDensity = self.atmConditions.calcIdealDensityAltitude(self.pressure, self.temperature)
        q = 0.5 * airDensity * math.pi * ( self.calcMaxSpeed() ) ** 2
        liftCoefficent = self.dragLiftInterface.getLiftCoefficient(self.angleOfAttack, self.wingSpan, self.wingArea, self.liftDistribution)
        parasiticDragoefficent = self.dragLiftInterface.getParasiticDragCoefficient(self.angleOfAttack)

        return ( parasiticDragoefficent + self.ellipticalDistribution * (liftCoefficent ** 2) ) / (q * self.wingArea)

    def calcDrag(self):        
        liftCoefficient = self.dragLiftInterface.getLiftCoefficient(self.angleOfAttack, self.wingSpan, self.wingArea, self.liftDistribution)
        aspectRatio = self.wingSpan ** 2 / self.wingArea 
        liftInducedDragCoefficient = liftCoefficient ** 2 / (math.pi * self.ellipticalDistribution * aspectRatio)
        
        dragCoefficient = self.dragLiftInterface.getDragCoefficient(self.angleOfAttack)
        dragCoefficient += liftInducedDragCoefficient

        airDensity = self.atmConditions.calcIdealDensityAltitude(self.pressure, self.temperature)
        q = 0.5 * airDensity * math.pi * ( self.calcMaxSpeed() ) ** 2
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
        densityAltitude = self.atmConditions.calcIdealDensityAltitude(self.pressure, self.temperature)
        totalWeight = self.weight + self.loadWeight + self.batteryWeight

        time = ( (2 * totalWeight) / (densityAltitude * dragCoefficient * self.wingArea) ) * (1 / stallSpeed - 1 / cruiseSpeed)
        distance = ( (2 * totalWeight) / (densityAltitude * dragCoefficient * self.wingArea) ) * math.log(stallSpeed / cruiseSpeed)
        return time, distance

    def calcPeriod6(self):
        cruiseSpeed = self.calcCruiseSpeed()
        stallSpeed = self.calcStallSpeed()
        dragCoefficient = self.dragLiftInterface.getDragCoefficient(self.angleOfAttack)
        densityAltitude = self.atmConditions.calcIdealDensityAltitude(self.pressure, self.temperature)
        totalWeight = self.weight + self.loadWeight + self.batteryWeight
        time5, distance5 = self.calcPeriod5()

        time6 = ( (2 * totalWeight) / (densityAltitude * dragCoefficient * self.wingArea) ) * (2 - 1 / cruiseSpeed) - time5
        distance6 = ( (2 * totalWeight) / (densityAltitude * dragCoefficient * self.wingArea) ) * math.log(stallSpeed / cruiseSpeed) - distance5
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
        elif self.mission.performance == MissionPerformance.MINIMAL:
            return self.calcStallSpeed()
        else: # Default to efficient
            return ( (self.calcMaxSpeed() + self.calcStallSpeed()) / 2 )
    
    def calcCruiseThrust(self):
        airDensity = self.atmConditions.calcIdealDensityAltitude(self.pressure, self.temperature)
        dragCoefficient = self.dragLiftInterface.getDragCoefficient(self.angleOfAttack)
        cruiseSpeed = self.calcCruiseSpeed()

        return ( (cruiseSpeed ** 2) * airDensity * dragCoefficient * self.calcFrontalArea() * 0.5 )
