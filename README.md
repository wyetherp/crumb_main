CRUMB

Make a computer pulse like a heartbeat. 15 minutes. $12. Zero experience.
What You're Building
Genesis Zero: An LED that pulses like a heartbeat. On a computer you programmed.
That's it. Once you can make a light blink, you can control anything—buttons, sensors, displays, motors. The pattern is the same.

What You Need

ESP32 board (~$12 on Amazon - search "ESP32 DevKit")
USB-C cable (data transfer, not just charging, Apple cables work best)
Computer with USB or USB-C port
Chrome or Edge browser


How To Do It (The Easy Way)
Reality check: This sounds complicated. It's not.
Steps:

Go to wyetherp.com/flash (Dec 5th)
Plug in the ESP32 via USB
Click "Flash Genesis Zero"
Select your USB port when prompted
Wait 30 seconds
Watch it pulse

That's it. No installation. No setup. No compatibility hell.
Video tutorial: [YouTube link - coming Dec 5th]

If That Doesn't Work (Or You Want To Modify Code)
Web flashing works 90% of the time. But if you hit the 10%:
Arduino IDE Method:

Install Arduino IDE (arduino.cc/software)
Add ESP32 support (paste this in Preferences → Board Manager URLs):

   https://dl.espressif.com/dl/package_esp32_index.json

Open /software/genesis_zero/genesis_zero.ino
Upload

Why you'd use Arduino IDE:

Web flash didn't work (rare, but happens)
You want to modify the code (change speed, brightness, pattern)
You want to build Genesis One, Two, etc. (requires code editing)

For Genesis Zero? Just use the website. It's easier.

Your Unfair Advantage
You have AI. Previous generations didn't.
Think about it:

Stuck at 2am? AI is awake
Don't understand an error? AI explains it in 10 seconds
Want to try something different? AI rewrites the code for you
Feel stupid asking? AI doesn't judge

The best teacher of a computer is another computer.
You're not learning alone. You have a 24/7 dedicated tutor that knows every error message, speaks every programming language, and has infinite patience.
This is why NOW is the easiest time in history to learn this.

What ESP32 Actually Is
It sounds scary. It's not.
ESP32 = small computer ($12) that you can program.
That's it. It's not magic. It's just a computer that:

Fits in your hand
Runs code you write
Controls lights, sensors, buttons, motors, whatever

When you "flash code," you're just installing a program. Like installing an app on your phone, except YOU wrote the app.

What's Next
After Genesis Zero (15 min):

Genesis One (45 min): Connect your own LED, not the built-in one
Genesis Two+: Add buttons, sensors, displays—whatever you want

Or just build:

Meditation timer that breathes with you
Plant monitor that texts when thirsty
Custom game controller
Smart lights
Whatever you need

Once you understand the pattern, you can build anything.

Troubleshooting
Web flash didn't work?

Try a different USB cable (must support data, not just power)
Try a different USB port
Try pressing and holding the BOOT button on the ESP32 while flashing
Copy the error into ChatGPT/Claude - they'll probably fix it

Still stuck? Open an issue or ask in Discussions

Files

For Genesis Zero: Just use the website (easiest)
Want to modify code? /software/genesis_zero/genesis_zero.ino
Genesis One+: /software/genesis_one/
Examples: /examples/ (buttons, sensors, displays)


Status
✅ Available now: Code, instructions, AI troubleshooting
🚧 Coming DEC 5th: Web flasher, video tutorial, starter kit ordering

Questions?

Stuck? Copy error into ChatGPT/Claude
Technical issue? Open an issue
General question? Start a discussion
Email: wja326@lehigh.edu


License: GPL-3.0 (build it, modify it, sell it, share it - just keep it open)
Made by Wyeth Anzilotti | 2025

That's it. Plug in. Click flash. Watch it pulse. $12, 15 minutes, AI in your corner.
Go build.
