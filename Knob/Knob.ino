#include <Servo.h>
#include "Arduino.h"

// Pin assignments for servo motors
const int servo1 = 4;
const int servo2 = 5;
const int servo3 = 6;
const int servo4 = 7;
const int servo5 = 8;
const int servo6 = 9;

// Servo motor objects for Braille dots
Servo dotServo1;
Servo dotServo2;
Servo dotServo3;
Servo dotServo4;
Servo dotServo5;
Servo dotServo6;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);

  // Attach servo motors to corresponding pins
  dotServo1.attach(servo1);
  dotServo1.write(30);

  dotServo2.attach(servo2);
  dotServo2.write(0);

  dotServo3.attach(servo3);
  dotServo3.write(20);

  dotServo4.attach(servo4);
  dotServo4.write(0);

  dotServo5.attach(servo5);
  dotServo5.write(30);


  dotServo6.attach(servo6);
  dotServo6.write(85);


  // Display setup message
  Serial.println("BrailleBot Ready! Write a letter in the serial monitor to see it demonstrated.");
}

void loop() {
  if (Serial.available() > 0) {
    // Read the incoming letter from serial monitor
    char letter = Serial.read();

    // Convert the letter to uppercase
    letter = toupper(letter);

    // Check if the input is a valid alphabet character (A-Z)
    if (letter >= 'A' && letter <= 'Z') {
      // Display the letter being demonstrated
      Serial.print("Demonstrating letter: ");
      Serial.println(letter);

      // Demonstrate the Braille pattern for the input letter
      demonstrateLetter(letter);
    } else {
      // If the input is not a valid alphabet character, notify the user
      Serial.println("Invalid input! Please enter a letter from A to Z.");
    }
  }
}

// Function to demonstrate the Braille pattern for a given letter
void demonstrateLetter(char letter) {
  // Define Braille patterns for each letter (A-Z)
  const char *braillePatterns[26] = {
    "100000",
    "101000",
    "110000",
    "110100",
    "100100",
    "111000",
    "111100",
    "101100",
    "011000",
    "011100",
    "100010",
    "101010",
    "110010",
    "110110",
    "100110",
    "111010",
    "111110",
    "101110",
    "011010",
    "011110",
    "100011",
    "101011",
    "011101",
    "110011",
    "110111",
    "100111"
  };

  // Get the index of the input letter in the alphabet
  int index = letter - 'A';

  // Display the Braille pattern for the input letter
  Serial.println(braillePatterns[index]);

  // Demonstrate the Braille pattern using servo motors
  for (int i = 0; i < 6; i++) {
    // Check if the corresponding Braille dot should be raised or lowered
    if (braillePatterns[index][i] == '1') {
      raiseDot(i + 1);
    } else {
      lowerDot(i + 1);
    }
  }

  // Delay to hold the Braille pattern for demonstration
  delay(2000);

  // Clear the Braille pattern after demonstration
  clearDots();

  // Add a short delay to separate letters
  delay(500);  // 500ms delay after clearing dots
}

// Function to raise a specific Braille dot
void raiseDot(int dot) {
  switch (dot) {
    case 1:
      dotServo1.write(15);
      break;
    case 2:
      dotServo2.write(20);
      break;
    case 3:
      dotServo3.write(0);
      break;
    case 4:
      dotServo4.write(20);
      break;
    case 5:
      dotServo5.write(10);
      break;
    case 6:
      dotServo6.write(95);
      break;
    default:
      break;
  }
}

// Function to lower a specific Braille dot
void lowerDot(int dot) {
  switch (dot) {
    case 1:
      dotServo1.write(30);
      break;
    case 2:
      dotServo2.write(0);
      break;
    case 3:
      dotServo3.write(20);
      break;
    case 4:
      dotServo4.write(0);
      break;
    case 5:
      dotServo5.write(30);
      break;
    case 6:
      dotServo6.write(80);
      break;
    default:
      break;
  }
}

// Function to clear all Braille dots
void clearDots() {
  for (int i = 1; i <= 6; i++) {
    lowerDot(i);
  }
}
void dot1Up() {
  for (int pos = 30; pos <= 0; pos--) {
    dotServo1.write(pos);

    delay(10);
  }
}
void dot1Down() {
  for (int pos = 0; pos >= 30; pos++) {
    dotServo1.write(pos);
    delay(5);
  }
}

void dot2Up() {
  for (int pos = 0; pos <= 20; pos++) {
    dotServo2.write(pos);
    delay(5);
  }
}
void dot2Down() {
  for (int pos = 20; pos >= 0; pos--) {
    dotServo2.write(pos);
    delay(5);
  }
}

void dot3Up() {
  for (int pos = 180; pos >= 165; pos--) {
    dotServo3.write(pos);
    delay(5);
  }
}
void dot3Down() {
  for (int pos = 165; pos <= 180; pos++) {
    dotServo3.write(pos);
    delay(5);
  }
}

void dot4Up() {
  for (int pos = 0; pos <= 16; pos++) {
    dotServo4.write(pos);
    delay(5);
  }
}
void dot4Down() {
  for (int pos = 16; pos >= 0; pos--) {
    dotServo4.write(pos);
    delay(5);
  }
}

void dot5Up() {
  for (int pos = 180; pos >= 160; pos--) {
    dotServo5.write(pos);
    delay(5);
  }
}
void dot5Down() {
  for (int pos = 160; pos <= 180; pos++) {
    dotServo5.write(pos);
    delay(5);
  }
}

void dot6Up() {
  for (int pos = 0; pos <= 10; pos++) {
    dotServo6.write(pos);
    delay(5);
  }
}
void dot6Down() {
  for (int pos = 10; pos >= 0; pos--) {
    dotServo6.write(pos);
    delay(5);
  }
}
