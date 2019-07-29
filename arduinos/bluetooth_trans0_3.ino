#include "BluetoothSerial.h"
BluetoothSerial SerialBT;
int incomingByte = 0;   // 受信するシリアルデータのために準備


void setup() {
  Serial.begin(9600);     // シリアルポートを開き，データレートを9600 bpsにセットする
  SerialBT.begin("ESP32a_2");
}

void loop() {

  // データを受信した場合にのみ，データを送信する
  if (Serial.available() > 0) {
    // 受信したデータの1バイトを読み取る
    incomingByte = Serial.read();
    if (incomingByte == 48) { //0
      SerialBT.print(0);
      Serial.println(incomingByte);
    }
    if (incomingByte == 49) { //1
      SerialBT.print(1);
      Serial.println(incomingByte);
    }
    if (incomingByte == 50) { //2
      SerialBT.print(2);
      Serial.println(incomingByte);
    }
    if (incomingByte == 51) { //3
      SerialBT.print(3);
      Serial.println(incomingByte);
    }
    // 受信したデータを出力する
   Serial.print("I received: ");
    Serial.println(incomingByte, DEC);

  }
}
