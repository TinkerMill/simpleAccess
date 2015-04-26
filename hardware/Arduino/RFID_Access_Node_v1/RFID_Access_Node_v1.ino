/*
  LCD display to Pro Micro pin connections
  1 to GND
  2 to 5V
  3 to the center pin on the potentiometer
  4 to Arduino digital pin 7
  5 to GND
  6 to Arduino digital pin 6
  7 (no connection)
  8 (no connection)
  9 (no connection)
  10 (no connection)
  11 to Arduino digital pin 5
  12 to Arduino digital pin 4
  13 to Arduino digital pin 3
  14 to Arduino digital pin 2
  15 to 5V
  16 to GND
*/
#include <LiquidCrystal.h>
LiquidCrystal lcd(7, 6, 5, 4, 3, 2);

//setup and definitions for piezo buzzer songs
#include "pitches.h"
// notes in the melody:
int successMelody[] = {NOTE_B3, NOTE_B4, NOTE_B5, NOTE_B6};
// note durations: 4 = quarter note, 8 = eighth note, etc.:
int successNoteDurations[] = {7, 6, 7, 2};
int failMelody[] = {NOTE_C1, NOTE_D1, NOTE_C1, NOTE_G1, NOTE_C1};
int failNoteDurations[] = {8, 9, 8, 2, 1};

//setup for the WS2812 RGB LED
#include <Adafruit_NeoPixel.h>
#include "WS2812_Definitions.h"
#define PIN 10
#define LED_COUNT 1
Adafruit_NeoPixel leds = Adafruit_NeoPixel(LED_COUNT, PIN, NEO_GRB + NEO_KHZ800);

boolean tagRead = false;

char relayPin = 9;
char futureInput1Pin = A2;
char futureInput2Pin = A3;

String myString;

void setup() {
  pinMode(relayPin, OUTPUT);
  
  //lcd initialization
  lcd.begin(16, 2);
  lcd.clear();
  
  //setup serial communication. Serial is the USB, Serial1 is the micro's TX and RX pins
  Serial.begin(19200);
  Serial1.begin(9600);

  leds.begin();  // Call this to start up the WS2812 RGB LED.
  clearLEDs();   // This function, defined below, turns all LEDs off...
  setColor(DARKSLATEBLUE, 6); // Set the LED color to dark blue
  
  //Tinkermill and version number splash screen
  lcd.setCursor(3, 0);
  lcd.print("TINKERMILL");
  lcd.setCursor(2, 1);
  lcd.print("RFID Node v1");
  delay(1500);
  lcd.clear();
}

void loop() {  
  //when serial data is sent to the pro micro over the usb
  //it is stored in a string and then printed back out over the usb
  if (Serial.available() > 0) {
    myString = Serial.readString();
    Serial.println(myString);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(myString);
    delay(1500);
    lcd.clear();
  }
  
  //defualt screen while waiting for a tag scan
  lcd.setCursor(1, 0);
  lcd.print("READY TO SCAN");

  while (Serial1.available() > 0) {
    int readByte = Serial1.read();
    Serial.write(readByte);
    tagRead = true;
  }
  delay(500);
  if (tagRead) {
    readSuccess();
    tagRead = false;
  }
  setColor(DARKSLATEBLUE, 6);
}

void setColor(unsigned long color, byte brightness) {
  byte red = (color & 0xFF0000) >> 16;
  byte green = (color & 0x00FF00) >> 8;
  byte blue = (color & 0x0000FF);

  for (int i = 0; i <= LED_COUNT - 1; i++) {
    leds.setPixelColor(i, red / brightness, green / brightness, blue / brightness);
  }
  leds.show();  // Turn the LEDs on
}

// Sets all LEDs to off, but DOES NOT update the display;
// call leds.show() to actually turn them off after this.
void clearLEDs() {
  for (int i = 0; i < LED_COUNT; i++) {
    leds.setPixelColor(i, 0);
    leds.show();
  }
}

void readSuccess() {
  lcd.clear();
  lcd.setCursor(3, 0);
  lcd.print("CARD READ");
  lcd.setCursor(4, 1);
  lcd.print("SUCCESS");

  digitalWrite(relayPin, HIGH);

  setColor(GREEN, 6);

  for (int thisNote = 0; thisNote < 4; thisNote++) {
    // to calculate the note duration, take one second
    // divided by the note type.
    //e.g. quarter note = 1000 / 4, eighth note = 1000/8, etc.
    int noteDuration = 700 / successNoteDurations[thisNote];
    tone(8, successMelody[thisNote], noteDuration);
    // to distinguish the notes, set a minimum time between them.
    // the note's duration + 30% seems to work well:
    int pauseBetweenNotes = noteDuration * 1.30;
    delay(pauseBetweenNotes);
    // stop the tone playing:
    noTone(8);
  }

  delay(900);
  
  digitalWrite(relayPin, LOW);
  
  lcd.clear();
}

void failBeeps() {
  for (int thisNote = 0; thisNote < 5; thisNote++) {

    // to calculate the note duration, take one second
    // divided by the note type.
    //e.g. quarter note = 1000 / 4, eighth note = 1000/8, etc.
    int noteDuration = 1000 / failNoteDurations[thisNote];
    tone(8, failMelody[thisNote], noteDuration);

    // to distinguish the notes, set a minimum time between them.
    // the note's duration + 30% seems to work well:
    int pauseBetweenNotes = noteDuration * 1.30;
    delay(pauseBetweenNotes);
    // stop the tone playing:
    noTone(8);
  }
}
