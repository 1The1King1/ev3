#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep
import sys


class Robozin(object):
    def __init__(self):

        #analogicos

        self.motor_E = LargeMotor("outB")
        self.motor_D = LargeMotor("outA")
        self.colorESQ = ColorSensor("in3")
        self.colorDIR = ColorSensor("in4")
        self.colorTRAS = ColorSensor("in2")
        self.giroS = GyroSensor()
        self.verm = False
        # self.infraS = InfraredSensor()
        #self.botao = TouchSensor()

        # mode

        self.giroS.mode = "GYRO-ANG"
        self.colorESQ.mode = "COL-COLOR"
        self.colorTRAS.mode = "COL-COLOR"
        self.colorDIR.mode = "COL-COLOR"
        # self.infraS = "IR-PROX"

        #Globais

        self.angulo_in = self.giroS.value()
        self.curva = False
        self.caminho = []
        self.voltando = False
        self.velocidade = 300
        self.variacao = 100

    def Andar(self):
        print("%s  -  %s" % (self.angulo_in, self.giroS.value()))
        if self.giroS.value() < self.angulo_in:  # esquerda
            Sound.beep()
            f = self.angulo_in - self.giroS.value()
            self.motor_E.run_forever(speed_sp=self.velocidade + (f * self.variacao))
            sleep(0.7)
            self.motor_D.run_forever(speed_sp=self.velocidade + (f * self.variacao))
            sleep(0.2)
        elif self.giroS.value() > self.angulo_in:  # direita
            Sound.beep()
            f = self.giroS.value() + self.angulo_in
            self.motor_D.run_forever(speed_sp=self.velocidade + (f * self.variacao))
            sleep(0.7)
            self.motor_E.run_forever(speed_sp=self.velocidade + (f * self.variacao))
            sleep(0.2)
        if not self.curva and not self.voltando:
            self.caminho.append("|")
        elif not self.voltando:
            self.caminho.append("-")
        self.motor_E.run_forever(speed_sp=self.velocidade)
        self.motor_D.run_forever(speed_sp=self.velocidade)

    def MeiaVolta(self):
        sys.stdout.write("Virando...")
        self.voltando = True
        angulo = self.giroS.value() #angulo_inicial
        ang_rel = angulo + 170      #angulo final
        while angulo < ang_rel:
            angulo = self.giroS.value()
            self.motor_E.run_forever(speed_sp=400)
            self.motor_D.run_forever(speed_sp=-400)

    def CurvaD(self):
        print("Virando...")
        self.voltando = False
        angulod = self.giroS.value() #angulo_inicial
        ang_reld = angulod + 80      #angulo final
        while angulod < ang_reld:
            angulod = self.giroS.value()
            self.motor_E.run_forever(speed_sp=400)
            self.motor_D.run_forever(speed_sp=-400)

    def CurvaE(self):
        print("virando..")
        self.voltando = False
        anguloe = self.giroS.value() #angulo_inicial
        ang_rele = anguloe - 80      #angulo final
        while anguloe > ang_rele:
            anguloe = self.giroS.value()
            self.motor_E.run_forever(speed_sp=-400)
            self.motor_D.run_forever(speed_sp=400)

    def Main(self):
        Sound.beep()
        print("")
        while True: #self.botao.value() == 0:
            if self.colorESQ.value() == 5 or self.colorDIR.value() == 5:
                self.velocidade = 150

            if self.colorTRAS.value() == 5 and not self.verm: #Vermelho
                self.verm = True
                self.caminho.append("R")
                self.curva = not self.curva
                self.CurvaD()
                self.motor_D.run_forever(speed_sp=300)
                self.motor_E.run_forever(speed_sp=300)
                sleep(2)
            if self.colorTRAS.value() == 6: #Branco

                self.Andar()
            elif self.colorTRAS.value() == 1: #Preto
                self.verm = False
                self.caminho.append("B")
                Sound.beep()
                self.MeiaVolta()
            elif self.colorTRAS.value() == 3: #Verde
                self.verm = False
                self.caminho.append("G")
                Sound.beep()
                self.CurvaE()
            else:
                Sound.beep().wait()
                Sound.beep()
                self.motor_E.stop()
                self.motor_D.stop()

        self.motor_E.stop()
        self.motor_D.stop()

        print(self.caminho)
        with open("mapa.txt", "w") as f:
            map = [self.caminho[0]]
            for i in range(1, len(self.caminho)):
                if self.caminho[i] != map[-1]:
                    map.append(self.caminho[i])


Robozin().Main()

# colors = ["nda","preto","azul","verde","amarelo","vermelho","branco","marrom"]
