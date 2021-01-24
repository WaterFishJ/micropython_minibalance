import pyb

p = pyb.Pin('Y3') # X1 has TIM2, CH1
timer10 = pyb.Timer(10, freq=10)
pwm1 = timer10.channel(1, pyb.Timer.PWM, pin=p)
pwm1.pulse_width_percent(20)

timer8 = pyb.Timer(8)
timer8.init(prescaler=1, period=1000, mode=pyb.Timer.UP)
enc8 = timer8.channel(1, mode=pyb.Timer.ENC_A,pin=pyb.Pin.board.Y1)

while (1):
    pyb.delay(10)
    print(timer8.counter())