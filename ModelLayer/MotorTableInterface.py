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


interface = MotorTableInterface("./T-motor AT2814 KV900 Cam-Carbon Z 10X8 25X20 test - alipoviy.csv")
print(interface.getMaxThrust())