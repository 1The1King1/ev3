#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep


class Robozin(object):
    def __init__(self):

        #analogicos

        self.me = LargeMotor("outC")
        self.md = LargeMotor("outD")
        self.cs = ColorSensor()
        self.giro = GyroSensor()

        #mode

        self.giro.mode = "GYRO-ANG"
        self.cs.mode = "COL-COLOR"

        self.preto = True

    def Andar(self):
        self.me.run_forever(speed_sp=600)
        self.md.run_forever(speed_sp=600)

    def MeiaVolta(self):
        print("virando...")
        angulo = self.giro.value() #angulo_inicial
        ang_rel = angulo + 173     #angulo final
        while angulo != ang_rel:
            angulo = self.giro.value()
            self.me.run_forever(speed_sp=200)
            self.md.run_forever(speed_sp=-200)

    def CurvaD(self):
        print("Curva...")
        angulod = self.giro.value() #angulo_inicial
        ang_reld = angulod + 87     #angulo final
        while angulod != ang_reld:
            angulod = self.giro.value()
            self.me.run_forever(speed_sp=300)
            self.md.run_forever(speed_sp=100)
        self.me.stop()
        self.md.stop()

    def CurvaE(self):
        print("Curva...")
        anguloe = self.giro.value() #angulo_inicial
        ang_rele = anguloe - 85     #angulo final
        while anguloe != ang_rele:
            anguloe = self.giro.value()
            self.me.run_forever(speed_sp=110)
            self.md.run_forever(speed_sp=300)

    def Main(self):
        Sound.beep()
        while True:
            if self.cs.value() == 5: #Vermelho
                self.CurvaD()
            if self.cs.value() == 6: #Branco
                print("andando...")
                self.Andar()
            elif self.cs.value() == 1: #Preto
                Sound.beep()
                self.MeiaVolta()
            elif self.cs.value() == 3: #Verde
                Sound.beep()
                self.CurvaE()
            else:
                Sound.beep().wait()
                Sound.beep()
                self.me.stop()
                self.md.stop()
                break

Robozin().Main()

# colors = ["nda","preto","azul","verde","amarelo","vermelho","branco","marrom"]
