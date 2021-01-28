# main.py -- put your code here!
import pyb, stm

encoder_value = 0.0
bias = 0.0
last_bias = 0
polling_flag = 0

def release_signal(timer):
    global polling_flag
    polling_flag = 1

def set_pwm(M1_A_Percent, M1_B_Percent, M2_A_Percent, M2_B_Percent):
    M1_A.pulse_width_percent(M1_A_Percent)
    M1_B.pulse_width_percent(M1_B_Percent)
    M2_A.pulse_width_percent(M2_A_Percent)
    M2_B.pulse_width_percent(M2_B_Percent)
    

timer8 = pyb.Timer(8)
timer8.init(prescaler=1, period=1000, mode=pyb.Timer.UP)
print(stm.mem16[stm.TIM8 + stm.TIM_CR1])
timer8.channel(1, mode=pyb.Timer.ENC_AB,pin=pyb.Pin.board.Y1)
timer8.channel(2, mode=pyb.Timer.ENC_AB,pin=pyb.Pin.board.Y2)
print(stm.mem16[stm.TIM8 + stm.TIM_SMCR])

M_timer = pyb.Timer(2, freq=1000)
M1_A = M_timer.channel(1, pyb.Timer.PWM, pin=pyb.Pin.board.X1)
M1_B = M_timer.channel(2, pyb.Timer.PWM, pin=pyb.Pin.board.X2)
M2_A = M_timer.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.X3)
M2_B = M_timer.channel(4, pyb.Timer.PWM, pin=pyb.Pin.board.X4)

timer10 = pyb.Timer(10, freq=100)
timer10.callback(release_signal)


while (1):
    if (polling_flag):