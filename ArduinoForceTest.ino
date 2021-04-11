/* 
FSR simple testing sketch. 
Used to collect an hour of sitting data and determine sampling speed
*/
int fsrPin1 = 0;    
int fsrPin2 = 1;
int fsrPin3 = 2;
int fsrPin4 = 3;
int fsrPin5 = 4;

 
void setup(void) {
  Serial.begin(9600);   
}
 
void loop(void) {

 
  Serial.print(analogRead(fsrPin1));     // the raw analog reading
  Serial.print(",");
  Serial.print(analogRead(fsrPin2));
  Serial.print(",");
  Serial.print(analogRead(fsrPin3));
  Serial.print(",");
  Serial.print(analogRead(fsrPin4));
  Serial.print(",");
  Serial.print(analogRead(fsrPin5));
  Serial.print("\r\n");
 
  delay(1000);
}
