import csv
import pandas as pd

class DragLiftCoefficientInterface:
    def __init__(self, filePath):
        self.filePath = filePath

    def getLiftCoefficient(self, angleOfAttack):
        with open(self.filePath, newline='') as fp:
            reader = csv.DictReader(fp)
            df = pd.DataFrame(data = reader)
            df = df.drop(df.columns[0], axis = 1) # first column is just row numbers
            df = df.apply(pd.to_numeric) # convert each entry to numerical values

            possibleAlphas = df['Alpha'].tolist()
            if angleOfAttack < possibleAlphas[0] or angleOfAttack > possibleAlphas[-1]:
                raise Exception(f"This angle of attack is out of range for the data available for this airfoil. Available range is {possibleAlphas[0]} - {possibleAlphas[1]}")
        
            targetRow = df.loc[df['Alpha'] == angleOfAttack]
            if targetRow.empty is False: # Data exists, no interpolation needed
                return targetRow['Cl'].values[0]
            else: # Interpolate the coefficient
                nearestValues = df.iloc[(df['Alpha'] - angleOfAttack).abs().argsort()[ : 2]]
                nearestValues = nearestValues.sort_values(by = ['Alpha'])
                
                x1 = nearestValues['Alpha'].values[0]
                y1 = nearestValues['Cl'].values[0]
                x2 = nearestValues['Alpha'].values[1]
                y2 = nearestValues['Cl'].values[1]
                
                interpolationRatio = (y2 - y1) / (x2 - x1)
                return interpolationRatio * (angleOfAttack - x1) + y1
    
    def getDragCoefficient(self, angleOfAttack):
        with open(self.filePath, newline='') as fp:
            reader = csv.DictReader(fp)
            df = pd.DataFrame(data = reader)
            df = df.drop(df.columns[0], axis = 1) # first column is just row numbers
            df = df.apply(pd.to_numeric) # convert each entry to numerical values

            possibleAlphas = df['Alpha'].tolist()
            if angleOfAttack < possibleAlphas[0] or angleOfAttack > possibleAlphas[-1]:
                raise Exception(f"This angle of attack is out of range for the data available for this airfoil. Available range is {possibleAlphas[0]} - {possibleAlphas[1]}")
        
            targetRow = df.loc[df['Alpha'] == angleOfAttack]
            if targetRow.empty is False: # Data exists, no interpolation needed
                return targetRow['Cd'].values[0]
            else: # Interpolate the coefficient
                nearestValues = df.iloc[(df['Alpha'] - angleOfAttack).abs().argsort()[ : 2]]
                nearestValues = nearestValues.sort_values(by = ['Alpha'])
                
                x1 = nearestValues['Alpha'].values[0]
                y1 = nearestValues['Cd'].values[0]
                x2 = nearestValues['Alpha'].values[1]
                y2 = nearestValues['Cd'].values[1]
                
                interpolationRatio = (y2 - y1) / (x2 - x1)
                return interpolationRatio * (angleOfAttack - x1) + y1


                


reader = DragLiftCoefficientInterface("./xf-naca2408-il-1000000_Subset_1.csv")
print(reader.getLiftCoefficient(0.1)) # Should be 0.24414
print(reader.getLiftCoefficient(-1.24)) # Should be 0.109764

print(reader.getDragCoefficient(0.1)) # Should be 0.004182
print(reader.getDragCoefficient(-1.24)) # Should be 0.0055896