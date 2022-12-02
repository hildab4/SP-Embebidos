
#include <ESP8266WiFi.h> //Whe using ESP8266
#include <PubSubClient.h>

#define MIC A0
#define SAMPLES 12500

// Wifi security
const char *ssid = "MotoEPC";
const char *password = "57142857";

// MQTT Broker IP address
const char *mqtt_server = "192.168.135.36";
// const char* mqtt_server = "10.25.18.8";

WiFiClient espClient;
PubSubClient client(espClient);

long start = 0;

unsigned int counter = 0;

// LED Pin
const int ledPin = 2;

uint16_t adc;
uint32_t payload;

uint8_t position = 0;
uint32_t messages[SAMPLES];

void setup()
{
  Serial.begin(9600);
  Serial.println("Starting");
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  start = millis();
}

void setup_wifi()
{
  delay(10);
  // connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect()
{
  // Reconnect
  while (!client.connected())
  {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP32Client_rojo"))
    { //"ESPClient_3" represent the client name that connects to broker
      Serial.println("connected");
    }
    else
    {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void loop()
{
  if (!client.connected())
  {
    reconnect();
  }
  client.loop();

  adc = analogRead(MIC);

  payload |= (adc & 0x3FF) << position * 10;

  if (counter == SAMPLES)
  {
    Serial.print("Reading: ");
    Serial.println((millis() - start) / 1000);
    start = millis();
    for (int i = 0; i < SAMPLES; i++)
    {
      client.publish("esp32/Mic", "test", 4);
    }

    Serial.print("Publishing: ");
    Serial.println((millis() - start) / 1000);
    start = millis();

    counter = 0;
  }

  if (position == 2)
  {
    messages[counter++] = payload;
    payload = 0;
    position = 0;
  }
  else
  {
    position++;
  }
}
