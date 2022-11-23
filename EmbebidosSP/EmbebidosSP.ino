
#include <ESP8266WiFi.h>  //Whe using ESP8266
#include <PubSubClient.h>


// Wifi security
const char* ssid = "IOT";
const char* password = "IOT12345";

// MQTT Broker IP address
const char* mqtt_server = "192.168.50.167";
// const char* mqtt_server = "10.25.18.8";

WiFiClient espClient;
PubSubClient client(espClient);

long lastMsg = 0;
char msg[50];

float Dato_Enviar = 0;


// LED Pin
const int ledPin = 2;

void setup() {
  Serial.begin(115200);
  Serial.println("Starting");
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  pinMode(ledPin, OUTPUT);
}

void setup_wifi() {
  delay(10);
  // connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();


  // If topic = "casa", check message is either "Uno" or "Dos". 
  // Changes the output state according to the message
  if (String(topic) == "casa") {
    Serial.print("Changing output to ");
    if(messageTemp == "Uno"){
      Serial.println("Uno");
      digitalWrite(ledPin, HIGH);
    }
    else if(messageTemp == "Dos"){
      Serial.println("off");
      digitalWrite(ledPin, LOW);
    }  // PROCESS DATA
    else if(messageTemp.startsWith("PACKA")){
      Serial.println("PACKA RECEIVED");
      // Serial.println(messageTemp.length());
      // Serial.println(messageTemp);
    }  // PROCESS DATA
    else if(messageTemp.startsWith("PACKB")){
      Serial.println("PACKB RECEIVED");
      Serial.println(messageTemp.length());
      // Serial.println(messageTemp);
    }  // PROCESS DATA
    else if(messageTemp.startsWith("PACKC")){
      Serial.println("PACKC RECEIVED");
      Serial.println(messageTemp.length());
      Serial.println(messageTemp);
    }  // PROCESS DATA
    else { 
      Serial.println("DATA RECEIVED");
       Serial.println(messageTemp.length());
    }
  
  }
}

void reconnect() {
  // Reconnect
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP32Client_rojo")) { //"ESPClient_3" represent the client name that connects to broker
      Serial.println("connected");
      // Subscribe
      client.subscribe("casa");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  char tempString[8];
  dtostrf(analogRead(A0), 1, 2, tempString);
  client.publish("esp32/Mic", tempString);
}
