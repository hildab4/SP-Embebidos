# subscribe to mqtt topic and save to wav file

import paho.mqtt.client as mqtt
import wave


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("esp32/Mic")


payload = []


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    wf = wave.open('test.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(16000)

    payload.append(msg.payload)

    if len(payload) > 16000*5:
        wf.writeframes(b''.join(payload))
        wf.close()
        payload.clear()
        print("save to wav file")


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()
