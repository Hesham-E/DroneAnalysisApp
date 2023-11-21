from .AtmosphereConditions import AtmosphereConditions
from .DragLiftCoefficientInterface import DragLiftCoefficientInterface
from .MotorTableInterface import MotorTableInterface
import math


G_ACCEL = 9.80665
UNDER_HOVER_FORCE = 0.15

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
        self.ascentDecentSpeed = ascentDecentSpeed

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
    
    def calcPeriod2(self):
        maxThrust = self.cruiseMotorTableInterface.getMaxThrust()
        cruiseAccel = maxThrust / (self.weight + self.loadWeight + self.batteryWeight)
        time2 = ( self.calcMaxSpeed(self.pressure, self.temperature) / cruiseAccel ) * math.atanh( self.calcStallSpeed(self.pressure, self.temperature) / self.calcMaxSpeed(self.pressure, self.temperature) )
        
        hoverForce = (self.weight + self.loadWeight + self.batteryWeight) * G_ACCEL
        energy2 = time2 * self.vtolMotorTableInterface.getPowerAtThrust(hoverForce / 4) * 4

        return time2, energy2
    
    def calcPeriod23(self):
        maxSpeed = self.calcMaxSpeed(self.pressure, self.temperature)

        maxThrust = self.cruiseMotorTableInterface.getMaxThrust()
        cruiseAccel = maxThrust / (self.weight + self.loadWeight + self.batteryWeight)
        time23 = (maxSpeed / cruiseAccel) * math.atanh(0.99)
        dist23 = maxSpeed * math.log( math.cosh(time23 * cruiseAccel / maxSpeed) ) / (cruiseAccel / maxSpeed)
        energy23 = time23 * self.cruiseMotorTableInterface.getMaxThrust()

        return time23, dist23, energy23
    
    def calcPeriod5(self):
        stallSpeed = self.calcStallSpeed(self.pressure, self.temperature)
        maxSpeed = self.calcMaxSpeed(self.pressure, self.temperature)
        dragCoefficient = self.dragLiftInterface.getDragCoefficient(self.angleOfAttack)
        densityAltitude = self.atmConditions.calcIdealDensityAltitude(self.pressure, self.temperature)
        frontalArea = self.calcFrontalArea()
        totalWeight = self.weight + self.loadWeight + self.batteryWeight

        time5 = (1 / stallSpeed - 1 / maxSpeed) - ( densityAltitude * dragCoefficient * frontalArea / (2 * totalWeight))
        return time5

    def calcPeriod6(self):
        maxSpeed = self.calcMaxSpeed(self.pressure, self.temperature)
        dragCoefficient = self.dragLiftInterface.getDragCoefficient(self.angleOfAttack)
        densityAltitude = self.atmConditions.calcIdealDensityAltitude(self.pressure, self.temperature)
        frontalArea = self.calcFrontalArea()
        totalWeight = self.weight + self.loadWeight + self.batteryWeight
        time5 = self.calcPeriod5()

        time6 = (1 / 0.5 - 1 / maxSpeed) - ( densityAltitude * dragCoefficient * frontalArea / (2 * totalWeight)) - time5
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

        cruisePower = self.cruiseMotorTableInterface.getMaxPower()
        time4 = ( self.batteryEnergy - energy1 - energy2 - energy23 - energy6 - energy7 - self.auxPowerCon * (time1 + time23 + time5 + time6 + time7) ) / (cruisePower + self.auxPowerCon)
        dist4 = time4 * self.calcMaxSpeed(self.pressure, self.temperature)

        return time4, dist4
    
    def calcMaxRange(self):
        time23, dist23, energy23 = self.calcPeriod23()
        time4, dist4 = self.calcPeriod4()

        return dist4 + dist23
