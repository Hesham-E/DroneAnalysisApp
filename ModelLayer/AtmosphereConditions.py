class AtmosphereConditions:
    SEA_PRESSURE = 101325.0 # Pascals
    SEA_TEMP = 288.15 # Kelvins
    LAPSE_RATE = 0.0065 # K/m
    GAS_CONSTANT = 8.3144698 # J/mol-K
    G_ACCEL = 9.80665 # m/s^2
    AIR_MOLAR_MASS = 0.028964 # kg/mol

    def calcIdealDensityAltitude(self, pressure, temperature):
        tempRatio = temperature / self.SEA_TEMP
        pressureRatio = pressure / self.SEA_PRESSURE
        tempPressureRatio = pressureRatio / tempRatio

        exponentialRatio = (self.G_ACCEL * self.AIR_MOLAR_MASS) / (self.LAPSE_RATE * self.GAS_CONSTANT)
        exponentialRatio = exponentialRatio - 1.0
        exponentialRatio = exponentialRatio ** -1.0

        tempPressureRatio = tempPressureRatio ** exponentialRatio
        tempPressureRatio = 1.0 - tempPressureRatio

        seaTempLapseRatio = self.SEA_TEMP / self.LAPSE_RATE

        return seaTempLapseRatio * tempPressureRatio

        
