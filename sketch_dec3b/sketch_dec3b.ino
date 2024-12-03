
#include <Servo.h>

#define SERVO_DELAY 5
#define SERVO_STEP 36

Servo servoX;
Servo servoY;

int posX = 0;
int posY = 0;


void plotData() {
  // Print the X position for the plotter
  Serial.print("X_Pos:");
  Serial.print(posX);
  Serial.print("\t");

  // Print the Y position (remains constant for now)
  Serial.print("Y_Pos:");
  Serial.println(posY);
}


void setup() {
  servoX.attach(9);
  servoY.attach(10);
  

  Serial.begin(115200);
}


// n stands for NULL, just a random character to prevent "empty character constant" error while also being understood that it holds no functional purpose.
char target = 'n'; // x or y
char direction = 'n'; // l or r


void loop() {

  if (Serial.available() > 0) {
    String serialMessage = Serial.readString();

    if (serialMessage == "reset") {
      posX = 0;
      posY = 0;
      servoX.write(posX);
      servoY.write(posY);
    } else {

      target = serialMessage[0];
      direction = serialMessage[2];
      
      if (target == 'x') {
        if (direction == 'l') {
          posX-=SERVO_STEP;
        }
        if (direction == 'r') {
          posX+=SERVO_STEP;
        }
        servoX.write(posX);
        delay(SERVO_DELAY);
      }
      if (target == 'y') {
        if (direction == 'l') {
          posY-=SERVO_STEP;
        }
        if (direction == 'r') {
          posY+=SERVO_STEP;
        }
        servoY.write(posY);
        delay(SERVO_DELAY);
      }

      // delay(5)
      // Serial.print(target);
      // Serial.print(" - ");
      // Serial.println(direction);
    }

    

  }
}
