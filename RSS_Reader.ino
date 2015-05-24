

// Ardunio showing whatever user enters as input from Serial Terminal, starting and ending with '~'

int startstring = 0;     // recognition of beginning of new string
int charcount = 0;       // keeps track of total chars on screen
int startname = 0;
int LInterrupt = 1;     // pin 2,3 are interrupt enabled pin. Attaching Proximity sensor in pin 2 i.e. interrupt pin 1. 
int RInterrupt = 0;

#include  <LiquidCrystal.h>  // import the LiquidCrystal Library
LiquidCrystal lcd(12, 11, 4, 5, 6, 7);      //(rs,enable,d4,d5,d6,d7)

void setup()
{
  Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
  lcd.begin(16,2);        // Initialize the LCD size 16x2 (column,row).
  lcd.setCursor(0,0);     // Set cursor position to top left corner
  attachInterrupt(LInterrupt, Lhandler, RISING);
  attachInterrupt(RInterrupt, Rhandler, RISING);
  pinMode(13, OUTPUT);
}

void Lhandler()
{
  Serial.println("1");
}

void Rhandler()
{
  Serial.println("2");
}

void loop()
{
  char incomingByte = 0;   // for incoming serial data
  if (Serial.available() > 0)
  {  // Check for incoming Serial Data
    //digitalWrite(13, HIGH);
    incomingByte = Serial.read();
    // read the data.
    if((incomingByte == '^')&&(startname == 0))                    // name started start printing on first line.
    {
        startname = 1;
        startstring = 0;
        lcd.clear();
        lcd.setCursor(0,0);
    }
    else if((incomingByte == '^')&&(startname == 1))               // end name, now data will start.
    {
      startname = 0;
      lcd.setCursor(0,1);
    }
    else if ((incomingByte == '~') && (startstring == 0))            // Check if byte is marker ~ to start the printing
    {                                                                
      startstring = 1;      // start printing
      charcount = 0;
      lcd.setCursor(0,1);
    }
    else if ((incomingByte == '~') && (startstring == 1))            // Check for the closing '~' to end the printing of serial data
    {
      startstring = 0;                                               // Set the printing to off
      delay(2000);                                                   // Wait 5 seconds
//      lcd.clear();                                                   // Wipe the screen
      charcount = 0;                                                 // reset the character count to 0
      lcd.setCursor(0,1);                                            // set the cursor to 0,1
      lcd.print("                ");                                 // empty the second row.
      lcd.setCursor(0,1);                                            // reset the cursor
    }
    else if(startname == 1)
    {
       lcd.print(incomingByte);
    }
    else if (startstring == 1)
    {                                                                // check if the string has begun if first '~' has been read
      if (charcount <= 15)
      {                                                              // check if charcount is under or equal to 30
//        if(charcount == 15)                                          // if the first line is full.
//          lcd.setCursor(0,1);                                        // set cursor to second line.
        lcd.print(incomingByte);                                     // Print the current byte in the serial
        charcount = charcount+1;                                     // Increment the charcount by 1 yes I know it's awkward
      }
      else if (charcount > 15)
      {                                                               // if the charcount is equal to 31 aka the screen is full
        delay(1000);                                                   // let user read the data!
       lcd.setCursor(0,1);                                            // reset the cursor to 0,0
        lcd.print("                ");                                 // empty the second row.
//      lcd.autoscroll();
        lcd.setCursor(0,1);                                           // as after printing all spaces cursor would have reached end so reset it.
        lcd.print(incomingByte);                                      // continue printing data
        charcount = 1;                                                // set charcount back to 1
      }
    }
   // else
    //{
     /// lcd.print(incomingByte);
      //charcount += 1;
    //}
  }
  digitalWrite(13, LOW);
  delay(10);                                                         // 10ms delay for stability
}
