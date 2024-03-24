from .AtmosphereConditions import AtmosphereConditions
from .DragLiftCoefficientInterface import DragLiftCoefficientInterface
from .MotorTableInterface import MotorTableInterface
from .Mission import *
from .ResultsWriter import ResultsWriter
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
                 batteryWeight, batteryCapacity, batteryVoltage,
                 cruiseMotorTablePath, vtolMotorTablePath,
                 auxPowerCon,
                 vtolSpeed,
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
        self.propellorDiameter = 0.4572

        self.angleOfAttack = angleOfAttack

        self.batteryWeight = batteryWeight
        self.batteryCapacity = batteryCapacity
        self.batteryVoltage = batteryVoltage
        self.batteryEnergy = batteryVoltage * batteryCapacity * 3.6 * 0.94

        self.mission = mission

        self.cruiseAltitude = mission.parameters["cruiseAltitude"]
        self.cruiseAltitude2 = mission.parameters["cruiseAltitude2"]
        self.currentAltitude = mission.parameters["baseStationAltitude"]
        self.baseAltitude = mission.parameters["baseStationAltitude"]
        self.vtolSpeed = vtolSpeed

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
        self.dragLiftInterface = DragLiftCoefficientInterface(f"./ModelLayer/data/airfoils/xf-naca{self.airFoil}-il-{self.adjustReynoldsNumberToValue(self.reynoldsNum)}_Subset_1.csv")
        self.cruiseMotorTableInterface = MotorTableInterface(cruiseMotorTablePath, self.pressure, self.temperature)
        self.vtolMotorTableInterface = MotorTableInterface(vtolMotorTablePath, self.pressure, self.temperature)
        
        self.resultsWriter = ResultsWriter(self.mission, self.batteryEnergy)

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
        maxLiftCoefficient = 0.9 * 1.7 #TODO: Change this
        wingloading = self.totalWeight / self.wingArea 
        
        print("Air Density: ", airDensity)
        print("CL,MAX ", maxLiftCoefficient)
        print("Wing Loading ", wingloading)

        vStallSquared = 2 * wingloading / ( airDensity * maxLiftCoefficient )
        return math.sqrt(vStallSquared)
    
    # def calcMaxSpeed(self):
    #     # thrust = self.cruiseMotorTableInterface.getMaxThrust()
    #     thrust = 5.66138 # TODO: REMOVE THIS, TESTING PURPOSES ONLY 
    #     airDensity = self.atmConditions.calcAirDensity(self.pressure, self.temperature)
    #     coefficientK = self.calcDragDueToLiftFactor()
    #     thrustAreaRatio = thrust / self.wingArea
    #     thrustWeightRatio = thrust / self.totalWeight
    #     wingLoading = self.totalWeight / self.wingArea

    #     print("Thrust: ", thrust)
    #     print("Air Density: ", airDensity)
    #     print("DragDueToLiftFactor: ", coefficientK)
    #     print("Thrust / Area: ", thrustAreaRatio)
    #     print("Thrust / Weight: ", thrustWeightRatio)
    #     print("Wing Loading: ", wingLoading)

    #     vMaxSquared = (thrustAreaRatio + wingLoading * math.sqrt( ( thrustWeightRatio ** 2 ) - 4 * self.calcZeroLiftDragCoefficient() * coefficientK ) ) / ( airDensity * self.calcZeroLiftDragCoefficient() )
    #     print("Max Speed: ", math.sqrt(vMaxSquared))

    #     return math.sqrt(vMaxSquared)
    
    def calcMaxSpeed(self):
        CD0 = self.calcZeroLiftDragCoefficient()
        coefficientK = self.calcDragDueToLiftFactor()
        airDensity = self.atmConditions.calcAirDensity(self.pressure, self.temperature)
        powerAvailable = math.sqrt( ( self.cruiseMotorTableInterface.getMaxThrust() ** 3 ) / ( math.pi / 2 * airDensity * ( self.propellorDiameter ** 2 ) ) )
        
        powerMax = 0
        speeds = []
        speedStep = 0.01
        speed = 1
        while speed < 1000:
            powerMax = 0.5 * airDensity * ( speed ** 3 ) * self.wingArea * CD0 + ( 2 * coefficientK * self.wingArea ) / (airDensity * speed) * ( (self.totalWeight / self.wingArea) ** 2 )

            if abs(powerMax - powerAvailable) / powerAvailable < 0.001:
                speeds.append(speed)
            
            speed += speedStep
        
        return max(speeds)
    
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

        print("skinFrictionCoefficient ", skinFrictionCoefficient)
        print("Wetted Area ", self.calcWettedArea())
        print("Reference Area ", self.calcReferenceArea())

        wettedAndReferenceAreaRatio = self.calcWettedArea() / self.calcReferenceArea()

        print("CD0 ", wettedAndReferenceAreaRatio * skinFrictionCoefficient)
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

        ROCMax = self.cruiseMotorTableInterface.getMechanicalPowerAtThrust( self.cruiseMotorTableInterface.getMaxThrust() ) / self.totalMass \
               - velocityROCMax * 1.155 / ( self.calcMaxLiftDragRatio() )

        return ROCMax, velocityROCMax
    
    def calcRateOfDescent(self):
        vThetaMin = math.sqrt( 2 / self.atmConditions.calcAirDensity( self.pressure, self.temperature ) \
                          * math.sqrt( self.liftDistribution / self.calcZeroLiftDragCoefficient() ) \
                          * ( self.totalWeight / self.wingArea ) )
        thetaMin = math.atan( 1 / self.calcMaxLiftDragRatio() )

        return vThetaMin *  math.sin(thetaMin), vThetaMin
    
    def calcFixedWingClimb(self, targetAltitude = None, currentAltitude = None):
        if targetAltitude == None:
            targetAltitude = self.cruiseAltitude
        if currentAltitude == None:
            currentAltitude = self.currentAltitude

        rateOfClimb, speed = self.calcRateOfClimb()
        
        distFWC = targetAltitude - currentAltitude # vertical height
        timeFWC = distFWC / rateOfClimb
        energyFWC = self.cruiseMotorTableInterface.getMaxPower() * timeFWC

        # converting distFWC to a horizontal component
        horizontalSpeed = math.sqrt( speed ** 2 - rateOfClimb ** 2 )
        distFWC = horizontalSpeed * timeFWC

        self.currentAltitude = targetAltitude

        return timeFWC, distFWC, energyFWC
    
    def calcFixedWingDescent(self, targetAltitude = None, currentAltitude = None):
        if targetAltitude == None:
            targetAltitude = self.mission.parameters["vtolDescent"]
        if currentAltitude == None:
            currentAltitude = self.currentAltitude
        
        distFWD = currentAltitude - targetAltitude # vertical height
        ROD, _ = self.calcRateOfDescent()
        timeFWD = distFWD / ROD # time based on vertical speed
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
        timeTA = self.vtolSpeed / takeOffAccel
        distTA = 0.5 * takeOffAccel * (timeTA ** 2)
        energyTA = self.vtolMotorTableInterface.getMaxPower() * 4 * timeTA
        return timeTA, distTA, energyTA
    
    def calcVTOLTakeOffDeceleration(self):
        # Deceleration Stage Time
        hoverForce = self.totalMass * G_ACCEL * UNDER_HOVER_FORCE
        accel = hoverForce / self.totalMass
        timeTD = self.vtolSpeed / accel
        distTD = self.vtolSpeed * timeTD + 0.5 * accel * (timeTD ** 2)
        energyTD = self.vtolMotorTableInterface.getPowerAtThrust(hoverForce / 4) * timeTD * 4

        return timeTD, distTD, energyTD
    
    def calcTakeOff(self):
        timeTA, distTA, energyTA = self.calcVTOLTakeOffAcceleration()
        timeTD, distTD, energyTD = self.calcVTOLTakeOffDeceleration()

        if self.mission.profile == MissionProfile.VTOL_STRAIGHT or self.mission.profile == MissionProfile.DOUBLE_CRUISE:
            dist = self.cruiseAltitude - self.mission.parameters["baseStationAltitude"] - distTA - distTD
        else:
            dist = self.mission.parameters["vtolClimb"] - self.mission.parameters["baseStationAltitude"] - distTA - distTD
        
        time = dist / self.vtolSpeed

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
        # cruiseThrust = self.calcCruiseThrust()
        cruiseThrust = 5.66138 # TODO: REMOVE THIS, TESTING PURPOSES ONLY 
        cruiseAccel = cruiseThrust / self.totalMass
        timeA = (cruiseSpeed / cruiseAccel) * math.atanh( 0.99 )
        # distA = ( cruiseSpeed ** 2 [squared makes it really large] ) * math.log( math.cosh( timeA * cruiseAccel / cruiseSpeed ) ) / ( cruiseThrust / self.totalMass )
        distA = cruiseSpeed * math.log( math.cosh( timeA * cruiseAccel / cruiseSpeed ) ) / ( cruiseThrust / self.totalMass )
        energyA = timeA * self.cruiseMotorTableInterface.getPowerAtThrust( cruiseThrust )

        return timeA, distA, energyA
    
    def calcVTOLLandingAcceleration(self):
        hoverForce = self.totalMass * G_ACCEL * UNDER_HOVER_FORCE
        accel = abs( hoverForce / self.totalMass - G_ACCEL )
        timeLA = self.vtolSpeed / accel
        distLA = self.vtolSpeed * timeLA + 0.5 * accel * (timeLA ** 2)
        energyLA = self.vtolMotorTableInterface.getPowerAtThrust(hoverForce / 4) * 4 * timeLA

        return timeLA, distLA, energyLA

    def calcVTOLLandingDeceleration(self):
        maxThrust = self.vtolMotorTableInterface.getMaxThrust() * 4
        accel = maxThrust / self.totalMass - G_ACCEL
        timeLD = self.vtolSpeed / accel
        distLD = 0.5 * accel * (timeLD ** 2)
        energyLD = self.vtolMotorTableInterface.getMaxPower() * 4 * timeLD

        return timeLD, distLD, energyLD
    
    def calcLanding(self):
        timeLA, distLA, energyLA = self.calcVTOLLandingAcceleration()
        timeLD, distLD, energyLD = self.calcVTOLLandingDeceleration()

        dist = self.currentAltitude - self.mission.parameters["baseStationAltitude"] - distLA - distLD
        time = dist / self.vtolSpeed
        hoverForce = self.totalMass * G_ACCEL
        energy = time * self.vtolMotorTableInterface.getPowerAtThrust(hoverForce / 4) * 4

        totalTime = timeLA + time + timeLD
        totalDist = distLA + dist + distLD
        totalEnergy = energyLA + energy + energyLD

        print(energyLA, energy, energyLD)
        print(distLA, dist, distLD)

        self.currentAltitude -= totalDist

        return totalTime, totalDist, totalEnergy
    
    # def calcCruisePeriod(self):
    #     timeT, distT, energyT = self.calcTakeOff()
    #     timeAT, energyAT = self.calcAccelerationTransitionPeriod()
    #     timeA, distA, energyA = self.calcAccelerationPeriod()
    #     timeL, distL, energyL = self.calcLanding()

    #     cruisePower = self.cruiseMotorTableInterface.getPowerAtThrust(self.calcCruiseThrust())
    #     timeC = ( self.batteryEnergy - energyT - energyAT - energyA - energyL - self.auxPowerCon * (timeT + timeA + timeL) ) / (cruisePower + self.auxPowerCon)
    #     distC = timeC * self.calcCruiseSpeed()

    #     return timeC, distC
    
    def calcCruisePeriod(self):
        timeInPeriods = 0
        distInPeriods = 0
        energyInPeriods = 0
        horizontalDistance = 0

        cruisePeriods = []

        for count, leg in enumerate( self.mission.legs ):
            self.resultsWriter.legInfos.append({})
            self.resultsWriter.legInfos[count]["mass"] = self.totalMass
            self.resultsWriter.legInfos[count]["legObject"] = leg

            if leg == MissionLeg.CRUISE:
                cruisePeriods.append( count )
                continue
            
            self.resultsWriter.legInfos[count]["altitudeStart"] = self.currentAltitude
            
            if self.mission.profile == MissionProfile.DOUBLE_CRUISE and leg == MissionLeg.ASCENT:
                time, dist, energy = eval( "self." + leg.string + f"(targetAltitude={self.cruiseAltitude2})" )
            else:
                time, dist, energy = eval( "self." + leg.string + "()" )

            self.resultsWriter.legInfos[count]["timeStart"] = timeInPeriods
            self.resultsWriter.legInfos[count]["timeEnd"] = timeInPeriods + time
            self.resultsWriter.legInfos[count]["distanceTravelled"] = dist
            self.resultsWriter.legInfos[count]["energyExpended"] = energy
            self.resultsWriter.legInfos[count]["altitudeEnd"] = self.currentAltitude
            

            if leg == MissionLeg.VTOL_TAKEOFF:
                timeA, distA, energyA = self.calcVTOLTakeOffAcceleration()
                timeD, distD, energyD = self.calcVTOLTakeOffDeceleration()

                self.resultsWriter.legInfos[count]["timeAccelerating"] = timeA
                self.resultsWriter.legInfos[count]["distanceAccelerating"] = distA
                self.resultsWriter.legInfos[count]["energyAccelerating"] = energyA

                self.resultsWriter.legInfos[count]["timeDecelerating"] = timeD
                self.resultsWriter.legInfos[count]["distanceDecelerating"] = distD
                self.resultsWriter.legInfos[count]["energyDecelerating"] = energyD

                self.resultsWriter.legInfos[count]["thrust"] = self.vtolMotorTableInterface.getMaxThrust() * 4
                self.resultsWriter.legInfos[count]["thrustPower"] = self.vtolMotorTableInterface.getMaxPower() * 4
                self.resultsWriter.legInfos[count]["targetSpeed"] = self.vtolSpeed

                self.resultsWriter.legInfos[count]["baseAltitude"] = self.baseAltitude
                self.resultsWriter.legInfos[count]["temperature"] = self.temperature
            elif leg == MissionLeg.VTOL_LANDING:
                timeA, distA, energyA = self.calcVTOLLandingAcceleration()
                timeD, distD, energyD = self.calcVTOLLandingDeceleration()

                # print("HERE!!!!")
                # print(time, dist, energy)
                # print(timeA, distA, energyA)
                # print(timeD, distD, energyD)
                
                self.resultsWriter.legInfos[count]["timeAccelerating"] = timeA
                self.resultsWriter.legInfos[count]["distanceAccelerating"] = distA
                self.resultsWriter.legInfos[count]["energyAccelerating"] = energyA

                self.resultsWriter.legInfos[count]["timeDecelerating"] = timeD
                self.resultsWriter.legInfos[count]["distanceDecelerating"] = distD
                self.resultsWriter.legInfos[count]["energyDecelerating"] = energyD

                self.resultsWriter.legInfos[count]["thrust"] = self.vtolMotorTableInterface.getMaxThrust() * 4
                self.resultsWriter.legInfos[count]["targetSpeed"] = self.vtolSpeed

                self.resultsWriter.legInfos[count]["baseAltitude"] = self.baseAltitude
                self.resultsWriter.legInfos[count]["temperature"] = self.temperature
            elif leg == MissionLeg.TRANSITION:
                self.resultsWriter.legInfos[count]["timeAccelerating"] = time
                self.resultsWriter.legInfos[count]["distanceAccelerating"] = dist
                self.resultsWriter.legInfos[count]["energyAccelerating"] = energy

                self.resultsWriter.legInfos[count]["targetSpeed"] = self.calcStallSpeed()
                self.resultsWriter.legInfos[count]["thrust"] = self.calcCruiseThrust()
                self.resultsWriter.legInfos[count]["thrustPower"] = self.cruiseMotorTableInterface.getPowerAtThrust( self.calcCruiseThrust() )
                self.resultsWriter.legInfos[count]["propellorPower"] = self.calcPropellorPower()
            elif leg == MissionLeg.ACCELERATION:
                self.resultsWriter.legInfos[count]["timeAccelerating"] = time
                self.resultsWriter.legInfos[count]["distanceAccelerating"] = dist
                self.resultsWriter.legInfos[count]["energyAccelerating"] = energy

                self.resultsWriter.legInfos[count]["targetSpeed"] = self.calcCruiseSpeed()
                self.resultsWriter.legInfos[count]["thrust"] = self.calcCruiseThrust()
                self.resultsWriter.legInfos[count]["thrustPower"] = self.cruiseMotorTableInterface.getPowerAtThrust( self.calcCruiseThrust() )
                self.resultsWriter.legInfos[count]["propellorPower"] = self.calcPropellorPower()
            elif leg == MissionLeg.ASCENT:
                self.resultsWriter.legInfos[count]["timeAccelerating"] = time
                self.resultsWriter.legInfos[count]["thrust"] = self.calcCruiseThrust()
                self.resultsWriter.legInfos[count]["targetSpeed"] = self.calcCruiseSpeed()
                self.resultsWriter.legInfos[count]["thrustPower"] = self.cruiseMotorTableInterface.getPowerAtThrust( self.calcCruiseThrust() )
                self.resultsWriter.legInfos[count]["propellorPower"] = self.calcPropellorPower()
                self.resultsWriter.legInfos[count]["ROC"], self.resultsWriter.legInfos[count]["compositeROC"] = self.calcRateOfClimb()
            elif leg == MissionLeg.ASCENT:
                self.resultsWriter.legInfos[count]["ROD"], self.resultsWriter.legInfos[count]["compositeROD"] = self.calcRateOfDescent()
            timeInPeriods += time
            distInPeriods += dist
            energyInPeriods += energy

            if leg != MissionLeg.VTOL_LANDING and leg != MissionLeg.VTOL_TAKEOFF:
                horizontalDistance += dist

        distC = self.mission.parameters["missionDistance"] - horizontalDistance
        cruisePower = self.cruiseMotorTableInterface.getPowerAtThrust( self.calcCruiseThrust() ) + self.auxPowerCon
        timeC = distC / self.calcCruiseSpeed()
        energyC = cruisePower * timeC

        print("cruise")
        print(timeC, distC, energyC)

        for count, cruisePeriod in enumerate( cruisePeriods ):
            self.resultsWriter.legInfos[cruisePeriod]["timeStart"] = self.resultsWriter.legInfos[cruisePeriod - 1]["timeEnd"]
            self.resultsWriter.legInfos[cruisePeriod]["timeEnd"] = self.resultsWriter.legInfos[cruisePeriod - 1]["timeEnd"] + timeC / len( cruisePeriods )
            self.resultsWriter.legInfos[cruisePeriod]["distanceTravelled"] = distC / len( cruisePeriods )
            self.resultsWriter.legInfos[cruisePeriod]["energyExpended"] = energyC / len( cruisePeriods )
            self.resultsWriter.legInfos[cruisePeriod]["altitudeStart"] = self.cruiseAltitude if count == 0 else self.cruiseAltitude2
            self.resultsWriter.legInfos[cruisePeriod]["altitudeEnd"] = self.cruiseAltitude if count == 0 else self.cruiseAltitude2

        return timeC, distC, energyC

    def calcMaxRange(self):
        timeC, distC, energyC = self.calcCruisePeriod()

        if MissionLeg.ACCELERATION in self.mission.legs:
            timeA, distA, energyA = self.calcAccelerationPeriod()
            distA *= self.mission.legs.count( MissionLeg.ACCELERATION )
            return distC + distA
        else:
            return distC
    
    def calcCruiseSpeed(self):
        if self.mission.performance == MissionPerformance.PERFORMANCE:
            return self.calcMaxSpeed()
        elif self.mission.performance == MissionPerformance.EFFICIENT:
            return self.calcEfficientSpeed()
    
    def calcCruiseThrust(self):
        if self.mission.performance == MissionPerformance.PERFORMANCE:
            return self.cruiseMotorTableInterface.getMaxThrust()
        elif self.mission.performance == MissionPerformance.EFFICIENT:
            return self.calcEfficientStaticThrust()
    
    def calcEfficientSpeed(self):
        airDensity = self.atmConditions.calcAirDensity(self.pressure, self.temperature)
        thrustWeightRatio = self.calcEfficientDynamicThrust() / self.totalWeight
        wingLoading = self.totalWeight / self.wingArea

        return math.sqrt(thrustWeightRatio * wingLoading / (airDensity * self.calcZeroLiftDragCoefficient()))

    def calcEfficientStaticThrust(self):
        propellorPower = self.calcEfficientSpeed() * self.calcEfficientDynamicThrust()
        thrust = ( math.pi / 2 * self.atmConditions.calcAirDensity(self.pressure, self.temperature) * self.propellorDiameter * propellorPower ) ** ( 1 / 3 )
        
        if thrust > self.cruiseMotorTableInterface.getMaxThrust():
            pass # throw an error!
        
        return thrust
    
    def calcEfficientDynamicThrust(self):
        coefficientK = self.calcDragDueToLiftFactor()
        thrustWeightRatio = math.sqrt(4 * self.calcZeroLiftDragCoefficient() * coefficientK)
        thrust = thrustWeightRatio * self.totalWeight

        return thrust
    
    def calcPropellorPower(self):
        if self.mission.performance == MissionPerformance.PERFORMANCE:
            CD0 = self.calcZeroLiftDragCoefficient()
            coefficientK = self.calcDragDueToLiftFactor()
            airDensity = self.atmConditions.calcAirDensity(self.pressure, self.temperature)
            return 0.5 * airDensity * ( self.calcMaxSpeed() ** 3 ) * self.wingArea * CD0 + ( 2 * coefficientK * self.wingArea ) / (airDensity * self.calcMaxSpeed()) * ( (self.totalWeight / self.wingArea) ** 2 )
        elif self.mission.performance == MissionPerformance.EFFICIENT:
            return self.calcEfficientDynamicThrust() * self.calcEfficientSpeed()
        
    def calcOswaldEfficicency(self):
        aspectRatio = self.calcAspectRatio()

        print("Oswald Efficicency ", 1.78 * (1 - 0.045 * (aspectRatio ** 0.68)) - 0.64)
        return 1.78 * (1 - 0.045 * (aspectRatio ** 0.68)) - 0.64
    
    def calcDragDueToLiftFactor(self):
        aspectRatio = self.calcAspectRatio()
        return 1 / (math.pi * aspectRatio * self.calcOswaldEfficicency())
    
    def calcAspectRatio(self):
        return (self.wingSpan ** 2) / self.wingArea
