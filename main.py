import pyb

def get_encoder_count(timer):
    print(timer8.counter())
    timer8.counter(0)

timer8 = pyb.Timer(8)
timer8.init(prescaler=1, period=1000, mode=pyb.Timer.UP)
timer8.channel(1, mode=pyb.Timer.ENC_A,pin=pyb.Pin.board.Y1)

timer10 = pyb.Timer(10, freq=100)
timer10.callback(get_encoder_count)


while (1):
    pyb.delay(10)
    #print(timer8.counter())