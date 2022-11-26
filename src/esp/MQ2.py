from machine import Pin, ADC
from math import log
from time import sleep

class MQ2:
    coefficients = {'CO': (1.512022272, -0.33975668)}

    def __init__(self, pin: int):
        self.pin = Pin(pin, Pin.IN)
        self.adc = ADC(self.pin, atten=ADC.ATTN_11DB)
        self.R0 = 2

    def calculateR0(self):
        print('Calculando R0...')
        Vin = 5000000 #microVolts
        Vout = 0
        for _ in range(100):
            Vout += self.adc.read_uv()
            sleep(0.1)
        print(f'Vout: {Vout}')
        Vout = Vout / 100
        Rs = (Vin - Vout)/Vout

        self.R0 = Rs/9.8
        print(f'R0 calculado: {self.R0}')

    def getPPM(self, gas: str):
        Vin = 5000000 #microVolts
        Vout = 0
        for _ in range(100):
            Vout += self.adc.read_uv()

        Vout = Vout/100

        Rs = (Vin - Vout)/Vout
        y = Rs/self.R0
        print(f'ratio = {y}')
        return 10 ** ((log(y, 10) - self.coefficients['CO'][0]) / self.coefficients['CO'][1])
