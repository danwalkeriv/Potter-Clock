// Copyright 2011 Daniel Walker
// This is the "firmware" for the potter clock ambient location display
// Upload this sketch to the arduino and wire the LEDs to the pins as
// described here:
int redPin = 9;      // select the pin for the LED
int greenPin = 10;      // select the pin for the LED
int bluePin = 11;      // select the pin for the LED

byte msg = 0;        // variable to hold data from serial 
int current_color = 0;
int current_temp_color = 0;
char temp_pattern[100];
char pattern[100];
int mode = 0;

// Sets the brightness of all of the LEDs to 0
void clear() {
  analogWrite(redPin, 0);
  analogWrite(greenPin, 0);
  analogWrite(bluePin, 0);
}

// Set the intensity of the specified LED to the specified value
void write_pin(byte color, int value) {
  int ledPin = 0;
  if (color == 'R') {
    ledPin = redPin;
  } else if (color == 'G') {
    ledPin = greenPin;   
  } else if (color == 'B') {
    ledPin = bluePin;
  }
  analogWrite(ledPin, value);  // turn LED ON  
}

void setup() {
  pinMode(redPin, OUTPUT);      // declare LED as output  
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
  pattern[0] = 'E';
  pattern[1] = 0;
  Serial.begin(9600);
  Serial.write("System initialized\n");
  Serial.flush();
}

void loop() {
  // While data is sent over serial assign it to the msg  
  int ledPin = 0;
  int redValue = 0;
  int greenValue = 0;
  int blueValue = 0;
  while (Serial.available() > 0){
    // Look for a color to write
    msg=Serial.read();
    if (mode == 0) {
      if (msg == 'R'){
       mode = 1;
       Serial.write("Looking for value for Red LED\n");
      } else if (msg == 'G') {
        mode = 2;
        Serial.write("Looking for value for Green LED\n");
      } else if (msg == 'B') {
        mode = 3;
        Serial.write("Looking for value for Blue LED\n");
      } else {
        mode = 0;
      }     
    } else if (mode == 1) {
      redValue = msg;
      write_pin('R', redValue);
      Serial.write("Got value for Red LED\n");
      mode = 0;
    } else if (mode == 2) {
      greenValue = msg;
      write_pin('G', greenValue);
      Serial.write("Got value for Green LED\n");
      mode = 0;
    } else if (mode == 3) {
      blueValue = msg;
      write_pin('B', blueValue);
      Serial.write("Got value for Blue LED\n");
      mode = 0;
    } else {
      Serial.write("Got into a bad state somehow!\n");
      mode = 0;
    }
  }
}
