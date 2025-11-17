# CRUMB
**Technology that adapts to you.**

Learn to build computers with zero experience. $12, 5 minutes, no prerequisites.

The goal of CRUMB is to teach you what computers are/how to communicate with them, once you understand how to communicate with it, you can build anything

---

## What You'll Build

**Genesis Zero** (15 min) → Make an LED pulse like a heartbeat  
**Genesis One** (45 min) → Connect your own LED  
**Your CRUMB** (∞) → Add buttons, sensors, displays, motors—anything

Once you understand the pattern, you can build:
- Meditation timers that breathe with you
- Plant monitors that text when thirsty
- Custom game controllers
- Weather stations
- Pet feeders
- Smart lights
- Whatever you need

---

## Quick Start: Genesis Zero

**What you need:**
- ESP32 board (~$12 on Amazon - search "ESP32 DevKit")
- USB-C cable (one that transfers data, not just power)
- Computer with USB port

**Steps:**
Video guide coming soon
1. Plug ESP32 into computer via USB
2. Install Arduino IDE (arduino.cc/en/software)
3. Add ESP32 board support:
   - Arduino IDE → Preferences → Additional Board Manager URLs
   - Paste: `https://dl.espressif.com/dl/package_esp32_index.json`
   - Tools → Board → Boards Manager → Search "ESP32" → Install
4. Open `/software/genesis_zero/genesis_zero.ino`
5. Select board: Tools → Board → ESP32 Dev Module
6. Select port: Tools → Port → (your USB port)
7. Click Upload (arrow button)
8. Watch the onboard LED pulse like a heartbeat

**That's it.** You just programmed a computer.

**Troubleshooting:**
- LED not pulsing? Check you selected the right port in Tools → Port
- Upload failed? Press and hold BOOT button on ESP32 while uploading
- Can't find port? Try a different USB cable (must support data transfer)
- Still stuck? Copy the error message into ChatGPT or Claude and ask for help

---

## Next Steps: Genesis One

**What you need (additional):**
- 1x LED (any color, ~$0.50)
- 1x 220Ω resistor (~$0.10)
- 2x jumper wires OR breadboard

**Steps:**
1. Connect LED long leg (anode) to GPIO pin 2 on ESP32
2. Connect LED short leg (cathode) to resistor
3. Connect other end of resistor to GND pin on ESP32
4. Upload the same code (it works on GPIO 2 by default)
5. Watch YOUR LED pulse

**What you just learned:** How to connect external components to a computer and control them with code.

**Now you understand the pattern.** Buttons, sensors, motors, displays—they all work the same way. Plug into GPIO pin. Write code. Control it.

---

## Understanding the Code
```cpp
//The entire program

#define LED_PIN 2  // Which pin controls the LED

void setup() {
  pinMode(LED_PIN, OUTPUT);  // Tell the ESP32 this pin controls something
}

void loop() {
  heartbeat();      // Call the heartbeat function below
  delay(800);       // Wait 0.8 seconds between beats
}

void heartbeat() {
  pulse(100, 150);  // First beat (Lub)
  delay(150);       // Short pause
  pulse(100, 150);  // Second beat (Dub)
}

void pulse(int brightness, int duration) {
  analogWrite(LED_PIN, brightness);  // Turn LED on
  delay(duration);                    // Wait
  analogWrite(LED_PIN, 0);           // Turn LED off
}
```

**That's 20 lines. Technology that feels alive.**

Change the numbers to make it beat faster, slower, brighter, dimmer. Break it. Fix it. Make it yours.

---

## Why This Exists

Most technology demands you adapt to it.  
CRUMB adapts to you.

**No tracking.** Your data stays local.  
**No subscriptions.** You own it forever.  
**No gatekeeping.** Clear docs, AI help when stuck.  
**No closed systems.** Modify anything.

Technology should help you be more human, not less.

---

## The Mission

Break the wall between "people who build technology" and "everyone else."

I built this because my brother struggles with conventional technology—apps that demand constant attention, interfaces designed for one way of thinking. I wanted to create something different.

Then I realized: the real problem isn't just the final product. It's that people think building technology is too hard for them.

Every person who builds CRUMB and understands how it works is one less person dependent on closed systems that don't serve them.

---

## Your Unfair Advantage

Previous generations had to figure this out alone. You have AI.

Stuck on a step? Copy the error into ChatGPT or Claude.  
Don't understand something? Ask.  
Want to try something different? Describe what you want.

AI teachers are infinitely patient, always available, and never judge you for asking questions.

**That's why now is the best time in history to learn this.**

---

## What's Next For You

**Option 1: Keep building**
- Add a button (connect to GPIO, read input)
- Add a temperature sensor (read values, display them)
- Add a display (show text, images)
- Build whatever you need

**Option 2: Help others**
- Share what you learned
- Answer questions in Discussions
- Contribute code improvements
- Design enclosures or cases

**Option 3: Teach someone**
- Show a friend how to build Genesis Zero
- Help them understand the pattern
- Watch them realize they can do this too

---

## Project Status

**✅ Available now:**
- Genesis Zero working code
- Genesis One instructions
- Core philosophy documented
- GPL-3.0 open source

**🚧 Coming November 30, 2025:**
- Complete video tutorial
- Photo build guide
- Bill of materials with supplier links
- Starter kit ordering ($15 shipped - everything you need)

---

## Files in This Repository
```
/software
  /genesis_zero - Heartbeat LED code (start here)
  /genesis_one - External LED code (same as zero, just documented)
  /examples - Button, sensor, display examples

/hardware
  /schematics - Wiring diagrams
  /bom - Bill of materials with links

/docs
  /build_guide - Step-by-step photos (coming Nov 30)
  /troubleshooting - Common issues and fixes

README.md - You are here
LICENSE - GPL-3.0 full text
```

---

## License

**GPL-3.0** — You can build it, modify it, sell it, share it.  
The only requirement: keep it open for others.

This means:
- ✅ Use this code in your own projects
- ✅ Modify it however you want
- ✅ Sell devices you build with this
- ✅ Keep your modifications private while developing
- ⚠️ If you distribute your modified version, share the source code
- ⚠️ Don't take this, close it off, and charge subscriptions

**Why this license?** Technology that serves humans should belong to humans, not corporations.

---

## Questions?

**Technical issues?** Open an issue in the Issues tab  
**General questions?** Start a discussion in Discussions tab  
**Email:** wja326@lehigh.edu  
**Website:** wyetherp.com *(launching Nov 30)*

---

## Contributing

🔨 **Build one** → Share photos and what you learned  
❓ **Ask questions** → Help us improve documentation  
💻 **Add features** → Submit pull requests  
🎨 **Design** → Create cases, PCBs, enclosures  
📚 **Teach** → Help others in Discussions

All contributions welcome. No contribution too small.

---

**Build. Share. Teach. Repeat.**

Made by Wyeth Anzilotti  
GPL-3.0 License  
2025
