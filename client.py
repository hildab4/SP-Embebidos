# subscribe to mqtt topic and save to wav file

import paho.mqtt.client as mqtt

import matplotlib.pyplot as plt
import time
import numpy as np
import matplotlib.animation as animation
from plot_data import DataPlot, RealtimePlot

from numpy import pi, cos, sin, convolve
from scipy.fftpack import fft, ifft, fftshift
from scipy.signal import butter, sosfiltfilt


SAMPLES = 10000

start = time.time()
count = 0
MINY = 100
MAXY = 130

x = np.arange(0, SAMPLES, 1)

y = [0]*SAMPLES

"""fig_signal = plt.figure()
ax_signal = fig_signal.add_subplot(1, 1, 1)
signal,= ax_signal.plot(x,y)"""

fig_fft = plt.figure()
ax_fft = fig_fft.add_subplot(1, 1, 1)
signal_fft,= ax_fft.plot(x,y, 'b')

#ax_signal.set_xlim([0,SAMPLES])



def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("esp32/Mic")

maxi = 0


pos = 0

def graph(y):
    topy = max([MAXY, max(y)])
    boty = min([MINY, min(y)])

    #ax_signal.set_ylim([boty,topy])

    ###signal.set_ydata(y)

    n = np.arange(SAMPLES)

    ham = 0.54-0.46*cos(2*pi*n/SAMPLES)

    y_ham = ham*y*8

    Y = fft(y_ham)


    
    

    signal_fft.set_ydata(fftshift(abs(Y)))
    signal_fft.set_xdata(np.arange(-len(Y)//2,len(Y)//2))

    ax_fft.set_ylim([0,300])
    ax_fft.set_xlim([-len(Y)//2,len(Y)//2])
    
    plt.draw()
    plt.pause(0.01)
        
        

def on_message(client, userdata, msg):
    global pos
    global start
    global y

    payload = int.from_bytes(msg.payload, byteorder="little")
    y[pos] = payload
    pos+=1

    if(pos>=SAMPLES):
        print(msg.payload, payload)
        graph(y)
        pos = 0
        
        

    

        




print("Connecting to MQTT broker")

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)


client.loop_forever()
