/*
 * ============================================
 * CRUMB Genesis Zero - The Heartbeat
 * ============================================
 * 
 * Your first program. An LED that breathes.
 * 
 * What's happening:
 * The LED slowly gets brighter, then slowly gets dimmer.
 * Over and over. Like a heartbeat.
 * 
 * Why it matters:
 * Every computer runs the same pattern: INPUT → PROCESS → OUTPUT
 * Once you understand this, you can build anything.
 * 
 * License: GPL-3.0 (Open source forever)
 * Learn more: https://wyetherp.com/crumb
 * ============================================
 */

// The built-in LED is on pin 2
int ledPin = 2;

// How bright the LED is (0 = off, 255 = full bright)
int brightness = 0;

// How much to change brightness each step
int fadeAmount = 5;

void setup() {
  // Set the LED pin as an output
  pinMode(ledPin, OUTPUT);
}

void loop() {
  // Set the LED brightness
  analogWrite(ledPin, brightness);

  // Change brightness for next time
  brightness = brightness + fadeAmount;

  // Reverse direction at the ends
  if (brightness <= 0 || brightness >= 255) {
    fadeAmount = -fadeAmount;
  }

  // Wait a bit (controls the speed of the pulse)
  delay(30);
}

/*
 * That's it. ~10 lines of real code.
 * You just made a computer breathe.
 * Now go build something.
 */
