import csv

class ResultsWriter:
    def __init__(self, mission, batteryEnergy):
        self.legInfos = [] # array of dictionaries, in order in mission 
        self.rows = [] # processed data from legInfos to be written
        self.timeStep = 0.1 # second
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

        for leg in self.legInfos:
            totalTime = leg["timeEnd"] - leg["timeStart"]
            steps = totalTime / self.timeStep
            distanceStep = leg["distanceTravelled"] / steps
            energyStep = leg["energyExpended"] / steps
            print(energyStep)
            altitudeStep = ( leg["altitudeEnd"] - leg["altitudeStart"] ) / steps

            periodTime = 0

            while periodTime <= leg["timeEnd"]:
                self.rows.append( [f"{currTime}", f"{currAltitude}", f"{currDistance}", f"{currSOC}"] )

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
