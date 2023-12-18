#include <Arduino.h>
#include "LM75.h"
#include <Wire.h>
// #include <Adafruit_SSD1306.h>
// #include <Adafruit_GFX.h>
#include "Buzzer.h"

#define ESP8266I2CAddress 0x66
#define SSD1306I2CAddress 0x3C

Buzzer buzzer(4, 3);
LM75 sensor(LM75_ADDRESS | 0b000);
#define TEMP_THRESHOLD 28 // 设置温度阈值为25摄氏度

// #define SCREEN_WIDTH 128
// #define SCREEN_HEIGHT 64
// #define OLED_RESET  -1
// Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup() {
  Serial.begin(115200);
  while (!Serial);

  Wire.begin();
  Wire.setClock(50);

  // if (!display.begin(SSD1306_SWITCHCAPVCC, SSD1306I2CAddress)){
  //   Serial.println(F("SSD1306 allocation failed"));
  //   for(;;);
  // } else {Serial.println("YES");}// 初始化OLED显示屏，地址可能需要根据模块调整
  
  // display.display();
  // delay(2000);
  // display.clearDisplay();
  // display.display();
  // display.setTextSize(1);
  // display.setTextColor(SSD1306_WHITE);
  Serial.println("Nano start running");
}

void loop() {

  float temperature = sensor.temp();

  // Wire.endTransmission();
  delay(2);
  // Wire.begin(ESP8266I2CAddress);

  if (temperature > TEMP_THRESHOLD) {
    Serial.println("1111");
    Serial.println("chaoguo 28");
  }
  sendTempToESP8266(temperature);
  Serial.println(temperature);

  // displayData(temperature); // 显示数据
  Wire.endTransmission();
  delay(10);
  // Request data from ESP8266
  requestDataFromESP8266();

  delay(1000);
}

// void displayData(float temperature) {
//   display.clearDisplay();
//   display.setTextSize(1);
//   display.setTextColor(WHITE);
//   display.setCursor(0, 0);
//   display.print("Temp: ");
//   display.print(temperature);
//   display.println(" C");
//   display.display();
//   Wire.endTransmission();
//   delay(2);
// }


void sendMessageToESP8266(char message) {
  Wire.beginTransmission(ESP8266I2CAddress); // Set the I2C address of the ESP8266
  Wire.write(message);
  Wire.endTransmission();
}

void sendTempToESP8266(float temperature) {
  Wire.beginTransmission(ESP8266I2CAddress);
  Wire.write('T');
  Wire.write((byte*)&temperature, sizeof(temperature));
  Wire.endTransmission();
}

void requestDataFromESP8266() {
  Wire.requestFrom(ESP8266I2CAddress, 1); // Request 6 bytes of data
  while (Wire.available()) {
    char c = Wire.read();
    Serial.print(c);
    if (c == '1') {
      Serial.println("aha");
      buzzer.begin(100);

      buzzer.sound(NOTE_E7, 80);
      buzzer.sound(NOTE_E7, 80);
      buzzer.sound(0, 80);
      buzzer.sound(NOTE_E7, 80);
      buzzer.sound(0, 80);
      buzzer.sound(NOTE_C7, 80);
      buzzer.sound(NOTE_E7, 80);
      buzzer.sound(0, 80);
      buzzer.sound(NOTE_G7, 80);
      buzzer.sound(0, 240);
      buzzer.sound(NOTE_G6, 80);
      buzzer.sound(0, 240);
      buzzer.sound(NOTE_C7, 80);
      buzzer.sound(0, 160);
      buzzer.sound(NOTE_G6, 80);
      buzzer.sound(0, 160);
      buzzer.sound(NOTE_E6, 80);
      buzzer.sound(0, 160);
      buzzer.sound(NOTE_A6, 80);
      buzzer.sound(0, 80);
      buzzer.sound(NOTE_B6, 80);
      buzzer.sound(0, 80);
      buzzer.sound(NOTE_AS6, 80);
      buzzer.sound(NOTE_A6, 80);
      buzzer.sound(0, 80);
      buzzer.sound(NOTE_G6, 100);
      buzzer.sound(NOTE_E7, 100);
      buzzer.sound(NOTE_G7, 100);
      buzzer.sound(NOTE_A7, 80);
      buzzer.sound(0, 80);
      buzzer.sound(NOTE_F7, 80);
      buzzer.sound(NOTE_G7, 80);
      buzzer.sound(0, 80);
      buzzer.sound(NOTE_E7, 80);
      buzzer.sound(0, 80);
      buzzer.sound(NOTE_C7, 80);
      buzzer.sound(NOTE_D7, 80);
      buzzer.sound(NOTE_B6, 80);
      buzzer.sound(0, 160);
      buzzer.sound(NOTE_C7, 80);
      buzzer.sound(0, 160);
      buzzer.sound(NOTE_G6, 80);
      buzzer.sound(0, 160);
      buzzer.sound(NOTE_E6, 80);
      buzzer.sound(0, 160);
      buzzer.sound(NOTE_A6, 80);
      buzzer.sound(0, 80);
      buzzer.sound(NOTE_B6, 80);
      buzzer.sound(0, 80);
      buzzer.sound(NOTE_AS6, 80);
      buzzer.sound(NOTE_A6, 80);
      buzzer.sound(0, 80);
      buzzer.sound(NOTE_G6, 100);
      buzzer.sound(NOTE_E7, 100);
      buzzer.sound(NOTE_G7, 100);
      buzzer.sound(NOTE_A7, 80);
      buzzer.sound(0, 80);
      buzzer.sound(NOTE_F7, 80);
      buzzer.sound(NOTE_G7, 80);
      buzzer.sound(0, 80);
      buzzer.sound(NOTE_E7, 80);
      buzzer.sound(0, 80);
      buzzer.sound(NOTE_C7, 80);
      buzzer.sound(NOTE_D7, 80);
      buzzer.sound(NOTE_B6, 80);
      buzzer.sound(0, 160);

      buzzer.end(2000);

    }
  }
  Wire.endTransmission();
  Serial.println();
}

