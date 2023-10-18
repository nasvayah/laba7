import RPi.GPIO as gpio
import time
import matplotlib.pyplot as plt

gpio.setmode(gpio.BCM) 
dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13
led = [2, 3, 4, 17, 27, 22, 10, 9]
c = 0
gpio.setup(dac, gpio.OUT)
gpio.setup(troyka, gpio.OUT, initial = gpio.HIGH) 
gpio.setup(comp, gpio.IN)
gpio.setup(led, gpio.OUT)

def binbin(x):
    return[int(element) for element in bin(x)[2:].zfill(8)]
def adc(x):
    return x*3.3/2**8

def voltage():
    for i in range(256):
        binarr = binbin(i)
        gpio.output(dac,binarr)
        time.sleep(0.001)
        value = gpio.input(comp)
        if value == 1:
            return adc(i)

def ledss(x):
    gpio.output(led,binbin(x))
try:
    start = time.time()
    u = 0.0
    data = []
    data2 = []
    gpio.output(troyka, 1)
    while u<2.24:
        c+=1
        u = voltage()
        data2.append(u)
        print(u)
    gpio.output(troyka,0)
    while voltage()>0.3:
        c+=1
        u = voltage()
        data2.append(u)
        print(u)

    finish = time.time()
    time_all = finish - start     

    with open('/home/b03-301/Paramonova/data.txt', 'w') as f:
        for i in data2:
            f.write(str(i) + '\n')
    with open('settings.txt', 'w') as f:
        f.write('частота дискретизации: ' + str(c / time_all) + '\n')
        f.write('шаг квантования: ' + str(3.3 / 256) + '\n')
    plt.plot(data2)
    plt.xlabel('time')
    plt.ylabel('voltage')
    plt.show()


    print('Время эксперимента: ', time_all, ', период: ', time_all / c,', частота: ', round(c / time_all, 4), ', шаг квантования: ', round(2.24 / 256, 4), sep='')

finally:
    gpio.output(dac, 0)
    gpio.cleanup()

