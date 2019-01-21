#!usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep
Eng1 = LargeMotor("outA")
Eng2 = LargeMotor("outB")
Cl1 = ColorSensor("in1")
Led = Leds()
#Modo de reflexão, intensidade da luz!
Cl1.mode = "COL-REFLECT"
Bt1 = Button()
print(" Bem-Vindo!\n","Botões para ser pressionados:\n","1 - Enter\n","2 - Backspace\n")
# Se o botão enter for pressionado!
def enter(state) :
    #Liga os leds dos botões da esquerda e direita!
    Led.set_color("LEFT", "RED")
    Led.set_color("RIGHT", "RED")
    while True :
        Speed = 700
        Direcao = "Indo para frente"
        #Os motores teram velocidade de 700
        Eng1.run_forever(speed_sp = Speed)
        Eng2.run_forever(speed_sp = Speed)
        print(Direcao)
        print("Taxa de intensidade da luz %d" %(int(Cl1.value())))
        #Se a reflexão for menor igual a 5, a velocidade será negativa!
        if Cl1.value() <= 5 :
            Speed = Speed * (-1)
            Direcao = "Indo para trás"
def backspace(state) :
    Cont = 0
    while True :
        #Quando o contador for um númeo par será acesa a cor ambar!
        if Cont % 2 == 0 :
            Led.set_color("LEFT", "AMBER")
            Led.set_color("RIGHT", "AMBER")
            Cont += 1
        else :
            Cont += 1
            #Reproduz um fequência de som de 1500 Mhz por 0.6s a cada 0.5s
            sound.tone([(1500, 600, 500)]).wait
        #ira freiar o robõ de maneira lenta!
        Eng1.stop(stop_action = coast)
        Eng2.stop(stop_action = coast)
Bt1.on_enter = enter
Bt1.on_backspace = backspace
#Loop para checar os botôes!
while True :
    Bt1.process()
    #Botões são checados a cada 0.01 s
    sleep(0.01)