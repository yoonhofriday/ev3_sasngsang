#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

ev3 = EV3Brick()

#모터 선언
ml = Motor(Port.A)  #왼쪽 모터
mr = Motor(Port.D)  #오른쪽 모터
mm = Motor(Port.C)  #미디엄 모터

#센서 선언
CSr = ColorSensor(Port.S1)      #오른쪽 컬러센서
CSl = ColorSensor(Port.S2)      #왼쪽 컬러센서
CSm = ColorSensor(Port.S3)      #미션 수행을 위한 컬러센서 
IS = InfraredSensor(Port.S4)    #적외선 센서


def line_tracking(): #라인트레킹 

    csr = CSr.reflection()          #메인 코드에서 설명
    csm = CSm.reflection()
    csl = CSl.reflection()

    ms = 150    #모터속도
    ml.run(ms + ((60 - csr) / 2 * 5))   #오른쪽 센서의 반사값이 낮아지면 왼쪽 모터속도 up
    mr.run(ms + ((60 - csl) / 2 * 5))   #왼쪽 센서의 반사값이 낮아지면 오른쪽 모터속도 up

def go(x, y):   #전진 (파워, 초)
    ml.run_time(x, y * 1000, Stop.HOLD, False)
    mr.run_time(x, y * 1000, Stop.HOLD, True)

def back(x, y): #후진 (파워, 초)
    ml.run_time(-x, y * 1000, Stop.HOLD, False)
    mr.run_time(-x, y * 1000, Stop.HOLD, True)

def left_turn(x, y):  #왼쪽 턴 (파워, 각도)
    ml.run_angle(-x, (y + 23) * 2, Stop.HOLD, False)
    mr.run_angle(x, (y + 23) * 2, Stop.HOLD, True)

def right_turn(x, y): #우측 턴 (파워, 각도)
    ml.run_angle(x, y * 2, Stop.HOLD, False)
    mr.run_angle(-x, y * 2, Stop.HOLD, True)

def stop(y):
    ml.run_time(0, y * 1000, Stop.HOLD, False)
    mr.run_time(0, y * 1000, Stop.HOLD, True)

def arm(y):  #팔(-1 = 위로, 1 = 아래로 움직임)
    mm.run_angle(200, y * 120, Stop.HOLD, True)


def mission1(): #미션1                     
    go(200, 1.8)
    left_turn(200, 100)
    go(200, 1.6)
    

def mission2_1(): #미션2-1
    go(200,1.8)
    arm(-1)
    go(200, 1.3)
    left_turn(100, 93)


def mission2_2(): #미션2-2
    go(100, 1.3)
    go(0,1)
    arm(1)
    back(200, 1)
    left_turn(200, 190)


def mission2_3(): #미션2-3
    go(200, 1.3)
    left_turn(200, 90)


def mission3(): #미션3
    while True:
        isd = IS.distance()             #메인 코드에서 설명
        csr = CSr.reflection()
        csm = CSm.reflection()
        csl = CSl.reflection()

        line_tracking()                 #라인트레킹 

        if isd < 5:                     #거리가 5미만일 경우 실행
            go(100, 4.2)
            back(100, 1)
            stop(2)
            break


def mission4(): #미션4
    go(100, 1.8)
    while True:
        csr = CSr.reflection()          #메인 코드에서 설명
        csl = CSl.reflection()
        csm = CSm.reflection()

        #(민감한)라인트레킹
        ms = 50  #모터속도
        ml.run(ms + ((70 - csr) * 6))
        mr.run(ms + ((70 - csl) * 6))

        if csm == 0:                    #검은색 선 인식시 
            break                       #미션 4 중지


def mission5(): #미션5
    stop(3)
    while True: 
        isd = IS.distance()         #메인 코드에서 설명
        csr = CSr.reflection()
        csm = CSm.reflection()
        csl = CSl.reflection()

        line_tracking()             #라인트레킹 

        if isd < 10:                #거리가 10미만일 경우 수행
            stop(1.5)
            left_turn(200, 202)
            go(300, 6.6)
            mission6()              #미션6 수행
            break

def mission6(): #미션6
    right_turn(200, 110)
    arm(-0.7)
    go(200, 0.7)
    stop(1)
    ev3.speaker.beep(1000,500)      #삐소리를 볼륨 500으로 1초 재생  
    stop(1)
    back(200, 0.9)
    arm(0.7)
    left_turn(200, 90)


stack = 1   #미션 수행하기을 돕는 변수

while True: #메인 코드
    isd = IS.distance()     #적외선 센서의 거리값 저장
    csr = CSr.reflection()  #우 컬러센서의 반사값 저장      (반사값이 낮을수록 어두움)
    csm = CSm.reflection()  #미션수행 컬러센서 반사값 저장  (반사값이 높을수록 밝음)
    csl = CSl.reflection()  #좌 컬러센서의 반사값 저장


    line_tracking()         #라인트레킹 

    if csm == 0:            #검은색 선 인식시 미션을  실행

        if stack == 1:      #stack이 1이면 미션1 수행
            mission1()
            stack += 1      #stack에 1 더하기

        elif stack == 2:    #stack이 2이면 미션2-1 수행
            mission2_1()
            stack += 1

        elif stack == 3:    #stack이 3이면 미션2-2 수행
            mission2_2()
            stack += 1

        elif stack == 4:    #stack이 4이면 미션2-3 수행
            mission2_3()
            stack += 1

        elif stack == 5:    #stack이 5이면 미션3 수행
            stack += 1
            mission3()

        elif stack == 6:    #stack이 6이면 미션4 수행
            stack += 1
            mission4()

        elif stack == 7:    #stack이 7이면 미션5 수행
            mission5()

        



#당일 미션

#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

ev3 = EV3Brick()

#모터 선언
ml = Motor(Port.A)  #왼쪽 모터
mr = Motor(Port.D)  #오른쪽 모터
mm = Motor(Port.C)  #미디엄 모터

#센서 선언
CSr = ColorSensor(Port.S1)      #오른쪽 컬러센서
CSl = ColorSensor(Port.S2)      #왼쪽 컬러센서
CSm = ColorSensor(Port.S3)      #미션 수행을 위한 컬러센서 
IS = InfraredSensor(Port.S4)    #적외선 센서


def line_tracking(): #라인트레킹 

    csr = CSr.reflection()          #메인 코드에서 설명
    csm = CSm.reflection()
    csl = CSl.reflection()

    ms = 150    #모터속도
    ml.run(ms + ((60 - csr) * 2))   #오른쪽 센서의 반사값이 낮아지면 왼쪽 모터속도 up
    mr.run(ms + ((60 - csl) * 2))   #왼쪽 센서의 반사값이 낮아지면 오른쪽 모터속도 up

def go(x, y):   #전진 (파워, 초)
    ml.run_time(x, y * 1000, Stop.HOLD, False)
    mr.run_time(x, y * 1000, Stop.HOLD, True)

def back(x, y): #후진 (파워, 초)
    ml.run_time(-x, y * 1000, Stop.HOLD, False)
    mr.run_time(-x, y * 1000, Stop.HOLD, True)

def left_turn(x, y):  #왼쪽 턴 (파워, 각도)
    ml.run_angle(-x, (y + 23) * 2, Stop.HOLD, False)
    mr.run_angle(x, (y + 23) * 2, Stop.HOLD, True)

def right_turn(x, y): #우측 턴 (파워, 각도)
    ml.run_angle(x, y * 2, Stop.HOLD, False)
    mr.run_angle(-x, y * 2, Stop.HOLD, True)

def stop(x):
    ml.run_time(0, y * 1000, Stop.HOLD, False)
    mr.run_time(0, y * 1000, Stop.HOLD, True)

def arm(y):  #팔(-1 = 위로, 1 = 아래로 움직임)
    mm.run_angle(200, y * 110, Stop.HOLD, True)


def first_curve():                      
    go(200, 2)
    right_turn(200, 100)
    go(200, 1.6)
    

def take_bottle(): 
    arm(-1)

def put_bottle():
    arm(1)
    back(200,1)
    right_turn(200,190)

def second_curve():
    left_turn(200, 100)





stack = 1   #미션 수행하기을 돕는 변수

while True: #메인 코드
    csr = CSr.reflection()  #우 컬러센서의 반사값 저장      (반사값이 낮을수록 어두움)
    csm = CSm.reflection()  #미션수행 컬러센서 반사값 저장  (반사값이 높을수록 밝음)
    csl = CSl.reflection()  #좌 컬러센서의 반사값 저장


    line_tracking()         #라인트레킹 

    if csm == 0:            #검은색 선 인식시 미션을  실행

        if stack == 1:      #stack이 1이면 first_curve 수행
            first_curve()
            stack += 1      #stack에 1 더하기

        elif stack == 2:    #stack이 2이면 take_bottle 수행
            take_bottle()
            stack += 1

        elif stack == 3:    #stack이 3이면 put_bottle 수행
            put_bottle()
            stack += 1

        elif stack == 4:    #stack이 4이면 second_curve 수행
            second_curve()   
        
        
            



    
     
    

