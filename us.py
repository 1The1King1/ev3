#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep

me = LargeMotor("outD")
md = LargeMotor("outC")
Us1 = UltrasonicSensor()
giro = GyroSensor()

giro.mode = "GYRO-ANG"
Us1.mode = "US-DIST-CM"
while True:
    distancia = Us1.value() / 10
    velo = int((distancia * 500)/100) + distancia
    print(velo, distancia)
    if distancia >= 10:
        if velo <= 800:
            me.run_forever(speed_sp=velo)
            md.run_forever(speed_sp=velo)
        else:
            me.run_forever(speed_sp=900)
            md.run_forever(speed_sp=900)
    else:
        print("Curva...")
        angulod = giro.value()  # angulo_inicial
        ang_reld = angulod + 87  # angulo final
        while angulod != ang_reld:
            angulod = giro.value()
            me.run_forever(speed_sp=500)
            md.run_forever(speed_sp=-500)
        Sound.beep().wait()
        me.stop()
        md.stop()
