import csv
import pandas as pd

class MotorTableInterface:
    def __init__(self, filePath):
        self.filePath = filePath
    
    def getMaxThrust(self):
        with open(self.filePath, newline='', encoding='utf-8') as fp:
            reader = csv.DictReader(fp)
            df = pd.DataFrame(data = reader)
        
        df = df.apply(pd.to_numeric)
        df = df.fillna(0)
        df = df.sort_values(by = ['Thrust (kgf)'])
        
        return df['Thrust (kgf)'].values[-1] * 9.81 # kgf * 9.81 = Newtons
    
    def getMaxPower(self):
        with open(self.filePath, newline='', encoding='utf-8') as fp:
            reader = csv.DictReader(fp)
            df = pd.DataFrame(data = reader)
        
        df = df.apply(pd.to_numeric)
        df = df.fillna(0)
        df = df.sort_values(by = ['Electrical power (W)'])

        return df['Electrical power (W)'].values[-1]

    def getPowerAtThrust(self, thrust):
        thrust = thrust / 9.81 # Newtons / 9.81 = kgf
        with open(self.filePath, newline='', encoding='utf-8') as fp:
            reader = csv.DictReader(fp)
            df = pd.DataFrame(data = reader)
        
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

# TESTING
# interface = MotorTableInterface("./ModelLayer/T-motor AT2814 KV900 Cam-Carbon Z 10X8 25X20 test - alipoviy.csv")
# print(interface.getMaxThrust())