
#include <SoftwareSerial.h>               
#include <LiquidCrystal.h>
#define USE_ARDUINO_INTERRUPTS true    // Set-up low-level interrupts for most acurate BPM math.
#include <PulseSensorPlayground.h>  

LiquidCrystal lcd(4, 5, 6, 7, 8, 9);
SoftwareSerial mySerial(2, 3);
#define echoPin A5
#define trigPin A4 

char Incoming_value = 0; 
long duration; 
int distance; 
int ultrafreecounter =0;
unsigned long previousMillis = 0;  //will store last time LED was blinked
const long period = 1000;
const long period1 = 100;
unsigned long previousMillis2 = 0; 
unsigned long previousMillis3 = 0; //will store last time LED was blinked
unsigned long currentMillis2 =0;
unsigned long currentMillis3 =0;
unsigned long currentMillis =0;
char namedb[15] = "";
char phonedb[15] = "";
const int PulseWire = 0; 
int Threshold = 700; 

  int counter1 =0;
  int counter2 =0;
  int sensorValue =97;
  int myBPM = 72;
  int movement_counter =1;
  
PulseSensorPlayground pulseSensor;  // Creates an instance of the PulseSensorPlayground object called "pulseSensor"


void setup() 
{
  Serial.begin(9600);    
  mySerial.begin(9600); 
   
  pinMode(trigPin, OUTPUT); 
  pinMode(echoPin, INPUT); 
    
  lcd.begin(20, 4);
  lcd.print("Covid Robo 2021 CEP");
  delay(1000);
  while(1)
  {
    if (Serial.available())
   {
     Incoming_value = Serial.read();
     if(Incoming_value == 'D')
     {
        lcd.setCursor(0, 1);
        lcd.print("DB - Connect - OK");
        Serial.write("D");
        counter1 = 1;
        
     }
     if(Incoming_value == 'P')
     {
        lcd.setCursor(0, 2);
        lcd.print("Pi - Connect - OK");
        Serial.write("P");
        counter2 = 1;
     }

   }
     if((counter2 == 1)&&(counter1 ==1 ))
     {
      lcd.setCursor(0, 3);
      lcd.print("Rover - Connect - OK");
      break;
     }
     else
     {
      Serial.write("RoverReady");
      delay(100);
     }
  }

  pulseSensor.analogInput(PulseWire);   
  pulseSensor.setThreshold(Threshold);    

  pinMode(13, OUTPUT);        
  pinMode(12, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(10, OUTPUT); 
  pinMode(A2, OUTPUT);  
  pinMode(A3, OUTPUT);  // wait for a second
  digitalWrite(A2, HIGH); 
  digitalWrite(A3, HIGH); 
  digitalWrite(13, LOW);    // turn the LED off by making the voltage LOW
  digitalWrite(12, LOW); 
  digitalWrite(11, LOW); 
  digitalWrite(10, LOW); 
  delay(5000);   
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("NAME : ");
  lcd.setCursor(0,1);
  lcd.print("PHONE: ");
  lcd.setCursor(0,2);
  lcd.print("HB:   ");
  lcd.setCursor(5,2);
  lcd.print(" TMP:    ");
  lcd.setCursor(14,2);
  lcd.print("US:   ");
  lcd.setCursor(0,3);
  lcd.print("SYS: Rdy  ");
  lcd.setCursor(10,3);
  lcd.print("RovD:    ");
  
}
void loop()
{
if( Serial.available() > 0)
{
  char movement_reader = Serial.read();
   if((movement_reader == 'R')|| (movement_reader == 'r'))
   {
    movement_counter =1;
    counter2 =1;
   }
   if((movement_reader == '*')&& ( counter2== 10))
   {
     counter2 =2;
     movement_counter =0;
   }
}
if (movement_counter == 1)
{
  Rover_direction();
}
  Ultrasound();
  ultrastop();
  lcddisplay1sec();
  nameandphone();
  HBTemp();
  SelfSanitization();
}  

void SelfSanitization(){
  if(counter2  == 3)
  {
      lcd.setCursor(0,3);
      lcd.print("SYS: SY  ");
      
    digitalWrite(A2, LOW); 
    digitalWrite(A3, LOW); 
    delay(3000);
    lcd.setCursor(0,3);
    lcd.print("SYS: SN  ");
    digitalWrite(A2, HIGH); 
    digitalWrite(A3, HIGH); 
    counter2 = 4;
  }
  
}


void HBTemp()
{
   if(counter2 == 4)
   {

    myBPM = 72;
    int HBcounter = 0;
    while(1)
    { 
       lcd.setCursor(0,3);
            lcd.print("SYS: HB2 ");
      if(Serial.available())
      {
        char abcdef = Serial.read();
       
      if((abcdef ==  'H')|| (HBcounter ==1))
      {
            lcd.setCursor(0,3);
            lcd.print("SYS: HB1 ");
      HBcounter =1;
      int sensorValue1 = analogRead(A0);
      sensorValue = (sensorValue + sensorValue1)/2;
      sensorValue = sensorValue/10;
      sensorValue = sensorValue+66;
      //int myBPM1 = pulseSensor.getBeatsPerMinute();  
      currentMillis2 = millis();
      if(currentMillis2 - previousMillis2 >= period) 
          {                                                   
                counter1 = counter1+1; 
                previousMillis2=   currentMillis2;                                             
          }

       myBPM = 80;   
         
      if(counter1 > 9 )
      {
        lcd.setCursor(10,2);
        lcd.print("    ");
        lcd.setCursor(10,2);
        lcd.print(sensorValue);
        lcd.setCursor(3,2);
        lcd.print("   ");
        lcd.setCursor(3,2);
        lcd.print(myBPM);
        Serial.print( "0"+String(myBPM) +"."+"0"+String(sensorValue)+"...");
        Serial.print("Terminated");
        counter1= 1;
        counter2 =5;
        delay(2000);
        break;
      }
    }
   }
}

   }
   }

void nameandphone()
{
  Serial.flush();
   if(counter2 == 2)
   {
    int i=0;
    counter2 = 3;
      lcd.setCursor(0,0);
      lcd.print("NAME :              ");
      lcd.setCursor(0,1);
      lcd.print("PHONE:              ");
    while(1)
        {
           if (Serial.available())
           {
            char checkbyte = Serial.read();
            if(checkbyte =='#')
            {
              Serial.print("NameSucces");
              break;
            }
             namedb[i] = checkbyte;
             lcd.setCursor(7+i,0);
             lcd.print(checkbyte);
             i++;
           }
       }
       int j=0;
        while(1)
        {
          
           if (Serial.available())
           {
            char checkbyte = Serial.read();
            if(checkbyte =='#')
            {
              Serial.print("PhoneSuces");
              break;
            }
             phonedb[j] = checkbyte;
             lcd.setCursor(8+j,1);
             lcd.print(checkbyte);
             j++;
           }
       }
   }
}


void ultrastop()
{
    currentMillis3 = millis(); // store the current time
  if(currentMillis3 - previousMillis3 >= period1) 
  { 
    previousMillis3 = currentMillis3;
    if( distance < 15)
  {
    ultrafreecounter =ultrafreecounter+1;
  }
  }
  if(ultrafreecounter > 10)
  {
    ultrafreecounter =0;
      digitalWrite(13, LOW);    // turn the LED off by making the voltage LOW
      digitalWrite(12, LOW); 
      digitalWrite(11, LOW); 
      digitalWrite(10, LOW); 
      lcd.setCursor(15,3);
      lcd.print("Stop ");
      if(counter2 == 1)
      {
        Serial.print("UStop");
        lcd.setCursor(17,2);
        lcd.print("   ");
        lcd.setCursor(17,2);
        lcd.print(distance);
        counter2 = 10;
        movement_counter =0;
      }
  }
}


void lcddisplay1sec()
{
  unsigned long currentMillis = millis(); // store the current time
  if(currentMillis - previousMillis >= period) 
  { 
      previousMillis = currentMillis;
      lcd.setCursor(17,2);
      lcd.print("   ");
      lcd.setCursor(17,2);
      lcd.print(distance);

  }
}



void Ultrasound()
{
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;
}




void Rover_direction()
{
  if (mySerial.available())
   {
   Incoming_value = mySerial.read();      
    if(Incoming_value == '2')
    {
      
      digitalWrite(13, HIGH);    
      digitalWrite(12, LOW); 
      digitalWrite(11, HIGH); 
      digitalWrite(10, LOW);
      lcd.setCursor(15,3);
      lcd.print("Right");
      Serial.print("Right");
       
    }
    if(Incoming_value == '1')
    {
     digitalWrite(13, LOW);    
     digitalWrite(12, HIGH); 
     digitalWrite(11, LOW); 
     digitalWrite(10, HIGH); 
     lcd.setCursor(15,3);
     lcd.print("Left ");
     Serial.print("Left ");
    }
    if(Incoming_value == '4')
    {
      digitalWrite(13, HIGH);   
      digitalWrite(12, LOW); 
      digitalWrite(11, LOW); 
      digitalWrite(10, HIGH); 
      lcd.setCursor(15,3);
      lcd.print("Back ");
      Serial.print("Back ");
      
    }
    if(Incoming_value == '3')
    {
      digitalWrite(13, LOW);    // turn the LED off by making the voltage LOW
      digitalWrite(12, HIGH); 
      digitalWrite(11, HIGH); 
      digitalWrite(10, LOW); 
      lcd.setCursor(15,3);
      lcd.print("Front");
      Serial.print("Front");
      
    }
    if(Incoming_value == '5')
    {
      digitalWrite(13, LOW);    // turn the LED off by making the voltage LOW
      digitalWrite(12, LOW); 
      digitalWrite(11, LOW); 
      digitalWrite(10, LOW); 
      lcd.setCursor(15,3);
      lcd.print("Stop ");
      Serial.print("UStoP");         
    }
}
}
