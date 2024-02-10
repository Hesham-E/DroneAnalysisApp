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
        self.reynoldsNum = 100000 # Reynolds number for model aircrafts

        self.fuselageRadius = fuselageRadius
        self.fuselageLength = fuselageLength

        # IMPORTANT NOTE:
        # Anderson's book uses sometimes uses W/S, a variable W for weight.
        # This appears to be weight in it's most literal sense.
        # As in order to convert the WING LOADING equations found in this book,
        # we must multiply any W by acceleration of gravity.
        # We surmise this may be to the imperial unit of "slug" found in wing loading.
        self.weight = weight
        self.loadWeight = mission.parameters["loadWeight"]
        self.totalMass = weight + batteryWeight + mission.parameters["loadWeight"]
        self.totalWeight = self.totalMass * G_ACCEL # W is used

        self.angleOfAttack = angleOfAttack

        self.batteryWeight = batteryWeight
        self.batteryCapacity = batteryCapacity
        self.batteryVoltage = batteryVoltage
        self.batteryEnergy = batteryVoltage * batteryCapacity * 3.6 * 0.94

        self.mission = mission

        self.cruiseAltitude = mission.parameters["cruiseAltitude"] # TODO: Replace this as per a mission profile, for the none simple ones
        self.currentAltitude = mission.parameters["baseStationAltitude"]
        self.ascentDecentSpeed = ascentDecentSpeed
        if mission.profile == MissionProfile.VTOL_STRAIGHT:
            self.mission.parameters["vtolClimb"] = self.cruiseAltitude
        print(self.mission.parameters)

        self.targetDistance = mission.parameters["missionDistance"]

        self.auxPowerCon = auxPowerCon

        self.pressure = mission.parameters["pressure"]
        self.temperature = mission.parameters["temperature"]

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
    
    def calcLift(self, max = False):
        airDensity = self.atmConditions.calcAirDensity(self.pressure, self.temperature)
        liftCoefficient = self.dragLiftInterface.getLiftCoefficient(self.angleOfAttack, self.wingSpan, self.wingArea, self.liftDistribution)

        if ( max ):
            return 0.5 * airDensity * ( self.calcEfficientSpeed() ** 2 ) * self.wingArea * liftCoefficient
        else:
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

        # should never be negative, abs() just makes it easier to test the code with dummy values
        return abs( self.wingArea - cR * self.fuselageRadius )
    
    def calcZeroLiftDragCoefficient(self):
        skinFrictionCoefficient = 0.42 / ( math.log(0.056 * self.reynoldsNum ) ** 2 )
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

        skinFrictionCoefficient = 0.42 / ( math.log(0.056 * self.reynoldsNum ) ** 2 )
        skinFrictionCoefficient = skinFrictionCoefficient * 1.5 # According to Anderson this 1.5 is needed if it is not a flat plane

        fuselageFormFactor = 1 + (60 / ((self.fuselageLength / (2 * self.fuselageRadius)) ** 3) + (self.fuselageLength / (2 * self.fuselageRadius) / 400))
        fuselageArea = math.pi * 2 * self.fuselageRadius * self.fuselageLength * (abs(1 - 2 / (self.fuselageLength / (self.fuselageRadius * 2))) ** (2/3)) * (1 + 1 / ((self.fuselageLength / (2 * self.fuselageRadius)) ** 2))
        fuseLageCoefficient = skinFrictionCoefficient * fuselageFormFactor * (fuselageArea / self.wingArea)
        
        return ( (wingParasiticDragCoefficient + fuseLageCoefficient) + self.ellipticalDistribution * (liftCoefficent ** 2) ) / (q * self.wingArea)

    def calcDrag(self, max = False):        
        liftCoefficient = self.dragLiftInterface.getLiftCoefficient(self.angleOfAttack, self.wingSpan, self.wingArea, self.liftDistribution)
        liftInducedDragCoefficient = liftCoefficient ** 2 / (math.pi * self.ellipticalDistribution * self.calcAspectRatio())
        
        dragCoefficient = self.dragLiftInterface.getDragCoefficient(self.angleOfAttack)
        dragCoefficient += liftInducedDragCoefficient

        airDensity = self.atmConditions.calcAirDensity(self.pressure, self.temperature)

        if (max):
            q = 0.5 * airDensity * math.pi * ( self.calcEfficientSpeed() ) ** 2
        else:
            q = 0.5 * airDensity * math.pi * ( self.calcCruiseSpeed() ) ** 2
        return dragCoefficient * q * self.wingArea
    
    def calcMaxLiftDragRatio(self):
        return self.calcLift( max = True ) / self.calcDrag( max = True )
    
    def calcRateOfClimb(self):
        velocityROCMax =  2 / self.atmConditions.calcAirDensity( self.pressure, self.temperature ) * \
                          math.sqrt(self.liftDistribution / 3 * self.calcZeroLiftDragCoefficient()) * \
                          self.totalWeight / self.wingArea
        velocityROCMax = velocityROCMax ** 0.5

        return self.cruiseMotorTableInterface.getMechanicalPowerAtThrust( self.cruiseMotorTableInterface.getMaxThrust() ) / self.totalMass \
               - velocityROCMax * 1.155 / ( self.calcMaxLiftDragRatio() )
    
    def calcRateOfDescent(self):
        vThetaMin = math.sqrt( 2 / self.atmConditions.calcAirDensity( self.pressure, self.temperature ) \
                          * math.sqrt( self.liftDistribution / self.calcZeroLiftDragCoefficient() ) \
                          * ( self.totalWeight / self.wingArea ) )
        thetaMin = math.atan( 1 / self.calcMaxLiftDragRatio() )

        return vThetaMin *  math.sin(thetaMin)
    
    def calcFixedWingClimb(self, targetAltitude = None, currentAltitude = None):
        if targetAltitude == None:
            targetAltitude = self.cruiseAltitude
        if currentAltitude == None:
            currentAltitude = self.currentAltitude

        distFWC = targetAltitude - currentAltitude # vertical height
        timeFWC = distFWC / self.calcRateOfClimb()
        energyFWC = self.cruiseMotorTableInterface.getMaxPower() * timeFWC

        # converting distFWC to a horizontal component
        thrust = self.cruiseMotorTableInterface.getMaxThrust()
        
        # abs() for testing with dummy values
        # if statement for testing with dummy values
        sinTheta = abs( thrust / self.totalMass - 1 / self.calcMaxLiftDragRatio() )
        if sinTheta < -1:
            sinTheta = -1
        elif sinTheta > 1:
            sinTheta = 1

        theta = math.asin( sinTheta )
        distFWC = distFWC / math.tan( theta ) # horizontal height

        self.currentAltitude = targetAltitude

        return timeFWC, distFWC, energyFWC
    
    def calcFixedWingDescent(self, targetAltitude = None, currentAltitude = None):
        if targetAltitude == None:
            targetAltitude = self.mission.parameters["vtolDescent"]
        if currentAltitude == None:
            currentAltitude = self.currentAltitude
        
        distFWD = currentAltitude - targetAltitude # vertical height
        timeFWD = distFWD / self.calcRateOfDescent() # time based on vertical speed
        energyFWD = self.auxPowerCon * timeFWD # Unpowered glide
        
        # convert distFWD to a horizontal component
        thetaMin = math.atan( 1 / self.calcMaxLiftDragRatio() )
        distFWD = distFWD / math.tan( thetaMin ) # convert distance to horizontal distance

        self.currentAltitude = targetAltitude

        return timeFWD, distFWD, energyFWD

    def calcVTOLTakeOffAcceleration(self):
        # Acceleration Stage Time
        thrust = self.vtolMotorTableInterface.getMaxThrust() * 4
        takeOffAccel = thrust / self.totalMass - G_ACCEL
        timeTA = self.ascentDecentSpeed / takeOffAccel
        distTA = 0.5 * takeOffAccel * (timeTA ** 2)
        energyTA = self.vtolMotorTableInterface.getMaxPower() * 4 * timeTA
        return timeTA, distTA, energyTA
    
    def calcVTOLTakeOffDeceleration(self):
        # Deceleration Stage Time
        hoverForce = self.totalMass * G_ACCEL * UNDER_HOVER_FORCE
        accel = hoverForce / self.totalMass
        timeTD = self.ascentDecentSpeed / accel
        distTD = self.ascentDecentSpeed * timeTD + 0.5 * accel * (timeTD ** 2)
        energyTD = self.vtolMotorTableInterface.getPowerAtThrust(hoverForce / 4) * timeTD * 4

        return timeTD, distTD, energyTD
    
    def calcTakeOff(self):
        timeTA, distTA, energyTA = self.calcVTOLTakeOffAcceleration()
        timeTD, distTD, energyTD = self.calcVTOLTakeOffDeceleration()

        dist = self.mission.parameters["vtolClimb"] - self.mission.parameters["baseStationAltitude"] - distTA - distTD
        time = dist / self.ascentDecentSpeed

        hoverForce = self.totalMass * G_ACCEL
        energy = time * self.vtolMotorTableInterface.getPowerAtThrust(hoverForce / 4) * 4

        totalTime = timeTA + time + timeTD
        totalDist = distTA + dist + distTD
        totalEnergy = energyTA + energy + energyTD

        self.currentAltitude += totalDist
        
        return totalTime, totalDist, totalEnergy
    
    def calcAccelerationTransitionPeriod(self):
        # Period 2: where we transfer from VTOL to fixed wing mode
        cruiseThrust = self.calcCruiseThrust()
        cruiseAccel = cruiseThrust / self.totalMass
        timeAT = ( self.calcCruiseSpeed() / cruiseAccel ) * math.atanh( self.calcStallSpeed() / self.calcCruiseSpeed() )
        distAT = 0.5 * cruiseAccel * ( timeAT ** 2 )
        
        hoverForce = self.totalMass * G_ACCEL
        energyAT = timeAT * self.vtolMotorTableInterface.getPowerAtThrust(hoverForce / 4) * 4

        return timeAT, distAT, energyAT
    
    def calcAccelerationPeriod(self):
        # Period 23: Acceleration to cruise speed
        cruiseSpeed = self.calcCruiseSpeed()
        cruiseThrust = self.calcCruiseThrust()
        cruiseAccel = cruiseThrust / self.totalMass
        timeA = (cruiseSpeed / cruiseAccel) * math.atanh( 0.99 )
        distA = ( cruiseSpeed ** 2 ) * math.log( math.cosh( timeA * cruiseAccel / cruiseSpeed ) ) / ( cruiseThrust / self.totalMass )
        energyA = timeA * self.cruiseMotorTableInterface.getPowerAtThrust( cruiseThrust )

        return timeA, distA, energyA
    
    def calcVTOLLandingAcceleration(self):
        hoverForce = self.totalMass * G_ACCEL * UNDER_HOVER_FORCE
        accel = hoverForce / self.totalMass - G_ACCEL
        timeLA = self.ascentDecentSpeed / accel
        distLA = self.ascentDecentSpeed * timeLA + 0.5 * accel * (timeLA ** 2)
        energyLA = self.vtolMotorTableInterface.getPowerAtThrust(hoverForce / 4) * 4 * timeLA

        return timeLA, distLA, energyLA

    def calcVTOLLandingDeceleration(self):
        maxThrust = self.vtolMotorTableInterface.getMaxThrust() * 4
        accel = maxThrust / self.totalMass - G_ACCEL
        timeLD = self.ascentDecentSpeed / accel
        distLD = 0.5 * accel * (timeLD ** 2)
        energyLD = self.vtolMotorTableInterface.getMaxPower() * 4 * timeLD

        return timeLD, distLD, energyLD
    
    def calcLanding(self):
        timeLA, distLA, energyLA = self.calcVTOLLandingAcceleration()
        timeLD, distLD, energyLD = self.calcVTOLLandingDeceleration()

        dist = self.currentAltitude - self.mission.parameters["baseStationAltitude"] - distLA - distLD
        time = dist / self.ascentDecentSpeed
        hoverForce = self.totalMass * G_ACCEL
        energy = time * self.vtolMotorTableInterface.getPowerAtThrust(hoverForce / 4) * 4

        totalTime = timeLA + time + timeLD
        totalDist = distLA + dist + distLD
        totalEnergy = energyLA + energy + energyLD

        self.currentAltitude -= totalDist

        return totalTime, totalDist, totalEnergy
    
    def calcCruisePeriod(self):
        timeInPeriods = 0
        distInPeriods = 0
        energyInPeriods = 0

        for leg in self.mission.legs:
            if leg == MissionLeg.CRUISE:
                continue
            
            time, dist, energy = eval( "self." + leg.string + "()" )

            timeInPeriods += time
            distInPeriods += dist
            energyInPeriods += energy

        cruisePower = self.cruiseMotorTableInterface.getPowerAtThrust( self.calcCruiseThrust() )
        timeC = ( self.batteryEnergy - energyInPeriods - self.auxPowerCon * timeInPeriods ) / ( cruisePower + self.auxPowerCon )
        distC = timeC * self.calcCruiseSpeed()

        return timeC, distC

    def calcMaxRange(self):
        timeA, distA, energyA = self.calcAccelerationPeriod()
        timeC, distC = self.calcCruisePeriod()

        return distC + distA
    
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
