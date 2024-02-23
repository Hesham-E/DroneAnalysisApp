import csv
from .Mission import *

class ResultsWriter:
    def __init__(self, mission, batteryEnergy):
        self.legInfos = [] # array of dictionaries, in order in mission 
        self.rows = [] # processed data from legInfos to be written
        self.timeStep = 0.1 # seconds
        self.headers = ["Time (s)", "Altitude (m)", "Distance Travelled (m)", "State of Charge (%)"]

        self.mission = mission
        # self.batteryCapactiy = batteryCapacity
        # self.batteryVoltage = batteryVoltage
        self.batteryEnergy = batteryEnergy
    
    def createRows(self):
        currTime = 0
        currDistance = 0
        currAltitude = self.legInfos[0]["altitudeStart"]
        currSOC = 100
        currEnergy = self.batteryEnergy

        print(currEnergy)
        print(self.legInfos)

        for count, leg in enumerate( self.legInfos ):
            totalTime = leg["timeEnd"] - leg["timeStart"]
            totalDistance = leg['distanceTravelled']
            totalEnergy = leg["energyExpended"]
            
            if "timeAccelerating" in leg.keys(): # non-linear rate of change
                
                # acceleration period
                timeA = leg["timeAccelerating"]
                distA = leg["distanceAccelerating"]
                energyA = leg["energyAccelerating"]
                
                acceleration = 2 * distA / (timeA ** 2)
                accelDirection = -1 if leg["altitudeEnd"] - leg["altitudeStart"] < 0 else 1

                print(timeA)
                print(distA)
                print(energyA)
                print(acceleration)
                print(accelDirection)
                print(self.timeStep)
                print(leg["mass"])
                print()

                periodTime = 0
                periodDistance = 0
                while periodTime < timeA:
                    self.rows.append( [f"{currTime:.2f}", f"{currAltitude:.2f}", f"{currDistance:.2f}", f"{currSOC:.2f}"] )

                    currTime += self.timeStep
                    periodTime += self.timeStep

                    print(periodDistance)
                    prevPeriodDistance = periodDistance
                    periodDistance = periodDistance / periodTime * self.timeStep + 0.5 * acceleration * ( periodTime ** 2 )
                    currDistance += abs( prevPeriodDistance - periodDistance )
                    
                    currEnergy -= acceleration * self.timeStep * leg["mass"]
                    currSOC = currEnergy / self.batteryEnergy * 100

                    if "timeDecelerating" in leg.keys(): #VTOL Take Off or Landing since only they have deceleration, therefore, altitude changes too
                        currAltitude += abs( prevPeriodDistance - periodDistance ) * accelDirection
                
                print("Done VTOL Accel")
                self.rows.append(["Done VTOL Accel"])
                # break

                if "timeDecelerating" in leg.keys(): # only the VTOL modes do this, so we know the next two periods
                    # linear period
                    time = totalTime - timeA - leg["timeDecelerating"]
                    dist = totalDistance - distA - leg["distanceDecelerating"]
                    energy = totalEnergy - energyA - leg["energyDecelerating"]
                    steps = time / self.timeStep

                    distanceStep = dist / steps
                    altitudeStep = distanceStep #TODO: Try to calculate this somehow to make the program more dynamic. Works currently given all our use cases though
                    energyStep = energy / steps

                    print(steps)
                    print(time)
                    print(dist)
                    print(energy)
                    print(self.timeStep)
                    print(distanceStep)
                    print(altitudeStep)
                    print(energyStep)
                    print()

                    periodTime = 0
                    while periodTime <= time:
                        self.rows.append( [f"{currTime:.2f}", f"{currAltitude:.2f}", f"{currDistance:.2f}", f"{currSOC:.2f}"] )

                        currTime += self.timeStep
                        periodTime += self.timeStep
                        currDistance += distanceStep
                        currAltitude += altitudeStep
                        currEnergy -= energyStep
                        currSOC = currEnergy / self.batteryEnergy * 100
                    
                    print("Done VTOL Linear")
                    self.rows.append(["Done VTOL Linear"])

                    # deceleration period
                    timeD = leg["timeDecelerating"]
                    distD = leg["distanceDecelerating"]
                    energyD = leg["energyDecelerating"]
                    
                    acceleration = 2 * distD / (timeD ** 2)
                    accelDirection = -1 if leg["altitudeEnd"] - leg["altitudeStart"] < 0 else 1

                    print(timeD)
                    print(distD)
                    print(energyD)
                    print(acceleration)
                    print(accelDirection)
                    print(self.timeStep)
                    print(leg["mass"])
                    print()

                    periodTime = 0
                    periodDistance = 0
                    while periodTime < timeD:
                        self.rows.append( [f"{currTime:.2f}", f"{currAltitude:.2f}", f"{currDistance:.2f}", f"{currSOC:.2f}"] )

                        currTime += self.timeStep
                        periodTime += self.timeStep

                        print(periodDistance)
                        prevPeriodDistance = periodDistance
                        periodDistance = periodDistance / periodTime * self.timeStep + 0.5 * acceleration * ( periodTime ** 2 )
                        currDistance += abs( prevPeriodDistance - periodDistance )
                        
                        currEnergy -= acceleration * self.timeStep * leg["mass"]
                        currSOC = currEnergy / self.batteryEnergy * 100

                        if "timeDecelerating" in leg.keys(): #VTOL Take Off or Landing since only they have deceleration, therefore, altitude changes too
                            currAltitude += abs( prevPeriodDistance - periodDistance ) * accelDirection
                    
                    print("Done VTOL Decel")
                    self.rows.append(["Done VTOL Decel"])
                    break

            else: # linear rate of change, ie. no acceleration in this period
                steps = totalTime / self.timeStep
                distanceStep = totalDistance / steps
                energyStep = totalEnergy / steps
                print(energyStep)
                altitudeStep = ( leg["altitudeEnd"] - leg["altitudeStart"] ) / steps

                while periodTime <= leg["timeEnd"]:
                    self.rows.append( [f"{currTime:.2f}", f"{currAltitude:.2f}", f"{currDistance:.2f}", f"{currSOC:.2f}"] )

                    currTime += self.timeStep
                    currDistance += distanceStep
                    currAltitude += altitudeStep
                    currEnergy -= energyStep
                    currSOC = currEnergy / self.batteryEnergy * 100

                    periodTime += self.timeStep
            
            self.rows.append(["Next Period"])
    
    def exportToCSV(self, filePath):
        fileName = "detailedResults.csv"
        self.createRows()
        
        with open(filePath + fileName, 'w') as csvFile:
            csvWriter = csv.writer( csvFile )
            csvWriter.writerow( self.headers )
            csvWriter.writerows( self.rows )
