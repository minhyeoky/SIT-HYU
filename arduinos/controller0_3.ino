



#define C4 261.6
#define C#4 277.18
#define D4 293.665
#define D#4 311.127
#define E4 329.63
#define F4 349.228
#define F#4 369.994
#define G4 391.995
#define G#4 415.305
#define A4 440
#define A#4 466.164
#define B4 493.883
#define C5 523.251

const int LEDpin = 15;
const int x_pin = 25; 
const int y_pin = 26;

int pin_data = 0; 
int x_pos = 0; 
int y_pos = 0;
int test_pos = 0;


void setup() {
  pinMode(sw_pin, INPUT); 
  ledcSetup(1, 12000, 8);
  ledcAttachPin(LEDpin, 1);
  Serial.begin(9600); 

}

void loop() {

  x_pos = analogRead(x_pin); 
  y_pos = analogRead(y_pin); 


  ledcWriteTone(1, 0.0);
  //right
  if (x_pos > 3500 && y_pos > 1300 && y_pos < 2300) {
    ledcWriteTone(1, C4);
    digitalWrite(LEDpin, HIGH);
    Serial.print(0);
  }

  //below
  if (x_pos < 2300 && x_pos > 1300 && y_pos > 3500) {
    ledcWriteTone(1, D4);
    digitalWrite(LEDpin, HIGH);
    Serial.print(1);
  }

  //left
  if (x_pos < 500 && y_pos < 2300 && y_pos > 1300) {
    ledcWriteTone(1, E4);
    digitalWrite(LEDpin, HIGH);
    Serial.print(2);
  }

  //up
  if (x_pos < 2300 && x_pos > 1300 && y_pos < 500) {
    ledcWriteTone(1, F4);
    digitalWrite(LEDpin, HIGH);
    Serial.print(3);
    
  }


  delay(100);
}
