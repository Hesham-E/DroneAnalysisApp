import csv
import math

from .Mission import *
from .AtmosphereConditions import *
from inspect import currentframe, getframeinfo

class ResultsWriter:
    def __init__(self, mission, batteryEnergy,
                 wingSpan, wingArea, totalMass,
                 batteryCapacity, maxSpeed, stallSpeed,
                 efficientSpeed):
        self.legInfos = [] # array of dictionaries, in order in mission 
        self.rows = [] # processed data from legInfos to be written
        self.timeStep = 0.1 # seconds
        self.headers = ["Time (s)", "Altitude (m)", "Distance Travelled (m)", 
                        "Current Horizontal Speed (m/s)", "Current Vertical Speed (m/s)", "State of Charge (%)", 
                        "Phase of Flight", "Phase of Flight (Integer)",
                        "Wing Span (m)", "Wing Area (m^2)", "Drone Weight (kg)",
                        "Battery Capacity (mAh)", "Maximum Speed (m/s)", "Stall Speed (m/s)",
                        "Minimum Cruise Thrust Speed (m/s)"]

        self.mission = mission
        # self.batteryCapactiy = batteryCapacity
        # self.batteryVoltage = batteryVoltage
        self.batteryEnergy = batteryEnergy
        self.atmConditions = AtmosphereConditions()

        self.cruiseDistance = None
        self.unpoweredDecel = 1.8

        self.wingSpan = wingSpan
        self.wingArea = wingArea
        self.totalMass = totalMass
        self.batteryCapacity = batteryCapacity
        self.maxSpeed = maxSpeed
        self.stallSpeed = stallSpeed
        self.efficientSpeed = efficientSpeed
    
    def quadradicCurve(self, x):
        return -2 * x ** 2
    
    def createRows(self):
        self.rows = [] # reset in case we are doing 2 runs

        currTime = 0
        currDistance = 0
        horizontalDistance = 0
        currAltitude = self.legInfos[0]["altitudeStart"]
        currSOC = 100
        currEnergy = self.batteryEnergy
        currVerticalSpeed = 0
        currHorizontalSpeed = 0
        numOfCruisePeriods = self.mission.legs.count(MissionLeg.CRUISE)

        def calcDrag(speed):
            airDensity = self.atmConditions.calcAirDensityAtAltitude(currAltitude, self.mission.parameters["temperature"])
            dragDueToLiftCoefficient = leg["dragDueToLiftFactor"]
        
            # print(airDensity)
            # print(dragDueToLiftCoefficient)
            # print(speed)
            # print(leg["wingArea"])
            # print(leg["CD0"])
            # print(leg["weight"])
            # print()
            return 0.5 * airDensity * ( speed ** 2 ) * leg["wingArea"] * leg["CD0"] + 2 * dragDueToLiftCoefficient * leg["wingArea"] / ( airDensity * ( speed ** 2 ) ) * ( ( leg["mass"] /leg["wingArea"] ) ** 2 )

        print(currEnergy)
        print(self.legInfos)

        for count, leg in enumerate( self.legInfos ):
            totalTime = leg["timeEnd"] - leg["timeStart"]
            totalDistance = leg['distanceTravelled']
            totalEnergy = leg["energyExpended"]
            print(f"Leg: {leg['legObject'].realName}")
            print(f"Total Distance: {totalDistance}")
            print(f"Total Time: {totalTime}")
            print(f"Altitude Start: {leg['altitudeStart']}")
            print(f"Altitude End: {leg['altitudeEnd']}")
            
            
            if "timeAccelerating" in leg.keys(): # non-linear rate of change
                if "timeDecelerating" in leg.keys(): # only the VTOL modes do this
                    currHorizontalSpeed = 0

                    # acceleration period
                    timeA = leg["timeAccelerating"]
                    distA = leg["distanceAccelerating"]
                    energyA = leg["energyAccelerating"]
                    
                    accelerationOld = 2 * distA / (timeA ** 2)
                    acceleration = leg["thrust"] / leg["mass"]
                    accelDirection = -1 if leg["altitudeEnd"] - leg["altitudeStart"] < 0 else 1

                    print("Time: ", timeA)
                    print("Distance: ", distA)
                    print("Energy: ", energyA)
                    print("AccelerationOld: ", accelerationOld)
                    print("Acceleration: ", acceleration)
                    print("AccelDirection: ", accelDirection)
                    print("Time Step: ", self.timeStep)
                    print("Mass: ", leg["mass"])
                    print("VTOL Speed: ", leg["targetSpeed"])
                    print()

                    periodTime = 0
                    periodDistance = 0

                    originalAccel = acceleration
                    while currVerticalSpeed < leg["targetSpeed"]:
                        self.rows.append( [f"{currTime:.2f}", f"{currAltitude:.2f}", f"{horizontalDistance:.2f}", f"{currHorizontalSpeed:.2f}", f"{currVerticalSpeed:.2f}", f"{currSOC:.2f}", f"{leg['legObject'].realName}", f"{leg['legObject'].value}", f"{self.wingSpan:.2f}", f"{self.wingArea:.2f}", f"{self.totalMass:.2f}", f"{self.batteryCapacity:.2f}", f"{self.maxSpeed:.2f}", f"{self.stallSpeed:.2f}", f"{self.efficientSpeed:.2f}"] )

                        currTime += self.timeStep
                        periodTime += self.timeStep
                        currVerticalSpeed += acceleration * self.timeStep

                        if currVerticalSpeed < leg["targetSpeed"]:
                            # print(periodDistance)
                            prevPeriodDistance = periodDistance
                            periodDistance = periodDistance / periodTime * self.timeStep + 0.5 * acceleration * ( periodTime ** 2 )
                            currDistance += abs( prevPeriodDistance - periodDistance )
                            
                            currEnergy -= leg["vtolThrustPowerA"] * self.timeStep
                            currEnergy -= leg["auxPower"] * self.timeStep
                            currSOC = currEnergy / self.batteryEnergy * 100

                            if "timeDecelerating" in leg.keys(): #VTOL Take Off or Landing since only they have deceleration, therefore, altitude changes too
                                currAltitude += abs( prevPeriodDistance - periodDistance ) * accelDirection
                            if currVerticalSpeed > 1: # because the calcDrag is dumb with small values
                                acceleration = originalAccel - ( calcDrag(currVerticalSpeed) / leg["mass"] )
                    
                    currVerticalSpeed = leg["targetSpeed"] # Correct overshoot based on timeStep chosen
                    accelDistance = periodDistance

                    print("Done VTOL Accel")
                    # self.rows.append(["Done VTOL Accel"])
                    # break

                    # calculate deceleration distance, we do this first in order to know how long the linear period is
                    acceleration = 9.80665 * 0.5 # half of the acceleration needed to hover
                    decelDistance = leg["targetSpeed"] / acceleration

                    # linear period
                    distL = abs( leg["altitudeEnd"] - leg["altitudeStart"] ) - accelDistance - decelDistance
                    timeL = distL / leg["targetSpeed"]
                    energyL = totalEnergy - energyA - leg["energyDecelerating"]
                    steps = timeL / self.timeStep

                    distanceStep = distL / steps
                    altitudeStep = distanceStep * accelDirection #Try to calculate this somehow to make the program more dynamic. Works currently given all our use cases though
                    energyStep = energyL / steps

                    print("Steps: ", steps)
                    print("Time: ", timeL)
                    print("Distance: ", distL)
                    print("Energy: ", energyL)
                    print("Time Step: ", self.timeStep)
                    print("Distance Step: ", distanceStep)
                    print("Altitude Step: ", altitudeStep)
                    print("Energy Step: ", energyStep)
                    print()

                    periodTime = 0
                    while periodTime < timeL:
                        self.rows.append( [f"{currTime:.2f}", f"{currAltitude:.2f}", f"{horizontalDistance:.2f}", f"{currHorizontalSpeed:.2f}", f"{currVerticalSpeed:.2f}", f"{currSOC:.2f}", f"{leg['legObject'].realName}", f"{leg['legObject'].value}", f"{self.wingSpan:.2f}", f"{self.wingArea:.2f}", f"{self.totalMass:.2f}", f"{self.batteryCapacity:.2f}", f"{self.maxSpeed:.2f}", f"{self.stallSpeed:.2f}", f"{self.efficientSpeed:.2f}"] )

                        currTime += self.timeStep
                        periodTime += self.timeStep

                        if periodTime < timeL:
                            currDistance += distanceStep
                            currAltitude += altitudeStep
                            currEnergy -= energyStep
                            currSOC = currEnergy / self.batteryEnergy * 100
                    
                    print("Done VTOL Linear")
                    # self.rows.append(["Done VTOL Linear"])

                    # deceleration period, yes we do this first in order to know how long the linear period is
                    timeD = leg["timeDecelerating"]
                    distD = leg["distanceDecelerating"]
                    energyD = leg["energyDecelerating"]
                    
                    accelerationOld = 2 * distA / (timeA ** 2)
                    acceleration = 9.80665 * 0.5 # half of the acceleration needed to hover
                    accelDirection = -1 if leg["altitudeEnd"] - leg["altitudeStart"] < 0 else 1

                    print("Time: ", timeD)
                    print("Distance: ", distD)
                    print("Energy: ", energyD)
                    print("AccelerationOld: ", accelerationOld)
                    print("Acceleration: ", acceleration)
                    print("AccelDirection: ", accelDirection)
                    print("Time Step: ", self.timeStep)
                    print("Mass: ", leg["mass"])
                    print()

                    periodTime = 0
                    periodDistance = 0
                    while currVerticalSpeed > 0:
                        self.rows.append( [f"{currTime:.2f}", f"{currAltitude:.2f}", f"{horizontalDistance:.2f}", f"{currHorizontalSpeed:.2f}", f"{currVerticalSpeed:.2f}", f"{currSOC:.2f}", f"{leg['legObject'].realName}", f"{leg['legObject'].value}", f"{self.wingSpan:.2f}", f"{self.wingArea:.2f}", f"{self.totalMass:.2f}", f"{self.batteryCapacity:.2f}", f"{self.maxSpeed:.2f}", f"{self.stallSpeed:.2f}", f"{self.efficientSpeed:.2f}"] )

                        currTime += self.timeStep
                        periodTime += self.timeStep
                        currVerticalSpeed -= acceleration * self.timeStep

                        if currVerticalSpeed > 0:
                            # print(periodDistance)
                            prevPeriodDistance = periodDistance
                            periodDistance = periodDistance / periodTime * self.timeStep + 0.5 * acceleration * ( periodTime ** 2 )
                            currDistance += abs( prevPeriodDistance - periodDistance )
                            
                            currEnergy -= leg["vtolThrustPowerD"] * self.timeStep
                            currEnergy -= leg["auxPower"] * self.timeStep
                            currSOC = currEnergy / self.batteryEnergy * 100

                            if "timeDecelerating" in leg.keys(): #VTOL Take Off or Landing since only they have deceleration, therefore, altitude changes too
                                currAltitude += abs( prevPeriodDistance - periodDistance ) * accelDirection
                                

                    decelDistance = periodDistance
                    currVerticalSpeed = 0 # Correct overshoot based on timeStep chosen
                else: # We are in Transition or Fixed Wing Acceleration or Fixed Wing Ascent
                    
                    
                    print(getframeinfo(currentframe()).lineno)
                    acceleration = leg["thrust"] / leg["mass"]

                    if leg["legObject"] == MissionLeg.ASCENT:
                        compositeSpeed = math.sqrt( currHorizontalSpeed ** 2 + currVerticalSpeed ** 2 )
                        climbAngle = math.asin( leg["ROC"] / leg["compositeROC"] )
                        horizontalAcceleration = acceleration * math.cos( climbAngle )
                        verticalAcceleration = acceleration * math.sin( climbAngle )

                        print(getframeinfo(currentframe()).lineno)
                        print(compositeSpeed, currHorizontalSpeed, currVerticalSpeed)
                        print(leg["compositeROC"], leg["ROC"])
                        print(currAltitude)
                        print(leg["altitudeEnd"])
                        if compositeSpeed < leg["compositeROC"]:
                            while compositeSpeed < leg["compositeROC"] and currAltitude < leg["altitudeEnd"]:
                                # acceleration phase
                                self.rows.append( [f"{currTime:.2f}", f"{currAltitude:.2f}", f"{horizontalDistance:.2f}", f"{currHorizontalSpeed:.2f}", f"{currVerticalSpeed:.2f}", f"{currSOC:.2f}", f"{leg['legObject'].realName}", f"{leg['legObject'].value}", f"{self.wingSpan:.2f}", f"{self.wingArea:.2f}", f"{self.totalMass:.2f}", f"{self.batteryCapacity:.2f}", f"{self.maxSpeed:.2f}", f"{self.stallSpeed:.2f}", f"{self.efficientSpeed:.2f}"] )
                                totalDistance += compositeSpeed * self.timeStep + 0.5 * acceleration * ( self.timeStep ** 2 )
                                horizontalDistance += currHorizontalSpeed * self.timeStep + 0.5 * horizontalAcceleration * ( self.timeStep ** 2 )
                                currAltitude += currVerticalSpeed * self.timeStep + 0.5 * verticalAcceleration * ( self.timeStep ** 2 )
                                currDistance = totalDistance

                                
                                currHorizontalSpeed += horizontalAcceleration * self.timeStep
                                currVerticalSpeed += verticalAcceleration * self.timeStep
                                compositeSpeed = math.sqrt( currHorizontalSpeed ** 2 + currVerticalSpeed ** 2 )

                                currEnergy -= leg["thrustPower"] * self.timeStep
                                currEnergy -= leg["auxPower"] * self.timeStep
                                currSOC = currEnergy / self.batteryEnergy * 100

                                if leg["thrust"] > leg["propellorPower"] / compositeSpeed: #put this after so that compositeSpeed isn't 0
                                    acceleration = leg["propellorPower"] / compositeSpeed / leg["mass"]

                                    horizontalAcceleration = acceleration * math.cos( climbAngle )
                                    verticalAcceleration = acceleration * math.sin( climbAngle )
                                
                                print(leg["thrust"] / leg["mass"])
                                print(acceleration)
                                print(leg["propellorPower"] / compositeSpeed / leg["mass"])
                                print(leg["mass"])
                                print(leg["thrust"])
                                print(leg["propellorPower"])
                        else: #already at speed, just pitch up
                            currVerticalSpeed = leg["compositeROC"] * math.sin(climbAngle)
                            currHorizontalSpeed = leg["compositeROC"] * math.cos(climbAngle)


                        deceleration = 9.80665 * 0.5 # half of the acceleration needed to hover
                        decelDistance = currVerticalSpeed / deceleration # slow down since next leg will be 0 vertical speed
                        while currAltitude < leg["altitudeEnd"] - decelDistance:
                            # do not accelerate but hold speed until target altitude
                            self.rows.append( [f"{currTime:.2f}", f"{currAltitude:.2f}", f"{horizontalDistance:.2f}", f"{currHorizontalSpeed:.2f}", f"{currVerticalSpeed:.2f}", f"{currSOC:.2f}", f"{leg['legObject'].realName}", f"{leg['legObject'].value}", f"{self.wingSpan:.2f}", f"{self.wingArea:.2f}", f"{self.totalMass:.2f}", f"{self.batteryCapacity:.2f}", f"{self.maxSpeed:.2f}", f"{self.stallSpeed:.2f}", f"{self.efficientSpeed:.2f}"] )
                            totalDistance += compositeSpeed * self.timeStep
                            horizontalDistance += currHorizontalSpeed * self.timeStep
                            currAltitude += currVerticalSpeed * self.timeStep
                            currDistance = totalDistance
                            currEnergy -= leg["cruiseThrustPower"] * self.timeStep
                            currEnergy -= leg["auxPower"] * self.timeStep

                        while currVerticalSpeed > 0:
                            # decelerate
                            self.rows.append( [f"{currTime:.2f}", f"{currAltitude:.2f}", f"{horizontalDistance:.2f}", f"{currHorizontalSpeed:.2f}", f"{currVerticalSpeed:.2f}", f"{currSOC:.2f}", f"{leg['legObject'].realName}", f"{leg['legObject'].value}", f"{self.wingSpan:.2f}", f"{self.wingArea:.2f}", f"{self.totalMass:.2f}", f"{self.batteryCapacity:.2f}", f"{self.maxSpeed:.2f}", f"{self.stallSpeed:.2f}", f"{self.efficientSpeed:.2f}"] )
                            totalDistance += compositeSpeed * self.timeStep
                            horizontalDistance += currHorizontalSpeed * self.timeStep
                            currAltitude += currVerticalSpeed * self.timeStep
                            currDistance = totalDistance
                            currEnergy -= leg["auxPower"] * self.timeStep

                            currVerticalSpeed -= deceleration * self.timeStep
                        
                        currVerticalSpeed = 0 # fix overcorrection
                        
                        while currHorizontalSpeed < leg["targetSpeed"]: #accelerate to cruising speed
                            self.rows.append( [f"{currTime:.2f}", f"{currAltitude:.2f}", f"{horizontalDistance:.2f}", f"{currHorizontalSpeed:.2f}", f"{currVerticalSpeed:.2f}", f"{currSOC:.2f}", f"{leg['legObject'].realName}", f"{leg['legObject'].value}", f"{self.wingSpan:.2f}", f"{self.wingArea:.2f}", f"{self.totalMass:.2f}", f"{self.batteryCapacity:.2f}", f"{self.maxSpeed:.2f}", f"{self.stallSpeed:.2f}", f"{self.efficientSpeed:.2f}"] )
                            totalDistance += currHorizontalSpeed * self.timeStep + 0.5 * acceleration * ( self.timeStep ** 2 )
                            horizontalDistance += currHorizontalSpeed * self.timeStep + 0.5 * acceleration * ( self.timeStep ** 2 )
                            currDistance = totalDistance
                            currHorizontalSpeed += acceleration * self.timeStep
                            totalTime += self.timeStep
                            currEnergy -= leg["cruiseThrustPower"] * self.timeStep
                            currEnergy -= leg["auxPower"] * self.timeStep

                            if leg["thrust"] > leg["propellorPower"] / currHorizontalSpeed: #put this after so that currHorizontalSpeed isn't 0
                                acceleration = leg["propellorPower"] / currHorizontalSpeed / leg["mass"]

                    else:
                        originalAccel = acceleration
                        while currHorizontalSpeed < leg["targetSpeed"]:
                            self.rows.append( [f"{currTime:.2f}", f"{currAltitude:.2f}", f"{horizontalDistance:.2f}", f"{currHorizontalSpeed:.2f}", f"{currVerticalSpeed:.2f}", f"{currSOC:.2f}", f"{leg['legObject'].realName}", f"{leg['legObject'].value}", f"{self.wingSpan:.2f}", f"{self.wingArea:.2f}", f"{self.totalMass:.2f}", f"{self.batteryCapacity:.2f}", f"{self.maxSpeed:.2f}", f"{self.stallSpeed:.2f}", f"{self.efficientSpeed:.2f}"] )
                            totalDistance += currHorizontalSpeed * self.timeStep + 0.5 * acceleration * ( self.timeStep ** 2 )
                            horizontalDistance += currHorizontalSpeed * self.timeStep + 0.5 * acceleration * ( self.timeStep ** 2 )
                            currDistance = totalDistance
                            currHorizontalSpeed += acceleration * self.timeStep
                            totalTime += self.timeStep
                            currTime += self.timeStep

                            if leg["legObject"] == MissionLeg.TRANSITION:
                                currEnergy -= leg["vtolThrustPower"] * self.timeStep
                            currEnergy -= leg["cruiseThrustPower"] * self.timeStep
                            currEnergy -= leg["auxPower"] * self.timeStep
                            currSOC = currEnergy / self.batteryEnergy * 100

                            if leg["thrust"] > leg["propellorPower"] / currHorizontalSpeed: #put this after so that currHorizontalSpeed isn't 0
                                acceleration = leg["propellorPower"] / currHorizontalSpeed / leg["mass"]
                            
                            print("speed", currHorizontalSpeed)
                            if currHorizontalSpeed > 1: # because the calcDrag is dumb with small values
                                acceleration = originalAccel - ( calcDrag(currHorizontalSpeed) / leg["mass"] )
                            # print("HERE!")
                            # print(leg["thrust"] / leg["mass"])
                            # print(acceleration)
                            # print(leg["propellorPower"] / currHorizontalSpeed / leg["mass"])
                            # print(leg["mass"])
                            # print(leg["thrust"])
                            # print(leg["propellorPower"])
                            

            else: # linear rate of change, ie. no acceleration in this period
                if leg["legObject"] == MissionLeg.CRUISE:
                    if self.cruiseDistance == None and numOfCruisePeriods != 0:
                        continue # need to resolve cruise distance first
                    else:
                        currVerticalSpeed = 0
                        print("CRUISE")
                        print(self.cruiseDistance)
                        print(horizontalDistance)
                        print(numOfCruisePeriods)
                        print(currHorizontalSpeed)

                        periodDistance = 0


                        # speed = currHorizontalSpeed
                        # decelDistance = 0
                        # decelTimeStep = 14.73
                        # while speed > 0:
                        #     dragDecel = calcDrag(speed) / leg["mass"]
                        #     speed -= dragDecel * decelTimeStep
                        #     decelDistance += speed * decelTimeStep

                        if self.legInfos[count+1]["legObject"] == MissionLeg.VTOL_LANDING or \
                           self.legInfos[count+1]["legObject"] == MissionLeg.VTOL_TAKEOFF:
                            
                            # calculate decel distance
                            decelDistance = 0.5 * self.unpoweredDecel * ( currHorizontalSpeed / self.unpoweredDecel ) ** 2
                            
                            self.cruiseDistance -= decelDistance * numOfCruisePeriods
                            tempCruiseDistance = self.cruiseDistance / numOfCruisePeriods - decelDistance
                            print("DECEL DISTANCE: ", decelDistance)
                            while periodDistance < tempCruiseDistance:
                                self.rows.append( [f"{currTime:.2f}", f"{currAltitude:.2f}", f"{horizontalDistance:.2f}", f"{currHorizontalSpeed:.2f}", f"{currVerticalSpeed:.2f}", f"{currSOC:.2f}", f"{leg['legObject'].realName}", f"{leg['legObject'].value}", f"{self.wingSpan:.2f}", f"{self.wingArea:.2f}", f"{self.totalMass:.2f}", f"{self.batteryCapacity:.2f}", f"{self.maxSpeed:.2f}", f"{self.stallSpeed:.2f}", f"{self.efficientSpeed:.2f}"] )

                                currTime += self.timeStep
                                currDistance += currHorizontalSpeed * self.timeStep
                                horizontalDistance += currHorizontalSpeed * self.timeStep
                                periodDistance += currHorizontalSpeed * self.timeStep
                                currEnergy -= leg["cruiseThrustPower"] * self.timeStep
                                currEnergy -= leg["auxPower"] * self.timeStep
                                currSOC = currEnergy / self.batteryEnergy * 100

                            while currHorizontalSpeed > 0:
                                self.rows.append( [f"{currTime:.2f}", f"{currAltitude:.2f}", f"{horizontalDistance:.2f}", f"{currHorizontalSpeed:.2f}", f"{currVerticalSpeed:.2f}", f"{currSOC:.2f}", f"{leg['legObject'].realName}", f"{leg['legObject'].value}", f"{self.wingSpan:.2f}", f"{self.wingArea:.2f}", f"{self.totalMass:.2f}", f"{self.batteryCapacity:.2f}", f"{self.maxSpeed:.2f}", f"{self.stallSpeed:.2f}", f"{self.efficientSpeed:.2f}"] )

                                currHorizontalSpeed -= self.unpoweredDecel * self.timeStep

                                currTime += self.timeStep
                                currDistance += currHorizontalSpeed * self.timeStep
                                horizontalDistance += currHorizontalSpeed * self.timeStep
                                periodDistance += currHorizontalSpeed * self.timeStep
                                currEnergy -= leg["auxPower"] * self.timeStep
                                currSOC = currEnergy / self.batteryEnergy * 100
                        else: # true linear cruise period
                            while periodDistance < self.cruiseDistance / numOfCruisePeriods:
                                self.rows.append( [f"{currTime:.2f}", f"{currAltitude:.2f}", f"{horizontalDistance:.2f}", f"{currHorizontalSpeed:.2f}", f"{currVerticalSpeed:.2f}", f"{currSOC:.2f}", f"{leg['legObject'].realName}", f"{leg['legObject'].value}", f"{self.wingSpan:.2f}", f"{self.wingArea:.2f}", f"{self.totalMass:.2f}", f"{self.batteryCapacity:.2f}", f"{self.maxSpeed:.2f}", f"{self.stallSpeed:.2f}", f"{self.efficientSpeed:.2f}"] )

                                currTime += self.timeStep
                                currDistance += currHorizontalSpeed * self.timeStep
                                horizontalDistance += currHorizontalSpeed * self.timeStep
                                periodDistance += currHorizontalSpeed * self.timeStep
                                currEnergy -= leg["cruiseThrustPower"] * self.timeStep
                                currEnergy -= leg["auxPower"] * self.timeStep
                                currSOC = currEnergy / self.batteryEnergy * 100

                        print(horizontalDistance)
                elif leg["legObject"] == MissionLeg.DESCENT:
                    # calculate decel distance
                    decelDistance = 0.5 * self.unpoweredDecel * ( ( currHorizontalSpeed - leg["compositeROD"] ) / self.unpoweredDecel ) ** 2
                    while currHorizontalSpeed > leg["compositeROD"]:
                        self.rows.append( [f"{currTime:.2f}", f"{currAltitude:.2f}", f"{horizontalDistance:.2f}", f"{currHorizontalSpeed:.2f}", f"{currVerticalSpeed:.2f}", f"{currSOC:.2f}", f"{leg['legObject'].realName}", f"{leg['legObject'].value}", f"{self.wingSpan:.2f}", f"{self.wingArea:.2f}", f"{self.totalMass:.2f}", f"{self.batteryCapacity:.2f}", f"{self.maxSpeed:.2f}", f"{self.stallSpeed:.2f}", f"{self.efficientSpeed:.2f}"] )

                        currHorizontalSpeed -= self.unpoweredDecel * self.timeStep

                        currTime += self.timeStep
                        currDistance += currHorizontalSpeed * self.timeStep
                        horizontalDistance += currHorizontalSpeed * self.timeStep
                        periodDistance += currHorizontalSpeed * self.timeStep
                        currEnergy -= leg["auxPower"] * self.timeStep
                        currSOC = currEnergy / self.batteryEnergy * 100
                    
                    glideAngle = math.asin( leg["ROD"] / leg["compositeROD"] )
                    currHorizontalSpeed = leg["compositeROD"] * math.cos( glideAngle )
                    currVerticalSpeed = leg["ROD"]

                    totalTime = abs( leg["altitudeEnd"] - leg["altitudeStart"] ) / leg["ROD"]
                    steps = totalTime / self.timeStep

                    altitudeStep = ( leg["altitudeEnd"] - leg["altitudeStart"] ) / steps
                    distanceStep = currHorizontalSpeed * self.timeStep

                    while currAltitude > leg["altitudeEnd"]:
                        self.rows.append( [f"{currTime:.2f}", f"{currAltitude:.2f}", f"{horizontalDistance:.2f}", f"{currHorizontalSpeed:.2f}", f"{currVerticalSpeed:.2f}", f"{currSOC:.2f}", f"{leg['legObject'].realName}", f"{leg['legObject'].value}", f"{self.wingSpan:.2f}", f"{self.wingArea:.2f}", f"{self.totalMass:.2f}", f"{self.batteryCapacity:.2f}", f"{self.maxSpeed:.2f}", f"{self.stallSpeed:.2f}", f"{self.efficientSpeed:.2f}"] )

                        currTime += self.timeStep
                        horizontalDistance += distanceStep
                        currAltitude += altitudeStep
                        currEnergy -= leg["auxPower"] * self.timeStep
                        currSOC = currEnergy / self.batteryEnergy * 100
                else:
                    pass # is a useless section
                    steps = totalTime / self.timeStep
                    distanceStep = totalDistance / steps
                    energyStep = totalEnergy / steps
                    altitudeStep = ( leg["altitudeEnd"] - leg["altitudeStart"] ) / steps

                    # if altitudeStep == 0: #Ie. not ascent or descent
                    periodTime = 0
                    while periodTime < totalTime:
                        self.rows.append( [f"{currTime:.2f}", f"{currAltitude:.2f}", f"{horizontalDistance:.2f}", f"{currHorizontalSpeed:.2f}", f"{currVerticalSpeed:.2f}", f"{currSOC:.2f}", f"{leg['legObject'].realName}", f"{leg['legObject'].value}", f"{self.wingSpan:.2f}", f"{self.wingArea:.2f}", f"{self.totalMass:.2f}", f"{self.batteryCapacity:.2f}", f"{self.maxSpeed:.2f}", f"{self.stallSpeed:.2f}", f"{self.efficientSpeed:.2f}"] )

                        currTime += self.timeStep
                        currDistance += distanceStep
                        horizontalDistance += distanceStep
                        currAltitude += altitudeStep
                        currEnergy -= energyStep
                        currSOC = currEnergy / self.batteryEnergy * 100

                        periodTime += self.timeStep
                    # else:
                    #     pass
            
            # self.rows.append(["Next Period"])
            print("Next Period")
        
        if self.cruiseDistance == None and numOfCruisePeriods != 0:
            self.cruiseDistance = self.mission.parameters["missionDistance"] - horizontalDistance
            self.cruiseDistance /= numOfCruisePeriods
            self.createRows() # need to run twice in order to get the cruise distance
    
    def exportToCSV(self, filePath):
        fileName = "detailedResults.csv"
        self.createRows()
        
        with open(filePath + fileName, 'w', newline='') as csvFile:
            csvWriter = csv.writer( csvFile )
            csvWriter.writerow( self.headers )
            csvWriter.writerows( self.rows )
