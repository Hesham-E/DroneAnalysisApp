import csv
import pandas as pd
from .AtmosphereConditions import AtmosphereConditions

class MotorTableInterface:
    def __init__(self, filePath, pressure, temperature):
        self.filePath = filePath
        self.table = None
        self.atmCond = AtmosphereConditions()

        with open(self.filePath, newline='', encoding='utf-8') as fp:
            reader = csv.DictReader(fp)
            self.table = pd.DataFrame(data = reader)
        
        self.temperature = temperature
        airDensity = self.atmCond.calcAirDensity(pressure, temperature)
        self.table["Thrust (kgf)"] = self.table["Thrust (kgf)"].apply( lambda x: ( airDensity / self.atmCond.SEA_AIR_DENSITY ) ** ( 1/3 ) * float(x) )
    
    def getMaxThrust(self):
        df = self.table.copy()
        
        df = df.apply(pd.to_numeric)
        df = df.fillna(0)
        df = df.sort_values(by = ['Thrust (kgf)'])
        
        return df['Thrust (kgf)'].values[-1] * 9.81 # kgf * 9.81 = Newtons
    
    def getMaxThrustAtAltitude(self, altitude):
        airDensity = self.atmCond.calcAirDensityAtAltitude(altitude, self.temperature)
        df = self.table.copy()
        df = df["Thrust (kgf)"].apply( lambda x: ( airDensity / self.atmCond.SEA_AIR_DENSITY ) ** ( 1/3 ) * float(x) )

        df = df.apply(pd.to_numeric)
        df = df.fillna(0)
        print(df)
        df = df.sort_values()
        
        return df.values[-1] * 9.81 # kgf * 9.81 = Newtons

    def getMinThrust(self):
        df = self.table.copy()
        
        df = df.apply(pd.to_numeric)
        df = df.fillna(0)
        df = df.sort_values(by = ['Thrust (kgf)'])
        
        return df['Thrust (kgf)'].values[0] * 9.81 # kgf * 9.81 = Newtons
    
    def getMaxPower(self):
        df = self.table.copy()
        
        df = df.apply(pd.to_numeric)
        df = df.fillna(0)
        df = df.sort_values(by = ['Electrical power (W)'])

        return df['Electrical power (W)'].values[-1]

    def getPowerAtThrust(self, thrust):
        thrust = thrust / 9.81 # Newtons / 9.81 = kgf
        df = self.table.copy()
        
        df = df.apply(pd.to_numeric)
        df = df.fillna(0)
        df = df.sort_values(by = ['Thrust (kgf)'])

        targetRow = df.loc[df['Thrust (kgf)'] == thrust]
        if targetRow.empty is False: # Data exists, no interpolation needed
            return targetRow['Electrical power (W)'].values[0]
        else: # Interpolate the 'Electrical power (W)'
            nearestValues = df.iloc[(df['Thrust (kgf)'] - thrust).abs().argsort()[ : 2]]
            nearestValues = nearestValues.sort_values(by = ['Thrust (kgf)'])
            
            x1 = nearestValues['Thrust (kgf)'].values[0]
            y1 = nearestValues['Electrical power (W)'].values[0]
            x2 = nearestValues['Thrust (kgf)'].values[1]
            y2 = nearestValues['Electrical power (W)'].values[1]
            
            interpolationRatio = (y2 - y1) / (x2 - x1)
            return interpolationRatio * (thrust - x1) + y1
        
    # def getMechanicalPowerAtThrust(self, thrust):
    #     thrust = thrust / 9.81 # Newtons / 9.81 = kgf
    #     df = self.table.copy()
        
    #     df = df.apply(pd.to_numeric)
    #     df = df.fillna(0)
    #     df = df.sort_values(by = ['Thrust (kgf)'])

    #     targetRow = df.loc[df['Thrust (kgf)'] == thrust]
    #     if targetRow.empty is False: # Data exists, no interpolation needed
    #         return targetRow['Mechanical power (W)'].values[0]
    #     else: # Interpolate the 'Mechanical power (W)'
    #         nearestValues = df.iloc[(df['Thrust (kgf)'] - thrust).abs().argsort()[ : 2]]
    #         nearestValues = nearestValues.sort_values(by = ['Thrust (kgf)'])
            
    #         x1 = nearestValues['Thrust (kgf)'].values[0]
    #         y1 = nearestValues['Mechanical power (W)'].values[0]
    #         x2 = nearestValues['Thrust (kgf)'].values[1]
    #         y2 = nearestValues['Mechanical power (W)'].values[1]
            
    #         interpolationRatio = (y2 - y1) / (x2 - x1)
    #         return interpolationRatio * (thrust - x1) + y1
    
    def getThrottle(self, thrust):
        thrust = thrust / 9.81 # Newtons / 9.81 = kgf
        df = self.table.copy()
        
        df = df.apply(pd.to_numeric)
        df = df.fillna(0)
        df = df.sort_values(by = ['Thrust (kgf)'])

        targetRow = df.loc[df['Thrust (kgf)'] == thrust]
        if targetRow.empty is False: # Data exists, no interpolation needed
            return targetRow['Throttle (%)'].values[0]
        else: # Interpolate the 'Throttle (%)'
            nearestValues = df.iloc[(df['Thrust (kgf)'] - thrust).abs().argsort()[ : 2]]
            nearestValues = nearestValues.sort_values(by = ['Thrust (kgf)'])
            
            x1 = nearestValues['Thrust (kgf)'].values[0]
            y1 = nearestValues['Throttle (%)'].values[0]
            x2 = nearestValues['Thrust (kgf)'].values[1]
            y2 = nearestValues['Throttle (%)'].values[1]
            
            interpolationRatio = (y2 - y1) / (x2 - x1)
            return interpolationRatio * (thrust - x1) + y1

# TESTING
# interface = MotorTableInterface("./ModelLayer/T-motor AT2814 KV900 Cam-Carbon Z 10X8 25X20 test - alipoviy.csv")
# print(interface.getMaxThrust())