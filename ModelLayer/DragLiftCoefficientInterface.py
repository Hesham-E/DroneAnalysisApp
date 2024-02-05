import csv
import pandas as pd
import math

class DragLiftCoefficientInterface:
    def __init__(self, filePath):
        self.filePath = filePath

    def getCoefficientHelper(self, angleOfAttack, coefficient):
        with open(self.filePath, newline='', encoding='utf-8') as fp:
            reader = csv.DictReader(fp)
            df = pd.DataFrame(data = reader)

        df = df.drop(df.columns[0], axis = 1) # first column is just row numbers
        df = df.apply(pd.to_numeric) # convert each entry to numerical values
        df = df.fillna(0)

        possibleAlphas = df['Alpha'].tolist()
        if angleOfAttack < possibleAlphas[0] or angleOfAttack > possibleAlphas[-1]:
            raise Exception(f"This angle of attack is out of range for the data available for this airfoil. Available range is {possibleAlphas[0]} - {possibleAlphas[1]}")
    
        targetRow = df.loc[df['Alpha'] == angleOfAttack]
        if targetRow.empty is False: # Data exists, no interpolation needed
            return targetRow[coefficient].values[0]
        else: # Interpolate the coefficient
            nearestValues = df.iloc[(df['Alpha'] - angleOfAttack).abs().argsort()[ : 2]]
            nearestValues = nearestValues.sort_values(by = ['Alpha'])
            
            x1 = nearestValues['Alpha'].values[0]
            y1 = nearestValues[coefficient].values[0]
            x2 = nearestValues['Alpha'].values[1]
            y2 = nearestValues[coefficient].values[1]
            
            interpolationRatio = (y2 - y1) / (x2 - x1)
            return interpolationRatio * (angleOfAttack - x1) + y1

    def getLiftCoefficient(self, angleOfAttack, wingSpan, wingArea, liftDistribution):
        airfoilLift = self.getLiftSlope()
        aspectRatio = wingSpan ** 2 / wingArea 
        wingLift = airfoilLift / ( 1 + airfoilLift / (math.pi * liftDistribution * aspectRatio) )
        zeroLiftAngle = self.getZeroLiftAngle()

        return wingLift * (angleOfAttack - zeroLiftAngle)
    
    def getDragCoefficient(self, angleOfAttack):
        return self.getCoefficientHelper(angleOfAttack, 'Cd')
    
    def getParasiticDragCoefficient(self, angleOfAttack):
        return self.getCoefficientHelper(angleOfAttack, 'Cdp')
    
    def getLiftSlope(self):
        with open(self.filePath, newline='', encoding='utf-8') as fp:
            reader = csv.DictReader(fp)
            df = pd.DataFrame(data = reader)
        
        df = df.drop(df.columns[0], axis = 1) # first column is just row numbers
        df = df.apply(pd.to_numeric) # convert each entry to numerical values
        df = df.fillna(0)

        # we know that the lift slope is linear in the middle
        half = int(len(df) / 2)
        x1 = df.iloc[half]['Alpha']
        y1 = df.iloc[half]['Cl']
        x2 = df.iloc[half + 1]['Alpha']
        y2 = df.iloc[half + 1]['Cl']

        return (y2 - y1) / (x2 - x1)
    
    def getLiftSlopeAt(self, angleOfAttack):
        with open(self.filePath, newline='', encoding='utf-8') as fp:
            reader = csv.DictReader(fp)
            df = pd.DataFrame(data = reader)

        df = df.drop(df.columns[0], axis = 1) # first column is just row numbers
        df = df.apply(pd.to_numeric) # convert each entry to numerical values
        df = df.fillna(0)

        possibleAlphas = df['Alpha'].tolist()
        if angleOfAttack < possibleAlphas[0] or angleOfAttack > possibleAlphas[-1]:
            raise Exception(f"This angle of attack is out of range for the data available for this airfoil. Available range is {possibleAlphas[0]} - {possibleAlphas[1]}")
    
        targetRow = df.index[df['Alpha'] == angleOfAttack].tolist()
        if targetRow is not []: # Data exists, no interpolation needed
            idx = targetRow[0]
            if idx != len(df) -1:
                x1 = df['Alpha'][idx]
                y1 = df['Cl'][idx]
                x2 = df['Alpha'][idx + 1]
                y2 = df['Cl'][idx + 1]
            elif idx == len(df) -1:
                x1 = df['Alpha'][idx - 1]
                y1 = df['Cl'][idx - 1]
                x2 = df['Alpha'][idx]
                y2 = df['Cl'][idx]
            
            interpolationRatio = (y2 - y1) / (x2 - x1)
        else: # Interpolate the 'Cl'
            nearestValues = df.iloc[(df['Alpha'] - angleOfAttack).abs().argsort()[ : 2]]
            nearestValues = nearestValues.sort_values(by = ['Alpha'])
            
            x1 = nearestValues['Alpha'].values[0]
            y1 = nearestValues['Cl'].values[0]
            x2 = nearestValues['Alpha'].values[1]
            y2 = nearestValues['Cl'].values[1]
            
            interpolationRatio = (y2 - y1) / (x2 - x1)

        return interpolationRatio
    
    def getZeroLiftAngle(self):
        with open(self.filePath, newline='', encoding='utf-8') as fp:
            reader = csv.DictReader(fp)
            df = pd.DataFrame(data = reader)

        df = df.drop(df.columns[0], axis = 1) # first column is just row numbers
        df = df.apply(pd.to_numeric) # convert each entry to numerical values
        df = df.fillna(0)
    
        targetRow = df.loc[df['Cl'] == 0]
        if targetRow.empty is False: # Data exists, no interpolation needed
            return targetRow['Alpha'].values[0]
        else: # Interpolate the 'Cl'
            nearestValues = df.iloc[(df['Cl'] - 0).abs().argsort()[ : 2]]
            nearestValues = nearestValues.sort_values(by = ['Cl'])
            
            x1 = nearestValues['Cl'].values[0]
            y1 = nearestValues['Alpha'].values[0]
            x2 = nearestValues['Cl'].values[1]
            y2 = nearestValues['Alpha'].values[1]
            
            interpolationRatio = (y2 - y1) / (x2 - x1)
            return interpolationRatio * (0 - x1) + y1 # Cl == 0


                

# TESTING
# reader = DragLiftCoefficientInterface("./ModelLayer/xf-naca2408-il-500000_Subset_1.csv")
# print(reader.getLiftCoefficient(0.1))
# print(reader.getLiftCoefficient(-1.24)) 

# print(reader.getDragCoefficient(0.1)) 
# print(reader.getDragCoefficient(-1.24)) 