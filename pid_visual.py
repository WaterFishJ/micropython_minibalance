import serial,array,threading,time
import pyqtgraph as pg
import numpy as np
from queue import Queue

portx="COM5"
bps=9600
timex=5
#串口执行到这已经打开 再用open命令会报错
ser = serial.Serial(portx, int(bps), timeout=1, parity=serial.PARITY_NONE,stopbits=1)

realtime_q = Queue(maxsize=0)
expect_q = Queue(maxsize=0)

def serial_process():
    bias = 0
    speed = 0
    while (True):
        n = ser.inWaiting()
        if(n):
            line = str(ser.readline())
            if ('bias=' in line):
                line = line.replace('b\'bias= ', '')
                line = line.replace('\\', '')
                line = line.replace('\'', '')
                line = line.replace('rn', '')
                bias = int(line)
                line = str(ser.readline())
                if ('speed=' in line):
                    line = line.replace('b\'speed= ', '')
                    line = line.replace('\\', '')
                    line = line.replace('\'', '')
                    line = line.replace('rn', '')
                    speed = int(line)
                realtime_q.put(bias)
                expect_q.put(speed)
                ser.flushInput()
                continue
            print(line)
                #print(realtime_q)
                #break

def plotData():
        if len(data_expect)<historyLength:
            data_expect.append(expect_q.get())
        else:
            data_expect[:-1] = data_expect[1:]
            data_expect[-1] = expect_q.get()

        if len(data_realtime)<historyLength:
            data_realtime.append(realtime_q.get())
        else:
            data_realtime[:-1] = data_realtime[1:]
            data_realtime[-1] = realtime_q.get()
        curve_realtime.setData(data_realtime)
        curve_expect.setData(data_expect)

if (ser.isOpen()):
    print("open success")

app = pg.mkQApp()#建立app
win = pg.GraphicsWindow()#建立窗口
win.setWindowTitle(u'PID')
win.resize(800, 500)#小窗口大小
p = win.addPlot()#把图p加入到窗口中
p.showGrid(x=True, y=True)#把X和Y的表格打开
p.setRange(xRange=[0,500], yRange=[-45, 45], padding=0)
p.setLabel(axis='left', text='y / Speed')#靠左
p.setLabel(axis='bottom', text='x / Point')
p.setTitle('PID:SPEED')#表格的名字
historyLength = 500
data_expect = array.array('d')
data_expect=np.zeros(historyLength).__array__('d')#把数组长度定下来
data_realtime = array.array('d')
data_realtime=np.zeros(historyLength).__array__('d')#把数组长度定下
curve_expect = p.plot()#绘制一个数据
curve_realtime = p.plot()#绘制一个数据
timer = pg.QtCore.QTimer()
timer.timeout.connect(plotData)#定时调用plotData函数
timer.start(5)#多少ms调用一次

th1 = threading.Thread(target=serial_process)
th1.start()

app.exec_()

while(1):
    time.sleep(0.05)
    #serial_process()
    #print(data_expect)