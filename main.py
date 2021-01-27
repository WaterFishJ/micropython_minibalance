# main.py -- put your code here!
import pyb, stm

def get_encoder_count(timer):
    print(timer8.counter())
    timer8.counter(0)
    

timer8 = pyb.Timer(8)
timer8.init(prescaler=1, period=1000, mode=pyb.Timer.UP)
print(stm.mem16[stm.TIM8 + stm.TIM_CR1])
timer8.channel(1, mode=pyb.Timer.ENC_AB,pin=pyb.Pin.board.Y1)
timer8.channel(2, mode=pyb.Timer.ENC_AB,pin=pyb.Pin.board.Y2)
print(stm.mem16[stm.TIM8 + stm.TIM_SMCR])

timer10 = pyb.Timer(10, freq=100)
timer10.callback(get_encoder_count)


while (1):
    pyb.delay(10)
    #print(timer8.counter())