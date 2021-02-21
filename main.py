# main.py -- put your code here!
import pyb
import stm
import math

encoder_value = 0.0

polling_flag = 0


def release_signal(timer):
    global polling_flag
    polling_flag = 1


def get_counter(Tim):
    count = Tim.counter()
    Tim.counter(500)
    return count - 500


def set_pwm(M1_A_Value, M1_B_Value, M2_A_Value, M2_B_Value):
    M1_A.pulse_width(M1_A_Value)
    M1_B.pulse_width(M1_B_Value)
    M2_A.pulse_width(M2_A_Value)
    M2_B.pulse_width(M2_B_Value)


def sw_callback():
    global speed
    if ((speed+10) == 50):
        speed = -40
    else:
        speed = speed + 10


EncoderM1 = pyb.Timer(8)
EncoderM1.init(prescaler=1, period=1000, mode=pyb.Timer.UP)
#print(stm.mem16[stm.TIM8 + stm.TIM_CR1])
EncoderM1.channel(1, mode=pyb.Timer.ENC_AB, pin=pyb.Pin.board.Y1)
EncoderM1.channel(2, mode=pyb.Timer.ENC_AB, pin=pyb.Pin.board.Y2)
EncoderM1.counter(500)
#print(stm.mem16[stm.TIM8 + stm.TIM_SMCR])

#M_timer = pyb.Timer(2, freq=1000)
M_timer = pyb.Timer(2)
M_timer.init(prescaler=11, period=6999)
print(stm.mem32[stm.TIM2 + stm.TIM_ARR])
M1_A = M_timer.channel(1, pyb.Timer.PWM, pin=pyb.Pin.board.X1)
M1_B = M_timer.channel(2, pyb.Timer.PWM, pin=pyb.Pin.board.X2)
M2_A = M_timer.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.X3)
M2_B = M_timer.channel(4, pyb.Timer.PWM, pin=pyb.Pin.board.X4)

timer10 = pyb.Timer(10, freq=100)
timer10.callback(release_signal)

sw = pyb.Switch()
sw.callback(sw_callback)

'''
Velocity_Kp = 50
Velocity_Ki = 10
Velocity_Kd = 0
'''
Velocity_Kp = -5
Velocity_Ki = -0.001
Velocity_Kd = 5
bias_Integral = 0
bias = 0
last_bias = 0
pwm_ValueA = 0
pwm_ValueB = 0
speed = 10

while (1):
    if (polling_flag):
        polling_flag = 0
        bias = get_counter(EncoderM1)
        print("bias=",bias)
        print("speed=",speed)
        error = bias - speed
        bias_Integral = bias_Integral + error
        if (bias_Integral > 15000):
            bias_Integral = 15000
        if (bias_Integral < -15000):
            bias_Integral = -15000
        pwm_ValueA = pwm_ValueA + (Velocity_Kp*error + Velocity_Ki *
                    bias_Integral + (error-last_bias)*Velocity_Kd)
        pwm_ValueB = pwm_ValueB - (Velocity_Kp*error + Velocity_Ki *
                    bias_Integral + (error-last_bias)*Velocity_Kd)
        if (pwm_ValueA < 0):    pwm_ValueA = 0
        if (pwm_ValueA > 6999): pwm_ValueA = 6999
        if (pwm_ValueB < 0):    pwm_ValueB = 0
        if (pwm_ValueB > 6999): pwm_ValueB = 6999
        last_bias = error
        set_pwm(int(pwm_ValueA), int(pwm_ValueB), 0, 0)
        #print(stm.mem32[stm.TIM2 + stm.TIM_CCR4])
        print("bias_Integral=", bias_Integral)
        print("valueA_pre=", stm.mem32[stm.TIM2 + stm.TIM_CCR1]/70, "%")
        print("valueB_pre=", stm.mem32[stm.TIM2 + stm.TIM_CCR2]/70, "%")
        

'''
        bias = get_counter(EncoderM1) - 5
        print("bias=",bias+15)
        last_bias = last_bias*0.4 + bias*0.6
        bias_Integral = bias_Integral + last_bias
        if (bias_Integral > 15000):
            bias_Integral = 15000
        if (bias_Integral < -15000):
            bias_Integral = -15000
        pwm_percent = (Velocity_Kp*last_bias + Velocity_Ki*bias_Integral)/100
        if (math.fabs(pwm_percent) > 100):
            pwm_percent = 100
        set_pwm(math.fabs(pwm_percent),0,0,0)
        print("bias_Integral=",bias_Integral)
        print("pwm_percent=",pwm_percent)
'''
