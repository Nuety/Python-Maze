// Adafruit_NeoMatrix example for tiled NeoPixel matrices.  Scrolls
// 'Howdy' across three 10x8 NeoPixel grids that were created using
// NeoPixel 60 LEDs per meter flex strip.

#include <Adafruit_GFX.h>
#include <Adafruit_NeoMatrix.h>
#include <Adafruit_NeoPixel.h>
#ifndef PSTR
 #define PSTR // Make Arduino Due happy
#endif

#define PIN 1

Adafruit_NeoMatrix matrix = Adafruit_NeoMatrix(16, 16, PIN,
  NEO_MATRIX_TOP     + NEO_MATRIX_LEFT +
  NEO_MATRIX_COLUMNS + NEO_MATRIX_ZIGZAG,
  NEO_GRB            + NEO_KHZ800);

void setup() {
  //Serial setup
  Serial.begin(460800);
  Serial.setTimeout(1);

//Neomatrix setup
  matrix.begin();
  matrix.setBrightness(124);
}

String pyline;
int  x, y, r, g, b;

String readLine(){
  String s;
  s = "";
  while (1) {
    while(!Serial.available());
    char c = Serial.read();
    if (c < ' ') {
      break;
    }
    s += c;
  }
  return s;
}

void loop() {
  if (Serial.available());
  pyline = readLine();

  if (pyline == "CLEAR") {
    Serial.println(pyline);
    matrix.clear();
  }

  if (pyline == "PRINT") {
    Serial.println(pyline);
    matrix.show();
  }

  if (pyline.substring(0, 3) == "SET") {
    x = pyline.substring(4, 7).toInt();
    y = pyline.substring(8, 11).toInt();
    r = pyline.substring(12, 15).toInt();
    g = pyline.substring(16, 19).toInt();
    b = pyline.substring(20, 23).toInt();
    matrix.drawPixel(x, y, matrix.Color(r, g, b));
    Serial.println(pyline);
  }

}
