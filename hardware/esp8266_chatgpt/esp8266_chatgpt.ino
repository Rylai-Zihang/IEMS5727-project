#include <ESP8266WiFi.h>
#include <Wire.h>
#include <WiFiUdp.h>

#define ESP8266I2CAddress 0x66

// String receivedMessage = "1";

const char* ssid = "group07";
const char* password =  "group007";

IPAddress remote_ip(192, 168, 8, 15);
unsigned int port = 8080;

WiFiUDP Udp;
unsigned int udpPort = 8080; // 本地端口号
char incomingPacket[537]; // 接收缓冲区

void setup() {
  Serial.begin(115200); 
  delay(10);
  Serial.println();
  Serial.printf("Connecting to %s ", ssid);

  WiFi.mode(WIFI_STA);
  WiFi.setAutoConnect(false);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected to WiFi");


  Udp.begin(udpPort); // 开启UDP监听并打印输出信息
  Serial.printf("Now listening at IP %s, UDP port %d\n", WiFi.localIP().toString().c_str(), udpPort);

  Wire.begin(2,0, ESP8266I2CAddress);
  Wire.setClock(100000);
  Serial.println("ESP8266 - I2C Communication Test");
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);
}

void loop() {

}


void receiveEvent(size_t howMany) {
  while (Wire.available() > 0) {
    char c = Wire.read();
    Serial.print(c);
    if (c == 'Y') {
      Serial.println(c);
      Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
      Udp.write("1");
      Udp.endPacket();
    } else if (c == 'T'){
      float temp;
      Wire.readBytes((char*)&temp, sizeof(float));
      Udp.beginPacket(remote_ip, port);
      Udp.write((const uint8_t *)&temp, sizeof(temp)); 
      Serial.println(temp);
      Udp.endPacket();

    }
  }
}

void requestEvent() {
    int packetSize = Udp.parsePacket();
    if (packetSize) {
      Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
      int len = Udp.read(incomingPacket, 536); //读取数据到imcomingPacket
      if (len > 0) //如果正确读取
      {
        incomingPacket[len] = 0; //末尾补0结束字符串
        Serial.printf("UDP packet contents: %s\n", incomingPacket);

        // if (strcmp(incomingPacket, "1") == 0) // 如果收到1
        if (incomingPacket[0] == '1')
        {
          Serial.println("Send nano '1'!");
          Wire.write("1");
        }
        else // 如果非指定信息
        {
          Wire.write("w");
        }
      }
    }
}

