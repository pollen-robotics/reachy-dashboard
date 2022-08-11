#include <Adafruit_SSD1306.h>

#define pixelsWidth 128         // Width of the screen, in nb of pixels
#define pixelsHeight 64          // Height of the screen, in nb of pixels
#define pinResetOLED -1          // Screen reset pin
#define i2cAddress 0x3C        // i2c address of the screen

Adafruit_SSD1306 ecranOLED(pixelsWidth, pixelsHeight, &Wire, pinResetOLED);

const byte numChars = 32;
char receivedChars[numChars];

boolean newData = false;

void setup() {
    Serial.begin(9600);
    // Serial.println("<Arduino is ready>");
    if(!ecranOLED.begin(SSD1306_SWITCHCAPVCC, i2cAddress))
      while(1);
    ecranOLED.clearDisplay();
    ecranOLED.setTextSize(2);
    ecranOLED.setCursor(0, 20);
    ecranOLED.setTextColor(SSD1306_WHITE);
    ecranOLED.display();    
}

void loop() {
    recvWithStartEndMarkers();
    showNewData();
}

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;
 
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

void showNewData() {
    if (newData == true) {
        // Serial.print("This just in ... ");
        // Serial.println(receivedChars);

        ecranOLED.clearDisplay();
        ecranOLED.setTextSize(2);
        ecranOLED.setCursor(0, 20);
        ecranOLED.print(receivedChars);
        ecranOLED.display();        
        newData = false;
    }
}
