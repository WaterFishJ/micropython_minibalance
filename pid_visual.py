import serial
portx="COM5"
bps=9600
timex=5
#串口执行到这已经打开 再用open命令会报错
ser = serial.Serial(portx, int(bps), timeout=1, parity=serial.PARITY_NONE,stopbits=1)

def serial_process():
    while (True):
        line = str(ser.readline())
        if ('bias=' in line):
            line = line.strip('b''bias=')
            print(line)
            print("next")
        

if (ser.isOpen()):
    print("open success")

while (True):
    serial_process()