from .AtmosphereConditions import AtmosphereConditions
from .DragLiftCoefficientInterface import DragLiftCoefficientInterface
from .MotorTableInterface import MotorTableInterface
import math


G_ACCEL = 9.80665
UNDER_HOVER_FORCE = 0.5

class Drone:
    def __init__(self, 
                 wingSpan, wingArea, wingThickness,
                 vStabilizerLen, vStabilizerWidth,
                 fuselageRadius, 
                 weight, loadWeight, 
                 angleOfAttack, 
                 batteryWeight, batteryCapacity, batteryVoltage,
                 targetAltitude,
                 cruiseMotorTablePath, vtolMotorTablePath,
                 auxPowerCon,
                 ascentDecentSpeed,
                 pressure, temperature):
        
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
        self.batteryVoltage = batteryVoltage
        self.batteryEnergy = batteryVoltage * batteryCapacity * 3.6 * 0.94

        self.targetAltitude = targetAltitude
        self.cruiseAltitude = 1 #TODO: change this
        self.ascentDecentSpeed = ascentDecentSpeed

        self.targetDistance = 1 #TODO: change this

        self.auxPowerCon = auxPowerCon

        self.pressure = pressure
        self.temperature = temperature

        self.ellipticalDistribution = 1.1
        self.liftDistribution = 0.95

        self.atmConditions = AtmosphereConditions()
        self.dragLiftInterface = DragLiftCoefficientInterface("./ModelLayer/xf-naca2408-il-500000_Subset_1.csv")
        self.cruiseMotorTableInterface = MotorTableInterface(cruiseMotorTablePath)
        self.vtolMotorTableInterface = MotorTableInterface(vtolMotorTablePath)

    def calcFrontalArea(self):
        wingArea = (self.wingSpan - self.fuselageRadius * 2) * self.wingThickness
        fuselageArea = (self.fuselageRadius * math.pi) ** 2
        vStabilizerArea = self.vStabilizerLen * self.vStabilizerWidth

        return wingArea + fuselageArea + vStabilizerArea
    
    def calcStallSpeed(self, pressure, temperature):
        airDensity = self.atmConditions.calcIdealDensityAltitude(pressure, temperature)
        liftCoefficient = self.dragLiftInterface.getLiftCoefficient(self.angleOfAttack, self.wingSpan, self.wingArea, self.liftDistribution)
        
        vStallSquared = ( 2 * (self.weight + self.loadWeight + self.batteryWeight) ) / ( self.wingArea * airDensity * liftCoefficient )
        return math.sqrt(vStallSquared)
    
    def calcMaxSpeed(self, pressure, temperature):
        thrust = self.cruiseMotorTableInterface.getMaxThrust()
        airDensity = self.atmConditions.calcIdealDensityAltitude(pressure, temperature)
        dragCoefficient = self.dragLiftInterface.getDragCoefficient(self.angleOfAttack)
        
        vMaxSquared = (2 * thrust) / (airDensity * dragCoefficient * self.calcFrontalArea())

        return math.sqrt(vMaxSquared)
    
    def calcLift(self, pressure, temperature):
        airDensity = self.atmConditions.calcIdealDensityAltitude(pressure, temperature)
        liftCoefficient = self.dragLiftInterface.getLiftCoefficient(self.angleOfAttack, self.wingSpan, self.wingArea, self.liftDistribution)

        return 0.5 * airDensity * ( self.calcMaxSpeed(pressure, temperature) ** 2 ) * self.wingArea * liftCoefficient

    def calcLiftInducedDrag(self, pressure, temperature):
        airDensity = self.atmConditions.calcIdealDensityAltitude(pressure, temperature)
        weight = self.weight + self.loadWeight + self.batteryWeight
        weightChordRatio = ( weight /  airDensity ) ** 2
        q = 0.5 * airDensity * math.pi * ( self.calcMaxSpeed(pressure, temperature) ) ** 2

        return (self.ellipticalDistribution * weightChordRatio) / (q * math.pi)

    def calcParasiticDrag(self, pressure, temperature):
        airDensity = self.atmConditions.calcIdealDensityAltitude(pressure, temperature)
        q = 0.5 * airDensity * math.pi * ( self.calcMaxSpeed(pressure, temperature) ) ** 2
        liftCoefficent = self.dragLiftInterface.getLiftCoefficient(self.angleOfAttack, self.wingSpan, self.wingArea, self.liftDistribution)
        parasiticDragoefficent = self.dragLiftInterface.getParasiticDragCoefficient(self.angleOfAttack)

        return ( parasiticDragoefficent + self.ellipticalDistribution * (liftCoefficent ** 2) ) / (q * self.wingArea)

    def calcDrag(self, pressure, temperature):        
        liftCoefficient = self.dragLiftInterface.getLiftCoefficient(self.angleOfAttack, self.wingSpan, self.wingArea, self.liftDistribution)
        aspectRatio = self.wingSpan ** 2 / self.wingArea 
        liftInducedDragCoefficient = liftCoefficient ** 2 / (math.pi * self.ellipticalDistribution * aspectRatio)
        
        dragCoefficient = self.dragLiftInterface.getDragCoefficient(self.angleOfAttack)
        dragCoefficient += liftInducedDragCoefficient

        airDensity = self.atmConditions.calcIdealDensityAltitude(pressure, temperature)
        q = 0.5 * airDensity * math.pi * ( self.calcMaxSpeed(pressure, temperature) ) ** 2
        return dragCoefficient * q * self.wingArea
    
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
        cruiseSpeed = self.dummyFunction()
        cruiseThrust = self.dummyFunction()
        totalWeight = self.weight + self.loadWeight + self.batteryWeight
        stallSpeed = self.calcStallSpeed(self.pressure, self.temperature)

        energy = hoverPower * ( cruiseSpeed / (cruiseThrust / totalWeight) ) *  math.atanh(stallSpeed / cruiseSpeed)
        time = ( cruiseSpeed / (cruiseThrust / totalWeight) ) * math.atanh(stallSpeed / cruiseSpeed)

        return time, energy
    
    def calcPeriod23(self):
        cruiseSpeed = self.dummyFunction()
        cruiseThrust = self.dummyFunction()
        cruisePower = self.cruiseMotorTableInterface.getPowerAtThrust(cruiseThrust)
        totalWeight = self.weight + self.loadWeight + self.batteryWeight

        time = cruiseSpeed / (cruiseThrust / totalWeight) * math.atanh(0.99)
        distance = (cruiseSpeed ** 2) / (cruiseThrust / totalWeight) * math.log( math.cosh( math.atanh(0.99) ) )
        energy = cruiseSpeed / (cruiseThrust / totalWeight) * cruisePower * math.atanh(0.99)

        return time, distance, energy
    
    def calcPeriod5(self):
        stallSpeed = self.calcStallSpeed(self.pressure, self.temperature)
        cruiseSpeed = self.dummyFunction()
        dragCoefficient = self.dragLiftInterface.getDragCoefficient(self.angleOfAttack)
        densityAltitude = self.atmConditions.calcIdealDensityAltitude(self.pressure, self.temperature)
        totalWeight = self.weight + self.loadWeight + self.batteryWeight

        time = ( (2 * totalWeight) / (densityAltitude * dragCoefficient * self.wingArea) ) * (1 / stallSpeed - 1 / cruiseSpeed)
        distance = ( (2 * totalWeight) / (densityAltitude * dragCoefficient * self.wingArea) ) * math.log(stallSpeed / cruiseSpeed)
        return time, distance

    def calcPeriod6(self):
        cruiseSpeed = self.dummyFunction()
        stallSpeed = self.calcStallSpeed(self.pressure, self.temperature)
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

        powerHeightRatio = hoverPower * abs(self.targetAltitude - self.cruiseAltitude) / self.ascentDecentSpeed
        maxPowerThrustRatio = (maxPower - hoverPower / 2) / (maxThrust / totalWeight - G_ACCEL)
        underPowerThrustRatio = (underHoverPower - hoverPower / 2) / (G_ACCEL - underHoverThrust / totalWeight)
        
        decentEnergy = (maxPowerThrustRatio + underPowerThrustRatio) * self.ascentDecentSpeed + powerHeightRatio

        maxThrustTimeRatio = 0.5 / (maxThrust / totalWeight - G_ACCEL)
        underThrustTimeRatio = 0.5 / (G_ACCEL - underHoverThrust / totalWeight)
        speedHeightRatio = abs(self.targetAltitude - self.cruiseAltitude) / self.ascentDecentSpeed

        decentTime = (maxThrustTimeRatio + underThrustTimeRatio) * self.ascentDecentSpeed + speedHeightRatio

        return decentTime, decentEnergy
    
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
        time23, distance23, energy23 = self.calcPeriod23()
        time5, distance5 = self.calcPeriod5()
        time6, distance6, energy6 = self.calcPeriod6()

        cruiseSpeed = self.dummyFunction()
        cruisePower = self.cruiseMotorTableInterface.getPowerAtThrust(cruiseSpeed)

        distance4 = self.targetDistance - distance23 - distance5 - distance6
        time4 = distance4 / cruiseSpeed
        energy4 = cruisePower * time4

        return time4, distance4, energy4
    
    def calcMaxRange(self):
        time23, dist23, energy23 = self.calcPeriod23()
        time4, dist4 = self.calcPeriod4()

        return dist4 + dist23
    
    def dummyFunction(self):
        # TODO: replace all instances of dummyFunction() with real logic
        return 1
