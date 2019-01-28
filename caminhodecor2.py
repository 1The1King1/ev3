#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep
import sys


class Robozin(object):
    def __init__(self):

        # analogicos

        self.motor_E = LargeMotor("outB")
        self.motor_D = LargeMotor("outA")
        self.colorS = ColorSensor("in2")
        self.giroS = GyroSensor()
        # self.infraS = InfraredSensor()
        # self.botao = TouchSensor()

        # mode

        self.giroS.mode = "GYRO-ANG"
        self.colorS.mode = "COL-COLOR"
        # self.infraS = "IR-PROX"

        # Globais

        self.controle_curva = 0
        self.angulo_in = self.giroS.value()
        self.curva = False
        self.caminho = []
        self.voltando = False
        self.velocidade = 300
        self.variacao = 100
        self.erro_ang = 0
        self.verm = 0
        self.verd = 0
        self.azul = 0
        self.angulacao = 0
        self.verdeB = False
        
    def Andar(self):
        print("%s  -  %s" % (self.angulo_in, self.giroS.value()))
        if self.giroS.value() < self.angulo_in:  # erro esquerda
            Sound.beep()
            self.erro_ang = self.angulo_in - self.giroS.value()
            print("%s  -  %s" % (self.angulo_in, self.giroS.value()))
            self.motor_E.run_forever(speed_sp=self.velocidade + (self.erro_ang * self.variacao))
            sleep(0.74)
            self.motor_D.run_forever(speed_sp=self.velocidade + (self.erro_ang * self.variacao))
            sleep(0.21)
        elif self.giroS.value() > self.angulo_in:  # erro direita
            Sound.beep()
            self.erro_ang = self.giroS.value() + self.angulo_in
            print("%s  -  %s" % (self.angulo_in, self.giroS.value()))
            self.motor_D.run_forever(speed_sp=self.velocidade + (self.erro_ang * self.variacao))
            sleep(0.74)
            self.motor_E.run_forever(speed_sp=self.velocidade + (self.erro_ang * self.variacao))
            sleep(0.21)
        if not self.curva and not self.voltando:
            self.caminho.append("|")
        elif not self.voltando:
            self.caminho.append("-")
        self.motor_E.run_forever(speed_sp=self.velocidade)
        self.motor_D.run_forever(speed_sp=self.velocidade)

    def MeiaVolta(self):
        print("Virando...")
        self.voltando = True
        angulo = self.giroS.value()  # angulo_inicial
        ang_rel = angulo + 170  # angulo final
        while angulo < ang_rel:
            angulo = self.giroS.value()
            self.motor_E.run_forever(speed_sp=400)
            self.motor_D.run_forever(speed_sp=-400)

    def CurvaD(self):
        print("Virando...")
        self.voltando = False

        # Angulação da curva

        if self.erro_ang > 0:
            angulod = self.giroS.value()
            ang_reld = angulod + (80 + self.erro_ang)
        elif self.erro_ang < 0:
            angulod = self.giroS.value()
            ang_reld = angulod + (80 - self.erro_ang)
        else:
            angulod = self.giroS.value()
            ang_reld = angulod + 80

        self.motor_D.stop()
        self.motor_E.stop()
        if self.giroS.value() > self.angulo_in:
            while self.giroS.value() > self.angulo_in:
                self.motor_D.run_forever(speed_sp=50)
        elif self.giroS.value() < self.angulo_in:
            while self.giroS.value() < self.angulo_in:
                self.motor_E.run_forever(speed_sp=50)

        self.motor_D.stop()
        self.motor_E.stop()

        while angulod < ang_reld:
            angulod = self.giroS.value()
            self.motor_E.run_forever(speed_sp=400)
            self.motor_D.run_forever(speed_sp=-400)

        self.angulo_in += 80

    def CaminhoInverso(self):
        if self.verm == 0 and self.verd == 0 and self.azul == 0:
            self.verm = 1
            self.verd = 1
            self.azul = 1
            return ('indo')
        else:
            self.verm = 0
            self.verd = 0
            self.azul = 0
            return ('voltando')

    def CurvaE(self):
        print("Virando...")
        self.voltando = False
        # Angulação da curva

        if self.erro_ang > 0:
            anguloe = self.giroS.value()
            if self.erro_ang <= 0:
                print(self.erro_ang)
            ang_rele = anguloe - (80 - self.erro_ang)
        elif self.erro_ang < 0:
            anguloe = self.giroS.value()
            ang_rele = anguloe - (80 + self.erro_ang)
        else:
            anguloe = self.giroS.value()
            ang_rele = anguloe - 80

        # Curva

        self.motor_D.stop()
        self.motor_E.stop()
        if self.giroS.value() > self.angulo_in:
            while self.giroS.value() > self.angulo_in:
                self.motor_D.run_forever(speed_sp=50)
        elif self.giroS.value() < self.angulo_in:
            while self.giroS.value() < self.angulo_in:
                self.motor_E.run_forever(speed_sp=50)

        self.motor_D.stop()
        self.motor_E.stop()

        while anguloe > ang_rele:
            anguloe = self.giroS.value()
            self.motor_E.run_forever(speed_sp=-400)
            self.motor_D.run_forever(speed_sp=400)
            self.controle_curva = 0



    def Main(self):
        Sound.beep()
        while True:  # self.botao.value() == 0:
            print(self.colorS.value())
            if self.colorS.value() == 6:  # Branco
                self.Andar()

            elif self.colorS.value() == 5:  # Vermelho
                self.Andar()

            elif self.colorS.value() == 3:  # Verde
                if not self.verdeB:
                    self.verdeB = True
                    Sound.beep()
                    Sound.beep()
                    if self.CaminhoInverso() == 'indo':
                        self.motor_D.stop()
                        self.motor_E.stop()
                        self.CurvaE()
                        self.motor_D.run_forever(speed_sp=300)
                        self.motor_E.run_forever(speed_sp=300)
                    else:
                        self.motor_D.stop()
                        self.motor_E.stop()
                        self.CurvaD()
                        self.motor_D.run_forever(speed_sp=300)
                        self.motor_E.run_forever(speed_sp=300)
                    self.angulo_in = self.giroS.value()
                else:
                    self.motor_D.stop()
                    self.motor_E.stop()
                    self.Andar()

            elif self.colorS.value() == 2:  # azul
                self.Andar()

            elif self.colorS.value() == 1:  # Preto
                self.MeiaVolta()
                self.CaminhoInverso()
                self.motor_D.run_forever(speed_sp=300)
                self.motor_E.run_forever(speed_sp=300)
                sleep(2)




Robozin().Main()

# colors = ["nda","preto","azul","verde","amarelo","vermelho","branco","marrom"]
