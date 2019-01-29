#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep


class Robozin(object):
    def __init__(self):

        # analogicos
            # motors
        self.motor_D, self.motor_E = LargeMotor("outA"), LargeMotor("outB")

            # Sensors

        self.giroS, self.colorS, self.infraS = GyroSensor("in1"), ColorSensor("in2"), InfraredSensor("in4")

            # mode

        self.giroS.mode, self.colorS.mode, self.infraS.mode = "GYRO-ANG", "COL-COLOR", "IR-PROX"

        # Globais

        self.caminho = []
        self.curva, self.voltando, self.verdeB = False # False Booleans

        self.velocidadeE, self.velocidadeD = 300, 300 # Velocidades

        self.angulo_in, self.variacao, self.erro_ang = self.giroS.value(), 100, 0 # Angulos

        self.verm, self.verd, self.azul = 0, 0, 0

    def Andar(self):

        # Correção do Infrared
        a = 22
        b = 200
        c = 300
        if self.infraS.value() > 40:
            print("%s  -  %s    2.2" % (self.angulo_in, self.giroS.value()))
            self.motor_E.run_to_rel_pos(position_sp=-a, speed_sp=b)
            self.motor_D.run_to_rel_pos(position_sp=a, speed_sp=b)
            self.motor_D.wait_while("running")
            self.motor_D.run_forever(speed_sp=b)
            self.motor_E.run_forever(speed_sp=b)
            sleep(0.9)
            self.motor_E.run_to_rel_pos(position_sp=a, speed_sp=b)
            self.motor_D.run_to_rel_pos(position_sp=-a, speed_sp=b)

        elif self.infraS.value() <= 35:
            print("%s  -  %s    2.1" % (self.angulo_in, self.giroS.value()))
            self.motor_D.stop()
            self.motor_E.run_to_rel_pos(position_sp=a, speed_sp=b)
            self.motor_D.run_to_rel_pos(position_sp=-a, speed_sp=b)
            self.motor_E.wait_while("running")
            self.motor_E.run_forever(speed_sp=b)
            self.motor_D.run_forever(speed_sp=b)
            sleep(0.9)
            self.motor_D.run_to_rel_pos(position_sp=a, speed_sp=b)
            self.motor_E.run_to_rel_pos(position_sp=-a, speed_sp=b)

        # Correção do Giroscopio

        if self.erro_ang in range(-7, 9):
            if self.giroS.value() < self.angulo_in:  # erro esquerda
                Sound.beep()
                self.erro_ang = self.angulo_in - self.giroS.value()
                print("%s  -  %s     3" % (self.angulo_in, self.giroS.value()))
                self.motor_E.run_forever(speed_sp=self.velocidadeE + (self.erro_ang * self.variacao))
                sleep(0.74)
                self.motor_D.run_forever(speed_sp=self.velocidadeD + (self.erro_ang * self.variacao))
                sleep(0.21)
            elif self.giroS.value() > self.angulo_in:  # erro direita
                Sound.beep()
                self.erro_ang = self.giroS.value() + self.angulo_in
                print("%s  -  %s    3" % (self.angulo_in, self.giroS.value()))
                self.motor_D.run_forever(speed_sp=self.velocidadeD + (self.erro_ang * self.variacao))
                sleep(0.74)
                self.motor_E.run_forever(speed_sp=self.velocidadeE + (self.erro_ang * self.variacao))
                sleep(0.21)

        else: # Correção critica do giroscopio

            print("%s  -  %s    1" % (self.angulo_in, self.giroS.value()))
            self.motor_D.stop()
            self.motor_E.stop()
            if self.giroS.value() > self.angulo_in:
                while self.giroS.value() > self.angulo_in:
                    self.motor_D.run_forever(speed_sp=50)
                    self.motor_E.run_forever(speed_sp=-50)
            else:
                while self.giroS.value() < self.angulo_in:
                    self.motor_E.run_forever(speed_sp=50)
                    self.motor_D.run_forever(speed_sp=-50)

            self.motor_D.stop()
            self.motor_E.stop()
        '''
        # Mapeamento
        if not self.curva and not self.voltando:
            self.caminho.append("|")
        elif not self.voltando:
            self.caminho.append("-")
        '''

        # Andando
        self.motor_E.run_forever(speed_sp=self.velocidadeE)
        self.motor_D.run_forever(speed_sp=self.velocidadeD)

    def meiavolta(self):
        print("Virando...")
        self.voltando = True
        angulo = self.giroS.value()  # angulo_inicial
        ang_rel = angulo + 170  # angulo final
        while angulo < ang_rel:
            angulo = self.giroS.value()
            self.motor_E.run_forever(speed_sp=400)
            self.motor_D.run_forever(speed_sp=-400)

    def curvaD(self):
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

    def caminhoinverso(self):
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

    def curvaE(self):
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

    def main(self):
        Sound.beep()
        while True:
            if self.colorS.value() == 6:  # Branco
                self.Andar()

            elif self.colorS.value() == 5:  # Vermelho
                self.Andar()

            elif self.colorS.value() == 3:  # Verde
                if not self.verdeB:
                    self.verdeB = True
                    Sound.beep()
                    Sound.beep()
                    if self.caminhoinverso() == 'indo':
                        self.motor_D.stop()
                        self.motor_E.stop()
                        self.curvaE()
                        self.motor_D.run_forever(speed_sp=300)
                        self.motor_E.run_forever(speed_sp=300)
                    else:
                        self.motor_D.stop()
                        self.motor_E.stop()
                        self.curvaD()
                        self.motor_D.run_forever(speed_sp=300)
                        self.motor_E.run_forever(speed_sp=300)
                    self.angulo_in = self.giroS.value()
                else:
                    self.motor_D.stop()
                    self.motor_E.stop()
                    self.Andar()

            elif self.colorS.value() == 2:  # azul
                #self.Andar()
                break
            elif self.colorS.value() == 1:  # Preto
                self.meiavolta()
                self.caminhoinverso()
                self.motor_D.run_forever(speed_sp=300)
                self.motor_E.run_forever(speed_sp=300)
                sleep(2)

        self.motor_E.stop()
        self.motor_D.stop()



Robozin().main()

# colors = ["nda","preto","azul","verde","amarelo","vermelho","branco","marrom"]
