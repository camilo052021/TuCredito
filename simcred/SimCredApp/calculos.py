class MiCredito():
    def __init__(self, tasa, plazo, monto):
        self.tasa = tasa
        self.plazo = plazo
        self.monto = monto

    def calcular(self):
        #Cuota = (Monto * (%MV x (1 + %MV) ^ n)) / ((1 + %MV) ^ n) - 1))
        cuota = (self.monto*(self.tasa*(1+self.tasa)**self.plazo))/(((1+self.tasa)**self.plazo)-1)
        #return (self.monto*(self.tasa*(1+self.tasa)**self.plazo))/(((1+self.tasa)**self.plazo)-1)
        return cuota
