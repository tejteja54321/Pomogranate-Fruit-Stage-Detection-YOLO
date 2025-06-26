#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <SoftwareSerial.h>
#define SCREEN_WIDTH 128  // OLED display width,  in pixels
#define SCREEN_HEIGHT 64  // OLED display height, in pixels

// declare an SSD1306 display object connected to I2C
Adafruit_SSD1306 oled(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
//SoftwareSerial Serial(1, 0);

const int buzz = 16;
String command;

#define m1 15
#define m2 14
#define m3 13
#define m4 12
#define m5 17
#define m6 18
#define m7 19
#define m8 22
#define mode 16
#define pump 11

int modeState = 1;

void setup() {
  Serial.begin(9600);
  Serial2.begin(9600);
  // initialize OLED display with address 0x3C for 128x64
  if (!oled.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    // Serial.println(F("SSD1306 allocation failed"));
    while (true)
      ;
  }
  pinMode(mode, INPUT);
  pinMode(m1, OUTPUT);
  pinMode(m2, OUTPUT);
  pinMode(m3, OUTPUT);
  pinMode(m4, OUTPUT);
  pinMode(m5, OUTPUT);
  pinMode(m6, OUTPUT);
  pinMode(m7, OUTPUT);
  pinMode(m8, OUTPUT);
  pinMode(pump, OUTPUT);


  digitalWrite(m1, LOW);
  digitalWrite(m2, LOW);
  // wait for initializing
  oled.clearDisplay();          // clear display
  oled.setTextSize(1);          // text size
  oled.setTextColor(WHITE);     // text color
  oled.setCursor(0, 0);         // position to display
  oled.println("Smart robot");  // text to display
  oled.display();
  delay(2000);
}

void loop() {
  modeState = digitalRead(mode);
  if (modeState == LOW) {
    oled.clearDisplay();                  // clear display
    oled.setTextSize(1);                  // text size
    oled.setTextColor(WHITE);             // text color
    oled.setCursor(0, 0);                 // position to display
    oled.println("Waiting for Input :");  // text to display
    oled.display();

    while (Serial2.available()) {
      // Serial.write(SerialBT.read());
      command = "";
      command = Serial2.readString();
      oled.clearDisplay();           // clear display
      oled.setTextSize(1);           // text size
      oled.setTextColor(WHITE);      // text color
      oled.setCursor(30, 0);         // position to display
      oled.println("INSTRUCION :");  // text to display
      oled.setTextSize(1);           // text size
      oled.setTextColor(WHITE);      // text color
      oled.setCursor(20, 20);
      oled.println(command);
      oled.display();
      if (command == "*forward#") {
        delay(500);
        moveForward();
        oled.setCursor(0, 30);
        oled.setTextSize(1);
        oled.setTextColor(WHITE);
        // Display static text
        oled.println("FORWARD");
        oled.display();
        delay(500);
      } else if (command == "*backward#") {
        moveBackward();
        oled.setCursor(0, 30);
        oled.setTextSize(1);
        oled.setTextColor(WHITE);
        // Display static text
        oled.println("Backward");
        oled.display();
        delay(500);
      } else if (command == "*left#") {
        turnLeft();
        oled.setCursor(0, 30);
        oled.setTextSize(1);
        oled.setTextColor(WHITE);
        // Display static text
        oled.println("Left");
        oled.display();
        delay(500);
      } else if (command == "*right#") {
        turnRight();
        oled.setCursor(0, 30);
        oled.setTextSize(1);
        oled.setTextColor(WHITE);
        // Display static text
        oled.println("Right");
        oled.display();
        delay(500);
      } else if (command == "*pick#") {
        pickMotors();
        oled.setCursor(0, 30);
        oled.setTextSize(1);
        oled.setTextColor(WHITE);
        // Display static text
        oled.println("pick");
        oled.display();
        delay(500);
      } else if (command == "*release#") {
        releseMotors();
        oled.setCursor(0, 30);
        oled.setTextSize(1);
        oled.setTextColor(WHITE);
        // Display static text
        oled.println("release");
        oled.display();
        delay(500);
      } else if (command == "*up#") {
        upMotors();
        oled.setCursor(0, 30);
        oled.setTextSize(1);
        oled.setTextColor(WHITE);
        oled.println("arm up");
        oled.display();
        delay(500);
      } else if (command == "*down#") {
        downMotors();
        oled.setCursor(0, 30);
        oled.setTextSize(1);
        oled.setTextColor(WHITE);
        // Display static text
        oled.println("arm down");
        oled.display();
        delay(500);
      } else if (command == "*sprinkle on#") {
        pumpMotors();
        oled.setCursor(0, 30);
        oled.setTextSize(1);
        oled.setTextColor(WHITE);
        // Display static text
        oled.println("Sprinkler");
        oled.display();
        delay(500);
      } else if (command == "*sprinkle off#") {
        stopMotors();
        oled.setCursor(0, 30);
        oled.setTextSize(1);
        oled.setTextColor(WHITE);
        oled.println("Sprinkler");
        oled.display();
        delay(500);
      }
    }
  } else {
    oled.clearDisplay();                   // clear display
    oled.setTextSize(1);                   // text size
    oled.setTextColor(WHITE);              // text color
    oled.setCursor(0, 0);                  // position to display
    oled.println("Waiting for Python :");  // text to display
    oled.display();
    digitalWrite(m1, HIGH);
    digitalWrite(m2, LOW);
    digitalWrite(m3, HIGH);
    digitalWrite(m4, LOW);
    while (Serial.available() > 0) {
      char serialInput = Serial.read();
      // lastCommand = serialInput;
      oled.setCursor(0, 50);
      oled.print("Input from PC:");
      oled.print(serialInput);
      if (serialInput == '2') {
        oled.clearDisplay();
        oled.setCursor(0, 0);
        oled.println("SPRAY ON..!");
        oled.display();
        digitalWrite(m1, LOW);
        digitalWrite(m3, LOW);
        digitalWrite(m2, LOW);
        digitalWrite(m4, LOW);
        digitalWrite(pump, HIGH);
        delay(1000);
        digitalWrite(pump, LOW);
      }
      if (serialInput == '4') {
        
        oled.clearDisplay();
        oled.setCursor(0, 0);
        oled.println("POMAGRANATE DETECTED..!");
        oled.display();
        digitalWrite(m1, LOW);
        digitalWrite(m2, LOW);
        digitalWrite(m3, LOW);
        digitalWrite(m4, LOW);
        delay(200);
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
        digitalWrite(pump, LOW);
      }
      if (serialInput == '5') {
        oled.clearDisplay();
        oled.setCursor(0, 0);
        oled.println("POMAGRANATE DETECTED..!");
        oled.display();
        digitalWrite(m1, LOW);
        digitalWrite(m2, LOW);
        digitalWrite(m3, LOW);
        digitalWrite(m4, LOW);
        delay(200);
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
      }
      delay(1000);  // Delay before the next loop iteration
    }
  }
}
void moveForward() {
  digitalWrite(m1, HIGH);
  digitalWrite(m2, LOW);
  digitalWrite(m3, HIGH);
  digitalWrite(m4, LOW);
}

void moveBackward() {
  digitalWrite(m1, LOW);
  digitalWrite(m2, HIGH);
  digitalWrite(m3, LOW);
  digitalWrite(m4, HIGH);
}

void turnLeft() {
  digitalWrite(m1, LOW);
  digitalWrite(m2, HIGH);
  digitalWrite(m3, HIGH);
  digitalWrite(m4, LOW);
}

void turnRight() {
  digitalWrite(m1, HIGH);
  digitalWrite(m2, LOW);
  digitalWrite(m3, LOW);
  digitalWrite(m4, HIGH);
}

void stopMotors() {
  digitalWrite(m1, LOW);
  digitalWrite(m2, LOW);
  digitalWrite(m3, LOW);
  digitalWrite(m4, LOW);
}
void pickMotors() {
  digitalWrite(m7, HIGH);
  digitalWrite(m8, LOW);
  delay(500);
  digitalWrite(m7, LOW);
  digitalWrite(m8, LOW);
}
void releseMotors() {
  digitalWrite(m7, LOW);
  digitalWrite(m8, HIGH);
  delay(500);
  digitalWrite(m7, LOW);
  digitalWrite(m8, LOW);
}
void upMotors() {
  digitalWrite(m5, HIGH);
  digitalWrite(m6, LOW);
  delay(500);
  digitalWrite(m5, LOW);
  digitalWrite(m6, LOW);
}
void downMotors() {
  digitalWrite(m5, LOW);
  digitalWrite(m6, HIGH);
  delay(500);
  digitalWrite(m5, LOW);
  digitalWrite(m6, LOW);
}
void pumpMotors() {
  digitalWrite(pump, HIGH);
  delay(1000);
  digitalWrite(pump, LOW);
}