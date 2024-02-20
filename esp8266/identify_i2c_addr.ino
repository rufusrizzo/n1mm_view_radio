// ------------------------------------------------------------
// i2c_scanner - Updated for PCBoard.ca 2020-08-20
//
// This sketch tests the standard 7-bit addresses
// Devices with higher bit address might not be seen properly
//
// Report data is sent to Serial Monitor setup for 9600 baud
// ------------------------------------------------------------
//Source:
//https://www.make-it.ca/i2c-lcd-display-on-arduino/
#include &lt;Wire.h&gt;
void setup()
{
Wire.begin();
Serial.begin(9600);
Serial.println("\nI2C Bus Scanner");
}
void loop()
{
byte error, address;
int nDevices;
Serial.println("Scanning I2C Bus...");
nDevices = 0;
for(address = 1; address &lt; 127; address++ )
{
// The i2c_scanner uses the return value of
// the Write.endTransmisstion to see if
// a device did acknowledge to the address.
Wire.beginTransmission(address);
error = Wire.endTransmission();
if (error == 0)
{
Serial.print("I2C device found at address 0x");
if (address&lt;16)
Serial.print("0");
Serial.print(address,HEX);
Serial.println(" ");
nDevices++; // Increment counter for total number of devices located
}
else if (error==4)
{
Serial.print("Unknow error at address 0x");
if (address&lt;16)
Serial.print("0");

