
//This is arduino's code not esp32 

int x_Pin = A4;
int y_Pin = A5;
int LEDpin  = 9;

int x_pos = 0 ;
int y_pos = 0 ;
int val = 0;

void setup()
{
  pinMode(LEDpin, OUTPUT);
  Serial.begin(9600);
}
void loop()
{
  noTone(LEDpin);

  x_pos = analogRead(x_Pin);
  y_pos = analogRead(y_Pin);
  //Serial.print(x_pos);
  //Serial.print("\t");
  //Serial.println(y_pos);


  //right
  if (x_pos > 500 && y_pos > 200 && y_pos < 500) {
    tone(LEDpin, 391);
    Serial.print(4);
  }

  //under
  if (x_pos < 400 && x_pos > 200 && y_pos > 500) {
    tone(LEDpin, 440);
    Serial.print(5);
  }

  //left
  if (x_pos < 100 && y_pos < 500 && y_pos > 200) {
    tone(LEDpin, 493);
    Serial.print(6);
  }

  //up
  if (x_pos < 500 && x_pos > 200 && y_pos < 100) {
    tone(LEDpin, 523);
    Serial.print(7);

  }

  delay(100);

}
