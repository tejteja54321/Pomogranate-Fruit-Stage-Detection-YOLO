#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// OLED Setup
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_ADDR 0x3C
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);


String serialInput = "";
char lastCommand = '0';

// TCS230 Pin Mapping for ESP32 (Modified)
#define S0 32         // GPIO32
#define S1 33         // GPIO33
#define S2 25         // GPIO25
#define S3 26         // GPIO26
#define sensorOut 27  // GPIO27
#define m1 14
#define m2 12
#define m3 13
#define m4 4
#define m5 19
#define m6 18
#define m7 2
#define m8 15

#define pump 17
unsigned int redFreq = 0, greenFreq = 0, blueFreq = 0;

void setup() {
  Serial.begin(9600);
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("OLED init failed!"));
    while (true); // Halt if OLED fails
  }
  // TCS230 Pins Configuration
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  pinMode(sensorOut, INPUT);
  pinMode(m1, OUTPUT);
  pinMode(m2, OUTPUT);
  pinMode(m3, OUTPUT);
  pinMode(m4, OUTPUT);
  pinMode(m5, OUTPUT);
  pinMode(m6, OUTPUT);
  pinMode(m7, OUTPUT);
  pinMode(m8, OUTPUT);
  pinMode(pump, OUTPUT);
  // Set frequency scaling to 20%
  digitalWrite(S0, HIGH);
  digitalWrite(m1, LOW);
  digitalWrite(m2, LOW);
  digitalWrite(m3, LOW);
  digitalWrite(m4, LOW);
  digitalWrite(m5, LOW);
  digitalWrite(m6, LOW);
  digitalWrite(m7, LOW);
  digitalWrite(m8, LOW);
  // Initial OLED message
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(WHITE);
  display.setCursor(0, 0);
  display.println("TEJA!!!!!!");
  display.display();

  Serial.println("ESP8266 Ready 🚀");
  
}
void showOnOLED(String message) {
  display.clearDisplay();
  display.setTextSize(2);
  display.setCursor(0, 0);
  display.println(message);
  display.display();
}
unsigned int getColorFreq(uint8_t s2_val, uint8_t s3_val) {
  digitalWrite(S2, s2_val);
  digitalWrite(S3, s3_val);
  delay(50);
  unsigned long sum = 0;
  for (int i = 0; i < 10; i++) {
    sum += pulseIn(sensorOut, LOW);
  }
  return sum / 10;
}

String detectColor(unsigned int r, unsigned int g, unsigned int b) {
  float total = r + g + b;
  float rRatio = r / total;
  float gRatio = g / total;
  float bRatio = b / total;

  Serial.print("R%: ");
  Serial.print(rRatio * 100, 1);
  Serial.print(" G%: ");
  Serial.print(gRatio * 100, 1);
  Serial.print(" B%: ");
  Serial.println(bRatio * 100, 1);

  // 🍎 Pomegranate Detection
  if (rRatio > 0.55 && gRatio < 0.3 && bRatio < 0.3 && r < 50) {
    return "🍎 POMEGRANATE";
  } else if (gRatio > 0.5) {
    return "🌿 GREEN";
  } else if (bRatio > 0.5) {
    return "🔵 BLUE";
  } else if (rRatio > 0.45 && gRatio > 0.35) {
    return "🟠 ORANGE/BROWN";
  }

  return "🤷 UNKNOWN";
}

void loop() {
  
  if (Serial.available() > 0) {
    char received = Serial.read();

    if (received == '\n' || received == '\r') return;

    Serial.print("📩 Received: ");
    Serial.println(received);

    // Check for Pomegranate Color and Show on OLED
    if (received == '1') {
      digitalWrite(pump, LOW);
      showOnOLED("💧 SPRAYING...");
      digitalWrite(m1, LOW);
      digitalWrite(m3, LOW);
      digitalWrite(m2, LOW);
      digitalWrite(m4, LOW);
      delay(1000);
      delay(2000);  // Wait before detecting again
      digitalWrite(pump, HIGH);
    }
    else if (received  == '5') {
      digitalWrite(m7, HIGH);
      digitalWrite(m8, LOW);
      delay(1400);
      digitalWrite(m7, LOW);
      digitalWrite(m8, LOW);
      delay(1300);
      digitalWrite(m5, HIGH);
      digitalWrite(m6, LOW);
      delay(500);
      digitalWrite(m5, LOW);
      digitalWrite(m6, LOW);
      delay(500);
      digitalWrite(m5, LOW);
      digitalWrite(m6, HIGH);
      delay(500);
      digitalWrite(m5, LOW);
      digitalWrite(m6, LOW);
      delay(500);
      digitalWrite(m7, LOW);
      digitalWrite(m8, HIGH);
      delay(1400);
      digitalWrite(m7, LOW);
      digitalWrite(m8, LOW);
      delay(500);
      showOnOLED("🍎 detected...");
      delay(100);
      showOnOLED("🍎 PLUCKING...");
      delay(2000);  // Wait before detecting again
      digitalWrite(pump, LOW);
    }

    else if (received == '4') {
     showOnOLED("🍎 Early FRUIT...");
      delay(2000);  // Wait
    }
    else {
      showOnOLED("❓ UNKNOWN CMD: " + String(received));
    }
  }
  delay(1000);  // Delay before the next loop iteration
}