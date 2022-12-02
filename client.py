# subscribe to mqtt topic and save to wav file

import paho.mqtt.client as mqtt

import matplotlib.pyplot as plt
import time
import numpy as np
from numpy import pi, cos, sin, convolve
from scipy.fftpack import fft, ifft, fftshift
from scipy.signal import butter, sosfiltfilt

SAMPLES = 3500

start = time.time()
count = 0

x = np.arange(0, SAMPLES, 1)

y = [0]*SAMPLES

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)


def plot_fft(Y, colours=None, markersize=10):
    f, ax = plots()
    ax.plot(np.arange(-len(Y)//2, len(Y)//2), fftshift(abs(Y)), 'bo')
    plt.show()
    return f, ax


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("esp32/Mic")


def animate(i):
    ax = fig.add_subplot(1, 1, 1)
    ax.clear()
    ax.plot(y)


def on_message(client, userdata, msg):
    payload = msg.payload
    int_val = int.from_bytes(payload, byteorder='little')
    y.pop(0)
    y.append(int_val)

    # Scale x domain by a factor of 8


print("Connecting to MQTT broker")

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

ani = animation.FuncAnimation(fig, animate, interval=50)
