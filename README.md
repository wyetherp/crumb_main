# CRUMB
### Build a soul-bonded AI companion for someone you love.

If you have any trouble ask AI for help!

$90 in hardware. One Python file. One person it's built for.

---

## Build Ember — The Raspberry Pi Companion

Ember is a physical AI companion that lives on a desk, knows its owner's name, and answers questions in plain English. This is the fastest path to a working CRUMB device.

### What You Need

| Part | Cost |
|------|------|
| Raspberry Pi 4 | ~$40 |
| 7" DSI Touchscreen | ~$35 |
| USB Microphone | ~$5 |
USB Speaker | ~$10 |

You'll also need:
- An [Anthropic API key](https://console.anthropic.com) (Claude)
- An [OpenAI API key](https://platform.openai.com) (Whisper)

**Total: ~$90**

---

### Setup

Video Build Guide: 
https://youtu.be/2e-LP8AQQFI

In terminal
**1. Install dependencies**
```bash
pip install anthropic openai sounddevice scipy pygame numpy
```

**2. Get the code**

Copy paste crumb.py directly into a file on the raspi (Easier)

Or
Clone Repository (Will copy all code i suggest copy pasting the one crumb.py file)

```bash
git clone https://github.com/wyetherp/crumb_main/crumb.py
cd crumb_main
```

**3. Add your API keys**

Open `crumb.py` and find the `ask_claude()` and `transcribe()` functions. Replace the API key strings with your own keys.

**4. Set the name**

At the top of `crumb.py`, find:
```python
ARTIFICER_SETS_NAME = "Luke"
```
Change `"Luke"` to whoever you're building this for.

**5. Run it**
```bash
python3 crumb.py
```

---

### What It Does

- **Binding ritual** — first-time attunement that remembers the owner's name forever
- **Ask CRUMB** — speak a question, get a response from Claude AI
- **Timer** — focus timer up to 60 minutes
- **Clock** — current time
- **Music** — plays up to three local tracks

---

### Customize It

Everything that makes Ember personal lives at the top of `crumb.py`:

```python
ARTIFICER_SETS_NAME = "Luke"     # who it's built for
CRUMB_SYSTEM_PROMPT = "..."      # its personality
TRACKS = [...]                   # music file paths
```

The personality is where it becomes yours. Describe who they are, what they love, how they talk. The AI does the rest.

---

## The ESP32 Path

Want to understand computing from the ground up before building?
Start with the [video curriculum](https://www.youtube.com/@Wyetherp-1) — 15 videos, $30 in parts, zero to AI companion.

📗 Earth → 🔥 Fire → 🌊 Water → 💨 Air

---

## Philosophy

Build it for someone specific. That's the whole philosophy.

GPL-3.0 — build it, modify it, sell it. Keep the knowledge open.

---

*Made by Wyeth Anzilotti | 2026*
*Because the wall is artificial and we can break it.*
