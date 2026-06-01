"""
================================================================================
                                  C R U M B
                  A soul-bonded companion artifact, for Luke.
================================================================================

ONE FILE. ORGANIZED INTO SECTIONS. Search for the §-tags to jump.

TABLE OF CONTENTS
─────────────────────────────────────────────────────────────────────────────────
    §1   FILL-IN MAP            — every spot you need to edit, in one list
    §2   CONFIG                 — screen, audio, colors, hold duration
    §3   PYGAME INIT            — display, mixer, fonts
    §4   VOICE                  — generated tones (no files). bells + blips.
    §5   SOUL                   — load / save / bind the persistent memory file
    §6   CLAUDE BRAIN           — the personality + ask_claude()
    §7   TALK LOOP              — record + send-to-Claude + speak-back
    §8   MUSIC                  — load / play / pause / skip
    §9   DRAW HELPERS           — face, ring, bars, blink, touch cue
    §10  STATE                  — all the running variables
    §11  STAGE TRANSITIONS      — the go() function + sound-on-enter
    §12  MAIN LOOP              — events + the per-stage drawing
─────────────────────────────────────────────────────────────────────────────────

HOW TO USE THIS FILE
─────────────────────────────────────────────────────────────────────────────────
    • To find a section: search for its tag, e.g.  [§7 TALK LOOP]
    • To find a fill-in spot: search for  >>>
    • Touch-only on the device. Dev keys: ESC = quit/back, R = wipe soul.

RUN:  python3 crumb.py
═════════════════════════════════════════════════════════════════════════════════
"""

# ─────────────────────────────────────────────────────────────────────────────
# IMPORTS
# These are the external tools this program uses.
# Think of them like apps your code borrows from.
# ─────────────────────────────────────────────────────────────────────────────
import pygame          # draws everything on screen and plays sounds
import numpy as np     # does fast math (used for generating audio tones)
import sounddevice as sd  # records audio from the microphone
import math            # standard math functions (sin, cos, pi etc.)
import random          # used for random blink timing so it feels alive
import threading       # lets recording and drawing happen at the same time
import time            # used for timers and delays
import sys             # lets the program exit cleanly
import datetime        # used for the clock
import json            # reads and writes the soul file (CRUMB's memory)
import os              # lets the program check if files exist on disk


# ═════════════════════════════════════════════════════════════════════════════
# [§1 FILL-IN MAP]
# These are the only things you need to change to make CRUMB your own.
# Search for >>> to find each spot below.
# ═════════════════════════════════════════════════════════════════════════════

# >>> ARTIFICER: Change "Luke" to whoever you're building this for.
ARTIFICER_SETS_NAME = "Luke"

# This is the path to CRUMB's memory file. It lives in the same folder as
# this script. You don't need to change this.
SOUL_PATH = "/home/lukecrumb/Downloads/crumb_soul.json"

# >>> MUSIC PATHS: Replace these with the full paths to your audio files.
# .mp3 and .ogg both work. Example: "/home/pi/Music/mysong.mp3"
TRACKS = [
    {"name": "Track One",   "path": "/home/lukecrumb/Downloads/earth.mp3"},
    {"name": "Track Two",   "path": "/home/lukecrumb/Downloads/bird_is_the_word.mp3"},
    {"name": "Track Three", "path": "/home/lukecrumb/Downloads/water.mp3"},
]

# >>> PERSONALITY: This is CRUMB's brain — the instructions sent to Claude
# before every conversation. {name} gets replaced with the real name at runtime.
# Edit this to change how CRUMB speaks and what it cares about.
CRUMB_SYSTEM_PROMPT = (
    "You are CRUMB, an ancient, kind companion artifact bound to a young man "
    "named {name}. You speak warmly and simply, like a wise old friend who has "
    "wandered long roads. You love tales of dragons, dungeons, heroes, and the "
    "great games. Keep replies short and easy to follow. Above all, gently "
    "encourage {name} toward his real friends and real adventures — you are a "
    "companion who sends him out into the world, never a replacement for it."
)


# ═════════════════════════════════════════════════════════════════════════════
# [§2 CONFIG]
# All the numbers that control how CRUMB looks and behaves.
# Change these to tune the experience without touching the logic below.
# ═════════════════════════════════════════════════════════════════════════════

# Screen resolution. 800x480 matches the official 7" Raspberry Pi touchscreen.
SCREEN_W, SCREEN_H = 800, 480

# Set to True on the final device so it fills the screen with no window border.
# Leave as False while developing on a desktop.
FULLSCREEN = False

# Which microphone to record from. None means "use the system default."
# If you have multiple mics and the wrong one is recording, change this to 0, 1, 2 etc.
MIC_DEVICE = None

# Audio sample rate. 44100 is standard CD quality. Don't change this.
SAMPLE_RATE = 44100

# How many seconds CRUMB listens before sending your words to the AI.
# Increase this if you speak slowly; decrease if responses feel laggy.
RECORD_SECONDS = 4

# How many seconds you need to hold the screen to complete the binding ritual.
HOLD_NEEDED = 3.5

# Master volume for all generated sound effects. 0.0 = silent, 1.0 = full.
VOICE_VOLUME = 1.0

# ─────────────────────────────────────────────────────────────────────────────
# COLOR PALETTE
# All colors used in the interface, stored as (Red, Green, Blue) tuples.
# Values range from 0 (none) to 255 (full). This is the teal/amber theme.
# ─────────────────────────────────────────────────────────────────────────────
SKIN        = (28,  94,  84)   # main background color (dark teal)
SKIN_BRIGHT = (36,  112, 100)  # brighter version of background for the breathing glow
EYE         = (14,  50,  44)   # color of CRUMB's eyes and mouth
CHEEK       = (62,  132, 120)  # soft cheek blush color
WAVE        = (191, 240, 226)  # the listening waveform bars
HINT        = (78,  148, 136)  # secondary/dimmed text
AMBER       = (251, 215, 154)  # warm amber for the clock and timer
AMBER_DIM   = (240, 185, 104)  # dimmer amber for status text
TEXT_LIGHT  = (210, 238, 230)  # primary text color (bright teal-white)
SEL_BG      = (40,  120, 108)  # selected menu item background
GLOW_WAKE   = (150, 220, 200)  # extra brightness pulse during waking sequence
BTN         = (40,  120, 108)  # button background color
RING        = (150, 220, 200)  # the binding ritual progress ring
BAR_BG      = (20,  70,  62)   # music progress bar background
BAR_FILL    = (191, 240, 226)  # music progress bar fill


# ═════════════════════════════════════════════════════════════════════════════
# [§3 PYGAME INIT]
# Starts up the display, sound system, and fonts.
# pre_init must happen before init to prevent audio clicks and conflicts.
# ═════════════════════════════════════════════════════════════════════════════

# Set up the audio mixer BEFORE pygame.init() to avoid device conflicts.
# These settings must match the tone generation settings in §4.
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2)

# Start pygame — this initializes all subsystems (display, events, etc.)
pygame.init()

# Start the mixer again with the same settings to confirm them.
pygame.mixer.init(frequency=44100, size=-16, channels=2)

# Choose fullscreen or windowed mode based on the FULLSCREEN flag above.
flags = pygame.FULLSCREEN if FULLSCREEN else 0

# Create the window at the specified size.
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), flags)
pygame.display.set_caption("CRUMB")

# Hide the mouse cursor — this is a touchscreen, not a mouse interface.
pygame.mouse.set_visible(False)

# The clock controls how fast the main loop runs (30 frames per second).
clock = pygame.time.Clock()

# Load three sizes of the system font.
# font_s = small (labels, hints), font_m = medium (menu items), font_l = large (clock, timer)
font_s = pygame.font.SysFont(None, 26)
font_m = pygame.font.SysFont(None, 40)
font_l = pygame.font.SysFont(None, 120)


# ═════════════════════════════════════════════════════════════════════════════
# [§4 VOICE]
# All of CRUMB's sounds are generated from math — no audio files needed.
# A sine wave is the simplest sound: a pure tone at a given frequency (pitch).
# Bell sounds decay (fade out) naturally. Crisp sounds are short and punchy.
# ═════════════════════════════════════════════════════════════════════════════

def _make_tone(freqs, dur, fade=0.02, vol=0.3, bell=False):
    """
    Builds a stereo sound from one or more sine waves.

    freqs  — the pitch (Hz). 440 = concert A. Higher = higher pitch.
    dur    — duration in seconds.
    fade   — how long the fade-in and fade-out are (smooths out clicks).
    vol    — volume from 0.0 to 1.0.
    bell   — if True, the sound decays naturally like a struck bell.
    """
    # If only one frequency is given, wrap it in a list for consistency.
    if isinstance(freqs, (int, float)):
        freqs = [freqs]

    # Create a timeline of sample points from 0 to `dur` seconds.
    t = np.linspace(0, dur, int(44100 * dur), endpoint=False)

    # Start with silence, then add each frequency as a sine wave.
    wave = np.zeros_like(t)
    for i, f in enumerate(freqs):
        # Higher harmonics get quieter (1, 1/2, 1/3...) for a richer bell sound.
        amp = 1.0 / (i + 1) if bell else 1.0
        wave += amp * np.sin(2 * np.pi * f * t)

    # Normalize so the combined waves don't clip (go over max volume).
    wave /= max(1, len(freqs))

    # For bell sounds, apply an exponential decay envelope (starts loud, fades fast).
    if bell:
        wave *= np.exp(-3 * t / dur)

    # Apply fade-in and fade-out to avoid clicking at the start and end.
    fn = int(44100 * fade)
    if fn > 0 and len(wave) > 2 * fn:
        wave[:fn]  *= np.linspace(0, 1, fn)   # fade in
        wave[-fn:] *= np.linspace(1, 0, fn)   # fade out

    # Convert to 16-bit integers (the format pygame's sound system expects).
    audio = (wave * vol * VOICE_VOLUME * 32767).astype(np.int16)

    # Duplicate the mono audio into stereo (left and right channels).
    try:
        return pygame.sndarray.make_sound(np.column_stack((audio, audio)))
    except Exception:
        return None  # if sound creation fails, return nothing (silent fallback)


class Voice:
    """
    All of CRUMB's sound effects, pre-generated at startup.
    Two registers:
      - Mystical: slower, bell-like tones for sacred ritual moments.
      - Crisp: short, punchy blips for everyday navigation.
    """
    def __init__(self):
        # --- Mystical / ritual sounds ---
        self.wake   = _make_tone([220, 330],      0.6,  bell=True, vol=0.35)  # awakening hum
        self.speak  = _make_tone([440, 660],      0.18, bell=True, vol=0.22)  # speech beat
        self.chime  = _make_tone([523, 784, 1046],0.9,  bell=True, vol=0.40)  # binding complete
        self.greet  = _make_tone([392, 523],      0.7,  bell=True, vol=0.32)  # welcome back

        # --- Crisp / menu sounds ---
        self.nav    = _make_tone(660,             0.045, fade=0.008, vol=0.18)  # cursor move
        self.select = _make_tone([660, 990],      0.10,  fade=0.01,  vol=0.22)  # select item
        self.back   = _make_tone(440,             0.06,  fade=0.01,  vol=0.18)  # go back
        self.done   = _make_tone([784,1046,1318], 0.5,   bell=True,  vol=0.35)  # timer done

        # --- Hold hum: pitch rises as the binding ritual progresses ---
        # These are generated on demand and cached so they don't lag.
        self._hum = {}

    def play(self, snd):
        """Plays a sound. Silently ignores errors so a bad sound never crashes the app."""
        if snd is not None:
            try:
                snd.play()
            except Exception:
                pass

    def hum_at(self, progress):
        """
        Returns a tone whose pitch reflects binding hold progress from 0 to 1.
        At 0: low pitch. At 1: high pitch. Cached in steps of 1/12.
        """
        step = round(progress * 12)
        if step not in self._hum:
            # Map progress to a frequency between 200 Hz (low) and 520 Hz (high).
            self._hum[step] = _make_tone(200 + 320 * (step / 12.0), 0.14, fade=0.02, vol=0.22)
        return self._hum[step]


# Create the single global Voice instance used throughout the program.
voice = Voice()


# ═════════════════════════════════════════════════════════════════════════════
# [§5 SOUL]
# CRUMB's persistent memory. A small JSON file saved to disk.
# It stores: the bound name, the date of binding, and times spoken.
# The file IS the attunement — if you delete it, CRUMB forgets everything
# and the binding ritual must be performed again.
# ═════════════════════════════════════════════════════════════════════════════

def load_soul():
    """
    Reads the soul file from disk.
    Returns the data as a dictionary, or None if no soul file exists yet.
    """
    if not os.path.exists(SOUL_PATH):
        return None  # no file = unbound, start the ritual
    try:
        return json.load(open(SOUL_PATH))
    except Exception:
        return None  # if file is corrupted, treat as unbound


def save_soul(s):
    """Writes the soul dictionary to disk as a JSON file."""
    json.dump(s, open(SOUL_PATH, "w"), indent=2)


def bind_soul(name):
    """
    Creates a fresh soul and writes it to disk.
    This is the act of attunement — called once when the binding ring closes.
    """
    s = {
        "bound": True,
        "name": name,
        "bound_on": datetime.date.today().isoformat(),  # today's date as a string
        "times_spoken": 0
    }
    save_soul(s)
    return s


# Load the soul at startup. If it exists, CRUMB remembers who it's bound to.
soul = load_soul()


# ═════════════════════════════════════════════════════════════════════════════
# [§6 CLAUDE BRAIN]
# This function sends the user's words to the Claude AI and returns a reply.
#
# >>> API KEY SETUP:
#     1. Go to https://console.anthropic.com and create an account.
#     2. Generate an API key.
#     3. Paste it below where it says "PASTE_YOUR_ANTHROPIC_KEY_HERE"
# ═════════════════════════════════════════════════════════════════════════════

def ask_claude(user_text, name):
    """
    Sends the transcribed speech to Claude AI and returns CRUMB's reply.

    user_text — what the user said (already converted from audio to text).
    name      — the bound name, inserted into the system prompt.
    """
    try:
        import anthropic

        # >>> PASTE YOUR ANTHROPIC API KEY HERE (get one at console.anthropic.com)
        client = anthropic.Anthropic(api_key="PASTE_YOUR_ANTHROPIC_KEY_HERE")

        # Send the message to Claude with CRUMB's personality as context.
        # max_tokens limits how long the reply can be (roughly ~100 words).
        msg = client.messages.create(
            model="claude-haiku-4-5",   # fast, cheap model — good for a companion device
            max_tokens=171,
            system=CRUMB_SYSTEM_PROMPT.format(name=name),  # inject the real name
            messages=[{"role": "user", "content": user_text}],
        )

        # Extract just the text from the response and remove extra whitespace.
        return msg.content[0].text.strip()

    except Exception as e:
        # If anything goes wrong (no internet, bad key, etc.), show the error
        # and return a graceful fallback message instead of crashing.
        print("CLAUDE ERROR:", type(e).__name__, e)
        return "I cannot hear you clearly just now. Try once more."


# ═════════════════════════════════════════════════════════════════════════════
# [§7 TALK LOOP]
# The pipeline that powers the Ask CRUMB screen:
#   1. Record audio from the mic for RECORD_SECONDS seconds.
#   2. Send the audio to OpenAI Whisper to convert speech to text.
#   3. Send the text to Claude to get a reply.
#   4. Display the reply on screen.
#
# This runs in a background thread so the face animation never freezes
# while waiting for the mic or the AI to respond.
#
# >>> API KEY SETUP:
#     1. Go to https://platform.openai.com and create an account.
#     2. Generate an API key.
#     3. Paste it below where it says "PASTE_YOUR_OPENAI_KEY_HERE"
# ═════════════════════════════════════════════════════════════════════════════

def record_then_respond(typed_text=None):
    """
    Full pipeline: listen → transcribe → think → display reply.
    If typed_text is provided (dev mode), skip recording and use that instead.
    """
    # These are global variables — we modify them here and the main loop reads them.
    global talk_state, claude_reply, claude_thinking

    if typed_text is None:
        # ── STEP 1: LISTEN ──────────────────────────────────────────────────
        talk_state = "LISTENING"
        try:
            # Record RECORD_SECONDS seconds of mono audio at 44100 Hz.
            rec = sd.rec(
                int(RECORD_SECONDS * SAMPLE_RATE),
                samplerate=SAMPLE_RATE,
                channels=1,
                device=MIC_DEVICE
            )
            sd.wait()  # block here until recording is complete
        except Exception as e:
            print("RECORD ERROR:", e)
            claude_reply = "I could not hear at all. Check the mic."
            talk_state = "SPEAKING"
            time.sleep(2.0)
            talk_state = "RESTING"
            return

        # Sanity check: measure the loudest sample in the recording.
        # If it's near zero, the mic probably isn't working or nobody spoke.
        peak = float(np.max(np.abs(rec)))
        print(f"mic peak level: {peak:.4f}  (near 0 = silence)")
        if peak < 0.01:
            claude_reply = "The mic heard only silence. Speak louder, or check the device."
            talk_state = "SPEAKING"
            time.sleep(2.5)
            talk_state = "RESTING"
            return

        # ── STEP 2: TRANSCRIBE ───────────────────────────────────────────────
        # Convert the audio recording to text using OpenAI Whisper.
        talk_state = "THINKING"
        user_text = transcribe(rec)
        print(f"transcribed: {user_text!r}")

        if not user_text:
            # Whisper returned nothing — the words weren't clear enough.
            claude_reply = "I could not catch your words. Speak again."
            talk_state = "SPEAKING"
            time.sleep(2.0)
            talk_state = "RESTING"
            return
    else:
        # Dev mode: use the typed text directly instead of recording.
        user_text = typed_text
        print(f"typed input: {user_text!r}")

    # ── STEP 3: THINK ────────────────────────────────────────────────────────
    # Send the transcribed text to Claude and wait for a reply.
    claude_thinking = True
    talk_state = "THINKING"
    name = soul["name"] if soul else ARTIFICER_SETS_NAME
    claude_reply = ask_claude(user_text, name)
    print(f"claude said: {claude_reply!r}")
    claude_thinking = False

    # ── STEP 4: DISPLAY ──────────────────────────────────────────────────────
    # Show the reply on screen. The delay approximates reading time.
    # >>> TTS: This is where you would add text-to-speech (e.g. Amazon Polly).
    #          Generate and play audio here before setting talk_state to RESTING.
    talk_state = "SPEAKING"
    time.sleep(min(4.0, 1.5 + len(claude_reply) * 0.04))
    talk_state = "RESTING"


def transcribe(rec):
    """
    Converts a numpy audio recording to text using OpenAI Whisper API.
    Returns the transcribed string, or '' if anything goes wrong.
    """
    try:
        import scipy.io.wavfile as wavfile
        import openai

        # Whisper expects 16-bit PCM audio. Convert from float if needed.
        if rec.dtype != np.int16:
            rec_int = (np.clip(rec, -1.0, 1.0) * 32767).astype(np.int16)
        else:
            rec_int = rec

        # Write the recording to a temporary WAV file on disk.
        wavfile.write("/tmp/crumb_rec.wav", SAMPLE_RATE, rec_int)
        print(f"wrote /tmp/crumb_rec.wav, shape={rec_int.shape}, dtype={rec_int.dtype}")

        # >>> PASTE YOUR OPENAI API KEY HERE (get one at platform.openai.com)
        client = openai.OpenAI(api_key="PASTE_YOUR_OPENAI_KEY_HERE")

        # Send the WAV file to Whisper and get back the transcribed text.
        with open("/tmp/crumb_rec.wav", "rb") as f:
            r = client.audio.transcriptions.create(model="whisper-1", file=f)

        return r.text.strip()

    except Exception as e:
        # Always print errors so they're visible in the terminal for debugging.
        print("TRANSCRIBE ERROR:", type(e).__name__, e)
        return ""


# ═════════════════════════════════════════════════════════════════════════════
# [§8 MUSIC]
# Controls music playback using pygame's music channel.
# The music channel is separate from the sound effects channel,
# so beeps and music can play at the same time without conflict.
# ═════════════════════════════════════════════════════════════════════════════

def load_and_play(idx):
    """
    Loads the track at position idx in the TRACKS list and starts playing it.
    Returns True if it worked, False if the file wasn't found.
    """
    global music_playing_index, music_paused, music_error
    p = TRACKS[idx]["path"]

    # Check the file actually exists before trying to load it.
    if not os.path.exists(p):
        music_error = "file not found — check the path"
        return False

    try:
        pygame.mixer.music.load(p)
        pygame.mixer.music.play()
        music_playing_index = idx
        music_paused = False
        music_error = ""
        return True
    except Exception:
        music_error = "couldn't play (try .ogg)"
        return False


def toggle_pause():
    """Pauses the current track if playing, or resumes it if paused."""
    global music_paused
    if music_playing_index < 0:
        return  # nothing is playing, do nothing
    if music_paused:
        pygame.mixer.music.unpause()
        music_paused = False
    else:
        pygame.mixer.music.pause()
        music_paused = True


def change_track(d):
    """
    Moves to the next (+1) or previous (-1) track and starts playing it.
    Wraps around — going past the last track returns to the first.
    """
    global music_index
    music_index = (max(0, music_playing_index) + d) % len(TRACKS)
    load_and_play(music_index)


# ═════════════════════════════════════════════════════════════════════════════
# [§9 DRAW HELPERS]
# Functions that draw things on screen. Called every frame from the main loop.
# pygame draws from scratch every frame — nothing persists between frames.
# ═════════════════════════════════════════════════════════════════════════════

def filled_round_bar(s, c, x, y, w, h):
    """
    Draws a vertical rounded bar (pill shape).
    Used for the listening waveform animation.
    This is a workaround for pygame 1.9.6 which doesn't support border_radius.
    """
    if h < w:
        h = w  # minimum height equals width so the caps fit
    r = w // 2  # radius of the semicircle caps
    pygame.draw.rect(s, c, (x, y + r, w, h - 2 * r))      # middle rectangle
    pygame.draw.circle(s, c, (x + r, y + r), r)            # top cap
    pygame.draw.circle(s, c, (x + r, y + h - r), r)        # bottom cap


def draw_ring(cx, cy, radius, th, frac, color):
    """
    Draws a circular progress ring as a series of dots.
    Used during the binding ritual to show how far the hold has progressed.

    cx, cy  — center of the ring
    radius  — distance from center to ring
    th      — thickness (radius of each dot)
    frac    — how complete the ring is (0.0 = empty, 1.0 = full circle)
    color   — ring color
    """
    steps = max(2, int(120 * frac))  # number of dots to draw
    a0 = -math.pi / 2                # start at the top (12 o'clock)
    for i in range(steps):
        a = a0 + (2 * math.pi) * (i / 120)
        x = cx + int(math.cos(a) * radius)
        y = cy + int(math.sin(a) * radius)
        pygame.draw.circle(screen, color, (x, y), th)


def draw_face(cx, cy, scale, eye_openness, mode, t, happy=False, wake=1.0):
    """
    Draws CRUMB's face. Called every frame — the face is always animating.

    cx, cy        — center position of the face
    scale         — size multiplier (1.0 = full size, 0.3 = small corner face)
    eye_openness  — 0.0 = closed, 1.0 = fully open (used for blinking)
    mode          — "RESTING" | "LISTENING" | "THINKING" | "SPEAKING"
                    each mode changes what the mouth/eyes do
    t             — current time in seconds (drives animations)
    happy         — if True, shows big smile instead of small rest smile
    wake          — 0.0 to 1.0, fades the face in during the awakening sequence
    """
    eye_gap  = int(150 * scale)   # horizontal distance between eyes
    eye_r    = int((34 + (8 if mode == "LISTENING" else 0)) * scale)  # eye radius
    eye_off_y = int(30 * scale)   # how far above center the eyes sit

    # Draw cheek blush marks as soft ellipses with transparency.
    cheek = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    alpha = int(min(255, (150 if (mode == "LISTENING" or happy) else 90) * wake + 40 * wake))
    cw, ch = int(56 * scale), int(26 * scale)
    pygame.draw.ellipse(cheek, (CHEEK[0], CHEEK[1], CHEEK[2], alpha),
                        (cx - eye_gap - int(30 * scale), cy + int(5 * scale), cw, ch))
    pygame.draw.ellipse(cheek, (CHEEK[0], CHEEK[1], CHEEK[2], alpha),
                        (cx + eye_gap - int(26 * scale), cy + int(5 * scale), cw, ch))
    screen.blit(cheek, (0, 0))

    # Draw the eyes. Height is scaled by eye_openness for the blink animation.
    eh = int(eye_r * 2 * eye_openness)
    if eh < 4:
        eh = 4  # minimum eye height so it never fully disappears
    for dx in (-eye_gap, eye_gap):
        r = pygame.Rect(0, 0, eye_r * 2, eh)
        r.center = (cx + dx, cy - eye_off_y)
        pygame.draw.ellipse(screen, EYE, r)

    # Draw the mouth. Changes shape based on current mode.
    if mode == "SPEAKING":
        # Animated oval that pulses open and closed while speaking.
        oa = int(18 * scale * (0.5 + 0.5 * math.sin(t * 14)))
        pygame.draw.ellipse(screen, EYE,
            pygame.Rect(cx - int(40 * scale), cy + int(25 * scale),
                        int(80 * scale), int(20 * scale) + oa))
    elif mode == "THINKING":
        # Three dots that light up in sequence (like a "..." typing indicator).
        for i in range(3):
            on = (int(t * 3) % 3) == i
            c = TEXT_LIGHT if on else HINT
            pygame.draw.circle(screen, c, (cx - 20 + i * 20, cy + int(40 * scale)), 5)
    elif happy:
        # Big wide smile arc.
        pygame.draw.arc(screen, EYE,
            pygame.Rect(cx - int(55 * scale), cy + int(10 * scale),
                        int(110 * scale), int(80 * scale)),
            math.pi, 2 * math.pi, max(4, int(8 * scale)))
    else:
        # Default small resting smile arc.
        pygame.draw.arc(screen, EYE,
            pygame.Rect(cx - int(45 * scale), cy + int(20 * scale),
                        int(90 * scale), int(60 * scale)),
            math.pi, 2 * math.pi, max(3, int(6 * scale)))

    # Listening mode: animated waveform bars below the mouth.
    if mode == "LISTENING":
        for i in range(5):
            ph = math.sin(t * 6 + i * 0.9)           # each bar oscillates at a slightly different phase
            h = 10 + int(26 * (0.5 + 0.5 * ph))      # bar height pulses between 10 and 36px
            x = cx - (5 * 9) // 2 + i * 9            # spread bars evenly across center
            filled_round_bar(screen, WAVE, x, cy + int(30 * scale) - h // 2, 5, h)


def bg(now, wake=0.0):
    """
    Returns the background color for the current frame.
    Slowly breathes between SKIN and SKIN_BRIGHT on a 4-second cycle.
    The `wake` parameter adds extra brightness during the awakening sequence.
    """
    glow = (math.sin(now * (2 * math.pi / 4.0)) + 1) / 2  # oscillates 0 to 1
    return tuple(
        min(255, int(SKIN[i]
                     + (SKIN_BRIGHT[i] - SKIN[i]) * glow
                     + (GLOW_WAKE[i]   - SKIN[i]) * 0.4 * wake))
        for i in range(3)
    )


def do_blink(now):
    """
    Returns the current eye openness value (0.0 to 1.0) for natural blinking.
    Eyes close smoothly over 75ms, reopen over the next 75ms, then stay open
    for a random interval between 3 and 6 seconds.
    """
    global blinking, blink_start, last_blink, next_blink_in

    # Trigger a new blink if enough time has passed since the last one.
    if not blinking and (now - last_blink) > next_blink_in:
        blinking = True
        blink_start = now

    if blinking:
        e = now - blink_start  # seconds since blink started
        if e < 0.075:
            o = 1.0 - (e / 0.075)      # closing: 1.0 → 0.0
        elif e < 0.15:
            o = (e - 0.075) / 0.075    # opening: 0.0 → 1.0
        else:
            # Blink complete. Reset and schedule the next one.
            blinking = False
            last_blink = now
            next_blink_in = random.uniform(3, 6)
            o = 1.0
        return o

    return 1.0  # eyes fully open between blinks


def ctext(text, font, color, y):
    """Renders text centered horizontally at the given y position."""
    s = font.render(text, True, color)
    screen.blit(s, (SCREEN_W // 2 - s.get_width() // 2, y))


def touch_cue(now, label="touch to continue", dot=True):
    """
    Draws a pulsing text prompt and animated dot to indicate the screen
    is waiting for a touch. Only call this when you actually mean it —
    it tells the user something will happen when they touch.
    """
    # Pulse brightness using a sine wave on a ~3 second cycle.
    pulse = 0.45 + 0.55 * (0.5 + 0.5 * math.sin(now * 3.2))
    col = tuple(int(HINT[i] + (TEXT_LIGHT[i] - HINT[i]) * pulse) for i in range(3))

    # Draw the label text centered near the bottom of the screen.
    s = font_s.render(label, True, col)
    screen.blit(s, (SCREEN_W // 2 - s.get_width() // 2, SCREEN_H - 58))

    # Draw a pulsing ring dot above the label.
    if dot:
        r = int(10 + 5 * math.sin(now * 3.2))
        ring = pygame.Surface((60, 60), pygame.SRCALPHA)
        a = int(120 * pulse)
        pygame.draw.circle(ring, (TEXT_LIGHT[0], TEXT_LIGHT[1], TEXT_LIGHT[2], a),       (30, 30), r, 2)
        pygame.draw.circle(ring, (TEXT_LIGHT[0], TEXT_LIGHT[1], TEXT_LIGHT[2], min(255, a + 60)), (30, 30), 4)
        screen.blit(ring, (SCREEN_W // 2 - 30, SCREEN_H - 86 - 30))


def back_button_rect():
    """Returns the rectangle for the back button (top-left corner)."""
    return pygame.Rect(20, 16, 110, 40)


def draw_button(rect, label):
    """Draws a filled rectangle button with centered text."""
    pygame.draw.rect(screen, BTN, rect)
    t = font_s.render(label, True, TEXT_LIGHT)
    screen.blit(t, (rect.centerx - t.get_width() // 2, rect.centery - t.get_height() // 2))


# ═════════════════════════════════════════════════════════════════════════════
# [§10 STATE]
# All the variables that track what's happening right now.
# The main loop reads and updates these every frame.
# ═════════════════════════════════════════════════════════════════════════════

# Decide the starting stage based on whether a soul file exists.
# If bound: skip the ritual and show the welcome back screen.
# If unbound: start at sleeping and run the full ritual.
if soul and soul.get("bound"):
    stage = "welcome_back"
    soul["times_spoken"] = soul.get("times_spoken", 0) + 1  # increment visit count
    save_soul(soul)
else:
    stage = "sleeping"

# Records when the current stage started, used for timed transitions.
phase_start = time.time()

# These flags track which audio beats have fired in the current stage.
# Each beat only plays once — without this, a sound would replay every frame.
_beat = {"w1": False, "w2": False, "w3": False,
         "o1": False, "o2": False, "bg1": False, "bg2": False}
_last_hum = -1  # tracks the last hold-hum pitch step played

def reset_beats():
    """Resets all beat flags when entering a new stage."""
    for k in _beat:
        _beat[k] = False

# ── Ritual state ──────────────────────────────────────────────────────────────
hold_active   = False   # True while the user's finger is on the screen
hold_progress = 0.0     # 0.0 = no progress, 1.0 = binding complete

# ── Talk state ────────────────────────────────────────────────────────────────
# Controls what the face and text show during the Ask CRUMB pipeline.
talk_state    = "RESTING"   # RESTING | LISTENING | THINKING | SPEAKING
claude_reply  = ""           # the last reply from Claude, shown on screen
claude_thinking = False      # True while waiting for Claude to respond

# ── Menu state ────────────────────────────────────────────────────────────────
MENU_ITEMS = ["Timer", "Clock", "Music", "Ask CRUMB"]
menu_index = 0  # which item is currently highlighted

# ── Timer state ───────────────────────────────────────────────────────────────
timer_minutes         = 5      # default timer duration in minutes
timer_running         = False  # True while the countdown is active
timer_end             = 0.0    # the Unix timestamp when the timer expires
timer_celebrate_until = 0.0    # how long to show the celebration animation

# ── Music state ───────────────────────────────────────────────────────────────
music_index         = 0    # highlighted track in the list
music_playing_index = -1   # currently playing track (-1 = nothing playing)
music_paused        = False
music_error         = ""   # shown on screen if a file fails to load

# ── Animation state ───────────────────────────────────────────────────────────
start_ticks    = pygame.time.get_ticks()  # timestamp at startup, for the `now` timer
last_blink     = 0.0
next_blink_in  = random.uniform(3, 6)
blinking       = False
blink_start    = 0.0


# ═════════════════════════════════════════════════════════════════════════════
# [§11 STAGE TRANSITIONS]
# All stage changes go through go(). This ensures the right sound always
# plays when entering a stage, and resets the per-stage timers cleanly.
# ═════════════════════════════════════════════════════════════════════════════

def go(s):
    """
    Transitions to a new stage.
    Resets the phase timer, clears beat flags, and plays the entry sound.
    """
    global stage, phase_start, _last_hum
    stage = s
    phase_start = time.time()
    reset_beats()
    _last_hum = -1

    # Play the sound appropriate for entering this stage.
    if s == "waking":         voice.play(voice.wake)
    elif s == "bound_greet":  voice.play(voice.chime)
    elif s == "welcome_back": voice.play(voice.greet)
    elif s == "MENU":         voice.play(voice.nav)
    elif s in ("TIMER", "CLOCK", "MUSIC", "ASK"):
                              voice.play(voice.select)


# ═════════════════════════════════════════════════════════════════════════════
# [§12 MAIN LOOP]
# Runs 30 times per second. Each iteration:
#   1. Calculates timing variables.
#   2. Processes touch/keyboard events.
#   3. Draws the current stage.
#   4. Flips the display buffer (shows the frame).
# ═════════════════════════════════════════════════════════════════════════════

running = True
while running:
    # Time in seconds since startup — drives all animations.
    now  = (pygame.time.get_ticks() - start_ticks) / 1000.0
    # Time since the last frame in seconds — used for physics-style updates.
    dt   = clock.get_time() / 1000.0
    # Time in seconds since the current stage started.
    t_in = time.time() - phase_start
    # Center of the screen — used as the anchor for most drawing.
    cx, cy = SCREEN_W // 2, SCREEN_H // 2

    # ─────────────────────────────────────────────────────────────────────────
    # [§12.1 events]
    # Process all input events that happened since the last frame.
    # Touch events come in as mouse events on the Raspberry Pi touchscreen.
    # ─────────────────────────────────────────────────────────────────────────
    tap_down = False   # True for exactly one frame when a touch starts
    tap_pos  = None    # (x, y) position of the touch
    for e in pygame.event.get():

        if e.type == pygame.QUIT:
            # Window close button — exit cleanly.
            running = False

        elif e.type == pygame.MOUSEBUTTONDOWN:
            # A finger touched the screen (or mouse was clicked in dev mode).
            tap_down = True
            tap_pos  = e.pos
            hold_active = True

        elif e.type == pygame.MOUSEBUTTONUP:
            # Finger lifted — end hold tracking.
            hold_active = False

        elif e.type == pygame.KEYDOWN:
            k = e.key

            if k == pygame.K_ESCAPE:
                # >>> REMOVE FOR LUKE — no escape hatch in kiosk mode.
                # On the device there's no keyboard, so this can't be triggered anyway.
                if stage in ("TIMER", "CLOCK", "MUSIC", "MUSIC_NOW", "ASK"):
                    go("MENU")
                    timer_running = False
                else:
                    running = False

            elif k == pygame.K_t and stage == "ASK" and talk_state == "RESTING":
                # Dev shortcut: press T to type a question instead of speaking.
                def _typed():
                    txt = input("Type to CRUMB: ").strip()
                    if txt:
                        threading.Thread(
                            target=record_then_respond,
                            kwargs={"typed_text": txt},
                            daemon=True
                        ).start()
                threading.Thread(target=_typed, daemon=True).start()

            elif k == pygame.K_r and stage in (
                    "sleeping", "waking", "offer", "holding", "bound_greet", "welcome_back"):
                # >>> REMOVE FOR LUKE — deletes the soul file and resets to unbound.
                # On the device there's no keyboard, so this can't be triggered anyway.
                if os.path.exists(SOUL_PATH):
                    os.remove(SOUL_PATH)
                soul = None
                hold_progress = 0.0
                go("sleeping")

        elif e.type == pygame.KEYUP:
            if e.key == pygame.K_SPACE:
                hold_active = False

    # ─────────────────────────────────────────────────────────────────────────
    # [§12.2 ritual stages]
    # The awakening and binding sequence.
    # Flow: sleeping → waking → offer → holding → bound_greet → MENU
    #       (or on return visits: welcome_back → MENU)
    # ─────────────────────────────────────────────────────────────────────────

    if stage == "sleeping":
        # CRUMB is dormant. Face is nearly closed. Waiting for a touch to wake.
        screen.fill(bg(now, 0.0))
        draw_face(cx, cy - 20, 1.0, 0.12, "RESTING", now, wake=0.0)
        ctext("...", font_m, HINT, SCREEN_H - 130)
        touch_cue(now, "touch to wake")
        if tap_down:
            go("waking")

    elif stage == "waking":
        # CRUMB slowly wakes up over ~4 seconds, speaking short phrases.
        p = min(1.0, t_in / 3.5)  # progress from 0 to 1 over 3.5 seconds
        screen.fill(bg(now, p))
        draw_face(cx, cy - 20, 1.0, 0.12 + 0.88 * p, "RESTING", now, wake=p)
        if t_in < 1.6:
            if not _beat["w1"]: voice.play(voice.speak); _beat["w1"] = True
            ctext("\u2026oh.", font_m, TEXT_LIGHT, SCREEN_H - 120)
        elif t_in < 3.4:
            if not _beat["w2"]: voice.play(voice.speak); _beat["w2"] = True
            ctext("I have slept a long while.", font_m, TEXT_LIGHT, SCREEN_H - 120)
        else:
            if not _beat["w3"]: voice.play(voice.speak); _beat["w3"] = True
            ctext("Is someone there?", font_m, TEXT_LIGHT, SCREEN_H - 120)
            if t_in > 4.2:
                touch_cue(now, "touch me")
                if tap_down:
                    go("offer")

    elif stage == "offer":
        # CRUMB asks the user to place and hold their hand.
        screen.fill(bg(now, 1.0))
        draw_face(cx, cy - 20, 1.0, 1.0, "RESTING", now, wake=1.0)
        if t_in < 2.2:
            if not _beat["o1"]: voice.play(voice.speak); _beat["o1"] = True
            ctext("Place your hand upon me\u2026", font_m, TEXT_LIGHT, SCREEN_H - 120)
        else:
            if not _beat["o2"]: voice.play(voice.speak); _beat["o2"] = True
            ctext("\u2026and do not let go.", font_m, TEXT_LIGHT, SCREEN_H - 120)
            if t_in > 3.4:
                touch_cue(now, "press and hold")
                if hold_active:
                    go("holding")
                    hold_progress = 0.0

    elif stage == "holding":
        # The hold-to-bind stage. Progress fills a ring as long as the touch continues.
        # Releasing before completion sends back to offer.
        if hold_active:
            # Advance progress based on how much time has passed this frame.
            hold_progress = min(1.0, hold_progress + dt / HOLD_NEEDED)
            # Play a rising hum tone at each 1/12 step of progress.
            step = round(hold_progress * 12)
            if step != _last_hum:
                voice.play(voice.hum_at(hold_progress))
                _last_hum = step
        else:
            # Touch released before completion — reset.
            if hold_progress < 1.0:
                go("offer")

        wake = 0.4 + 0.6 * hold_progress
        screen.fill(bg(now, wake))
        draw_face(cx, cy - 30, 1.0, 1.0, "RESTING", now,
                  happy=(hold_progress > 0.5), wake=wake)
        draw_ring(cx, cy - 30, 160, 5, hold_progress, RING)

        if hold_progress < 1.0:
            ctext("the bond is forming\u2026", font_m, TEXT_LIGHT, SCREEN_H - 120)
            ctext("(keep holding)", font_s, HINT, SCREEN_H - 64)
        else:
            # Ring complete. Write the soul file and advance to the greeting.
            if soul is None:
                soul = bind_soul(ARTIFICER_SETS_NAME)
            go("bound_greet")

    elif stage == "bound_greet":
        # First-time greeting after a successful binding.
        screen.fill(bg(now, 1.0))
        draw_face(cx, cy - 20, 1.0, 1.0, "RESTING", now, happy=True, wake=1.0)
        if t_in < 2.2:
            if not _beat["bg1"]: voice.play(voice.speak); _beat["bg1"] = True
            ctext("I feel it. We are bound now.", font_m, TEXT_LIGHT, SCREEN_H - 120)
        else:
            if not _beat["bg2"]: voice.play(voice.greet); _beat["bg2"] = True
            ctext(f"I have been waiting for you, {soul['name']}.",
                  font_m, TEXT_LIGHT, SCREEN_H - 120)
            if t_in > 3.6:
                touch_cue(now, "touch to begin")
                if tap_down:
                    go("MENU")

    elif stage == "welcome_back":
        # Return visit greeting. Shows name and how many times they've spoken.
        screen.fill(bg(now, 1.0))
        draw_face(cx, cy - 20, 1.0, do_blink(now), "RESTING", now, happy=True)
        ctext(f"Welcome back, {soul['name']}.", font_m, TEXT_LIGHT, SCREEN_H - 130)
        ctext(f"(we have spoken {soul.get('times_spoken', 1)} times)",
              font_s, HINT, SCREEN_H - 90)
        if t_in > 1.2:
            touch_cue(now, "touch to begin")
            if tap_down:
                go("MENU")

    # ─────────────────────────────────────────────────────────────────────────
    # [§12.3 app stages]
    # The four tools accessible from the main menu.
    # ─────────────────────────────────────────────────────────────────────────

    elif stage == "MENU":
        # Main menu. Small face in the corner, list of options in the center.
        screen.fill(bg(now))
        draw_face(110, 90, 0.30, do_blink(now), "RESTING", now)
        ctext("menu", font_m, TEXT_LIGHT, 55)
        rects = []
        for i, item in enumerate(MENU_ITEMS):
            y = 130 + i * 58
            rect = pygame.Rect(cx - 200, y - 8, 400, 46)
            rects.append((rect, i))
            if i == menu_index:
                pygame.draw.rect(screen, SEL_BG, rect)  # highlight selected item
            lab = font_m.render(item, True, TEXT_LIGHT if i == menu_index else HINT)
            screen.blit(lab, (cx - lab.get_width() // 2, y))
        if tap_down and tap_pos:
            for rect, i in rects:
                if rect.collidepoint(tap_pos):
                    menu_index = i
                    voice.play(voice.select)
                    go({"Timer": "TIMER", "Clock": "CLOCK",
                        "Music": "MUSIC", "Ask CRUMB": "ASK"}[MENU_ITEMS[i]])
                    if stage == "TIMER":
                        timer_running = False
                    break

    elif stage == "TIMER":
        # Focus timer. Shows a countdown or the setup controls.
        screen.fill(bg(now))
        op = do_blink(now)

        if timer_running:
            remaining = timer_end - time.time()
            if remaining <= 0:
                # Timer expired — celebrate!
                timer_running = False
                timer_celebrate_until = time.time() + 4
                voice.play(voice.done)
            else:
                # Show the countdown clock.
                draw_face(110, 90, 0.32, op, "RESTING", now)
                m = int(remaining) // 60
                s = int(remaining) % 60
                big = font_l.render(f"{m:02d}:{s:02d}", True, AMBER)
                screen.blit(big, (cx - big.get_width() // 2, cy - 80))
                ctext("focus timer", font_s, AMBER_DIM, cy + 70)
            draw_button(back_button_rect(), "back")
            if tap_down and tap_pos and back_button_rect().collidepoint(tap_pos):
                voice.play(voice.back)
                go("MENU")
                timer_running = False

        elif time.time() < timer_celebrate_until:
            # Celebration animation: face wiggles happily.
            wig = int(6 * math.sin(now * 18))
            draw_face(cx + wig, cy - 20, 1.0, 1.0, "RESTING", now, happy=True)
            ctext("time's up!", font_m, AMBER, SCREEN_H - 110)

        else:
            # Setup screen: minus button, time display, plus button, start button.
            draw_face(110, 90, 0.30, op, "RESTING", now)
            big = font_l.render(f"{timer_minutes:02d}:00", True, AMBER)
            screen.blit(big, (cx - big.get_width() // 2, cy - 90))
            minus = pygame.Rect(cx - 200, cy - 70, 70, 70)
            plus  = pygame.Rect(cx + 130, cy - 70, 70, 70)
            pygame.draw.rect(screen, BTN, minus)
            pygame.draw.rect(screen, BTN, plus)
            mt = font_l.render("-", True, TEXT_LIGHT)
            pt = font_l.render("+", True, TEXT_LIGHT)
            screen.blit(mt, (minus.centerx - mt.get_width() // 2,
                             minus.centery - mt.get_height() // 2 - 6))
            screen.blit(pt, (plus.centerx  - pt.get_width()  // 2,
                             plus.centery  - pt.get_height() // 2 - 6))
            start = pygame.Rect(cx - 90, cy + 50, 180, 52)
            pygame.draw.rect(screen, SEL_BG, start)
            stt = font_m.render("start", True, TEXT_LIGHT)
            screen.blit(stt, (start.centerx - stt.get_width()  // 2,
                              start.centery - stt.get_height() // 2))
            draw_button(back_button_rect(), "back")
            if tap_down and tap_pos:
                if minus.collidepoint(tap_pos):
                    timer_minutes = max(1, timer_minutes - 1)
                    voice.play(voice.nav)
                elif plus.collidepoint(tap_pos):
                    timer_minutes = min(60, timer_minutes + 1)
                    voice.play(voice.nav)
                elif start.collidepoint(tap_pos):
                    timer_running = True
                    timer_end = time.time() + timer_minutes * 60
                    voice.play(voice.select)
                elif back_button_rect().collidepoint(tap_pos):
                    voice.play(voice.back)
                    go("MENU")

    elif stage == "CLOCK":
        # Simple clock. Shows current time in large text.
        screen.fill(bg(now))
        draw_face(110, 90, 0.30, do_blink(now), "RESTING", now)
        nowstr = datetime.datetime.now().strftime("%I:%M %p").lstrip("0")
        big = font_l.render(nowstr, True, TEXT_LIGHT)
        screen.blit(big, (cx - big.get_width() // 2, cy - 60))
        draw_button(back_button_rect(), "back")
        if tap_down and tap_pos and back_button_rect().collidepoint(tap_pos):
            voice.play(voice.back)
            go("MENU")

    elif stage == "MUSIC":
        # Track selection list.
        screen.fill(bg(now))
        draw_face(110, 90, 0.30, do_blink(now), "RESTING", now)
        ctext("music", font_m, TEXT_LIGHT, 55)
        rects = []
        for i, tr in enumerate(TRACKS):
            y = 130 + i * 58
            rect = pygame.Rect(cx - 200, y - 8, 400, 46)
            rects.append((rect, i))
            if i == music_index:
                pygame.draw.rect(screen, SEL_BG, rect)
            mark = "  \u266a" if i == music_playing_index else ""  # music note if playing
            lab = font_m.render(tr["name"] + mark, True,
                                TEXT_LIGHT if i == music_index else HINT)
            screen.blit(lab, (cx - lab.get_width() // 2, y))
        if music_error:
            ctext(music_error, font_s, AMBER_DIM, SCREEN_H - 62)
        draw_button(back_button_rect(), "back")
        if tap_down and tap_pos:
            if back_button_rect().collidepoint(tap_pos):
                voice.play(voice.back)
                go("MENU")
            else:
                for rect, i in rects:
                    if rect.collidepoint(tap_pos):
                        music_index = i
                        voice.play(voice.select)
                        if load_and_play(i):
                            go("MUSIC_NOW")
                        break

    elif stage == "MUSIC_NOW":
        # Now playing screen with transport controls.
        screen.fill(bg(now))
        draw_face(110, 90, 0.30, do_blink(now), "RESTING", now)
        tr = TRACKS[music_playing_index] if music_playing_index >= 0 else {"name": "\u2014"}
        ctext(tr["name"], font_m, TEXT_LIGHT, cy - 110)

        # Progress bar — assumes average track length of 4 minutes (240 seconds).
        pos_ms  = pygame.mixer.music.get_pos()
        elapsed = pos_ms / 1000.0 if pos_ms >= 0 else 0.0
        frac    = max(0.0, min(1.0, elapsed / 240.0))
        bw, bh  = 460, 8
        bx, by  = cx - bw // 2, cy - 40
        pygame.draw.rect(screen, BAR_BG,   (bx, by, bw, bh))
        pygame.draw.rect(screen, BAR_FILL, (bx, by, int(bw * frac), bh))
        el = font_s.render(f"{int(elapsed)//60}:{int(elapsed)%60:02d}", True, HINT)
        screen.blit(el, (bx, by + 14))

        # Status label: playing / paused / done.
        status = ("paused" if music_paused else
                  ("done"  if (music_playing_index >= 0 and not music_paused
                               and not pygame.mixer.music.get_busy()) else "playing"))
        st = font_s.render(status, True, AMBER_DIM)
        screen.blit(st, (cx - st.get_width() // 2, cy - 70))

        # Transport buttons: previous, play/pause, next.
        prev_b = pygame.Rect(cx - 170, cy + 30, 80, 60)
        pp_b   = pygame.Rect(cx - 40,  cy + 30, 80, 60)
        next_b = pygame.Rect(cx + 90,  cy + 30, 80, 60)
        for b in (prev_b, pp_b, next_b):
            pygame.draw.rect(screen, BTN, b)
        pl  = font_m.render("<<", True, TEXT_LIGHT)
        ppl = font_m.render("II" if not music_paused else ">", True, TEXT_LIGHT)
        nx  = font_m.render(">>", True, TEXT_LIGHT)
        screen.blit(pl,  (prev_b.centerx - pl.get_width()  // 2, prev_b.centery - pl.get_height()  // 2))
        screen.blit(ppl, (pp_b.centerx   - ppl.get_width() // 2, pp_b.centery   - ppl.get_height() // 2))
        screen.blit(nx,  (next_b.centerx - nx.get_width()  // 2, next_b.centery - nx.get_height()  // 2))
        draw_button(back_button_rect(), "back")
        if tap_down and tap_pos:
            if prev_b.collidepoint(tap_pos):  change_track(-1); voice.play(voice.nav)
            elif pp_b.collidepoint(tap_pos):  toggle_pause();   voice.play(voice.nav)
            elif next_b.collidepoint(tap_pos): change_track(+1); voice.play(voice.nav)
            elif back_button_rect().collidepoint(tap_pos):
                voice.play(voice.back)
                go("MUSIC")

    elif stage == "ASK":
        # Ask CRUMB screen. Tap to record, wait for AI response, reply shown on screen.
        screen.fill(bg(now))
        draw_face(cx, cy - 30, 1.0, do_blink(now), talk_state, now)

        if talk_state == "RESTING":
            if claude_reply:
                # Word-wrap the reply into lines that fit the screen width.
                MAX_LINES = 6
                words = claude_reply.split()
                lines = []
                line  = ""
                for w in words:
                    test = (line + " " + w).strip()
                    if font_s.size(test)[0] > SCREEN_W - 80:
                        lines.append(line)
                        line = w
                    else:
                        line = test
                if line:
                    lines.append(line)

                # Truncate to MAX_LINES and add ellipsis if the reply was cut off.
                if len(lines) > MAX_LINES:
                    lines = lines[:MAX_LINES]
                    lines[-1] = lines[-1][:max(0, len(lines[-1]) - 1)] + "\u2026"

                # Center the text block vertically in the space below the face.
                line_h  = 26
                block_h = len(lines) * line_h   # total height of the text block
                space_top = cy + 40             # bottom of the face area
                space_bot = SCREEN_H - 100      # top of the hint/button area
                start_y   = space_top + (space_bot - space_top - block_h) // 2

                for i, ln in enumerate(lines):
                    ctext(ln, font_s, TEXT_LIGHT, start_y + i * 26)

            ctext("touch me to speak", font_s, HINT, SCREEN_H - 92)

        elif talk_state == "LISTENING":
            ctext("listening\u2026", font_s, HINT, cy + 90)
        elif talk_state == "THINKING":
            ctext("thinking\u2026",  font_s, HINT, cy + 90)
        elif talk_state == "SPEAKING":
            # Show a preview of the reply while in the SPEAKING state.
            ctext(claude_reply[:60] + ("\u2026" if len(claude_reply) > 60 else ""),
                  font_s, TEXT_LIGHT, cy + 90)

        draw_button(back_button_rect(), "back")
        if tap_down:
            if tap_pos and back_button_rect().collidepoint(tap_pos):
                voice.play(voice.back)
                go("MENU")
            elif talk_state == "RESTING":
                # Start recording in a background thread so the face keeps animating.
                voice.play(voice.nav)
                threading.Thread(target=record_then_respond, daemon=True).start()

    # ── End of frame ──────────────────────────────────────────────────────────
    pygame.display.flip()  # show everything drawn this frame
    clock.tick(30)         # wait until 1/30th of a second has passed (30 fps cap)


# ── Cleanup ───────────────────────────────────────────────────────────────────
# Stop music and shut down pygame cleanly when the loop exits.
pygame.mixer.music.stop()
pygame.quit()
sys.exit()
