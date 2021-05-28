void setup() {
Serial.begin(9600);   // put your setup code here, to run once:
pinMode(LED_BUILTIN, OUTPUT);
digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
    while(Serial.available())
    {        
      if  (Serial.read() == '1')  // When '1' is received, turn motor clockwise
        {
              digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
              
        }
      else
        {
              digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
                 
        }
    }
}
