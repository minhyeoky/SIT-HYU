#include "BluetoothSerial.h"
BluetoothSerial SerialBT;
int incomingByte = 0;   // 受信するシリアルデータのために準備


void setup() {
  Serial.begin(9600);     // シリアルポートを開き，データレートを9600 bpsにセットする
  SerialBT.begin("ESP32a_4to7");
}

void loop() {

  // データを受信した場合にのみ，データを送信する
  if (Serial.available() > 0) {
    // 受信したデータの1バイトを読み取る
    incomingByte = Serial.read();
    if (incomingByte == 52) { //0
      SerialBT.print(4);
      Serial.println(incomingByte);
    }
    if (incomingByte == 53) { //1
      SerialBT.print(5);
      Serial.println(incomingByte);
    }
    if (incomingByte == 54) { //2
      SerialBT.print(6);
      Serial.println(incomingByte);
    }
    if (incomingByte == 55) { //3
      SerialBT.print(7);
      Serial.println(incomingByte);
    }
    // 受信したデータを出力する
   Serial.print("I received: ");
    Serial.println(incomingByte, DEC);

  }
}
