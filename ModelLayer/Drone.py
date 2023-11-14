from .AtmosphereConditions import AtmosphereConditions
from .DragLiftCoefficientInterface import DragLiftCoefficientInterface
from .MotorTableInterface import MotorTableInterface
import math

class Drone:
    def __init__(self, 
                 wingSpan, wingArea, wingThickness,
                 vStabilizerLen, vStabilizerWidth,
                 fuselageRadius, 
                 weight, loadWeight, 
                 angleOfAttack, 
                 batteryWeight, batteryCapacity, batteryVoltage,
                 targetAltitude,
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
        self.batteryVoltage = batteryVoltage
        self.batteryEnergy = batteryVoltage * batteryCapacity * 3.6 * 0.94

        self.targetAltitude = targetAltitude

        self.ellipticalDistribution = 1.1

        self.atmConditions = AtmosphereConditions()
        self.dragLiftInterface = DragLiftCoefficientInterface("./ModelLayer/xf-naca2408-il-500000_Subset_1.csv")
        self.motorTableInterface = MotorTableInterface(motorTablePath)

    def calcFrontalArea(self):
        wingArea = (self.wingSpan - self.fuselageRadius * 2) * self.wingThickness
        fuselageArea = (self.fuselageRadius * math.pi) ** 2
        vStabilizerArea = self.vStabilizerLen * self.vStabilizerWidth

        return wingArea + fuselageArea + vStabilizerArea
    
    def calcStallSpeed(self, pressure, temperature):
        airDensity = self.atmConditions.calcIdealDensityAltitude(pressure, temperature)
        liftCoefficient = self.dragLiftInterface.getLiftCoefficient(self.angleOfAttack)
        
        vStallSquared = ( 2 * (self.weight + self.loadWeight + self.batteryWeight) ) / ( self.wingArea * airDensity * liftCoefficient )
        return math.sqrt(vStallSquared)
    
    def calcMaxSpeed(self, pressure, temperature):
        thrust = self.motorTableInterface.getMaxThrust()
        airDensity = self.atmConditions.calcIdealDensityAltitude(pressure, temperature)
        dragCoefficient = self.dragLiftInterface.getDragCoefficient(self.angleOfAttack)
        
        vMaxSquared = (2 * thrust) / (airDensity * dragCoefficient * self.calcFrontalArea())
        return math.sqrt(vMaxSquared)
    
    def calcLift(self, pressure, temperature):
        airDensity = self.atmConditions.calcIdealDensityAltitude(pressure, temperature)
        liftCoefficient = self.dragLiftInterface.getLiftCoefficient(self.angleOfAttack)

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
        liftCoefficent = self.dragLiftInterface.getLiftCoefficient(self.angleOfAttack)
        parasiticDragoefficent = self.dragLiftInterface.getParasiticDragCoefficient(self.angleOfAttack)

        return ( parasiticDragoefficent + self.ellipticalDistribution * (liftCoefficent ** 2) ) / (q * self.wingArea)

    def calcDrag(self, pressure, temperature):
        airDensity = self.atmConditions.calcIdealDensityAltitude(pressure, temperature)
        q = 0.5 * airDensity * math.pi * ( self.calcMaxSpeed(pressure, temperature) ) ** 2
        dragCoefficient = self.dragLiftInterface.getDragCoefficient(self.angleOfAttack)

        return dragCoefficient * q * self.wingArea