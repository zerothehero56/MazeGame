# sounds.py
# This module handles loading and managing sound effects for the game
import os
import pygame

# Initialize Pygame mixer for audio playback
pygame.mixer.init()
# Set number of mixer channels to allow multiple sounds
pygame.mixer.set_num_channels(64)

# Get the base directory of this script
BASE_DIR = os.path.dirname(__file__)
# Define the sounds directory relative to base
SOUNDS_DIR = os.path.join(BASE_DIR, "sounds")

# Placeholders for sound objects; actual loading is deferred
sound_fah = None
sound_idk = None
sound_win = None
sound_cmonman = None
sound_flight = None
sound_rizz = None
sound_ankle = None
sound_sike = None
sound_talary = None
sound_siren = None
sound_weave = None
sound_lebronshine = None
sound_rizzy = None
sound_default = None
sound_200 = None
sound_300 = None

sounds_loaded = False

# Function to load a sound with fallback filenames
def load_sound(*filenames):
    # Loop through each filename option
    for filename in filenames:
        # Construct full path to the sound file
        path = os.path.join(SOUNDS_DIR, filename)
        # Check if the file exists
        if os.path.exists(path):
            # Try to load the sound
            try:
                return pygame.mixer.Sound(path)
            # If loading fails, continue to next filename
            except (pygame.error, OSError):
                continue
    # Return None if no file could be loaded
    return None

# Function to load all configured sounds
def load_all_sounds():
    global sounds_loaded
    # Load remaining sounds until finished
    while not sounds_loaded:
        load_next_sound()

# Sound queue for incremental loading
sound_queue = [
    ("sound_fah",       ("fah.wav", )),
    ("sound_idk",       ("IDK.mp3", )),
    ("sound_win",       ("win.wav",)),
    ("sound_cmonman",   ("thastooeas.wav",)),
    ("sound_flight",    ("LEBRONN.wav", )),
    ("sound_rizz",      ("rizz.mp3",)),
    ("sound_ankle",     ("brokenankle.mp3",)),
    ("sound_sike",      ("sike.mp3",)),
    ("sound_talary",    ("takealookaroundyou.mp3",)),
    ("sound_siren",     ("siren.mp3",)),
    ("sound_weave",     ("weave.wav",)),
    ("sound_aycaramba",  ("aycaramba.wav",)),
    ("sound_eatmyshorts", ("eatmyshorts.wav",)),
    ("sound_lebronshine", ("LebronShine.wav",)),
    ("sound_rizzy",     ("rizzy.mp3",)),
    ("sound_default",   ("defaulte.mp3",)),
    ("sound_200",       ("200.wav",)),
    ("sound_300",       ("300.wav",)),
]

load_index = 0

# Load the next sound in the queue, one per frame
def load_next_sound():
    global load_index, sounds_loaded
    global sound_fah, sound_idk, sound_win, sound_cmonman, sound_flight
    global sound_rizz, sound_ankle, sound_sike, sound_talary, sound_siren
    global sound_weave, sound_lebronshine, sound_rizzy, sound_default

    if sounds_loaded:
        return

    if load_index >= len(sound_queue):
        sounds_loaded = True
        return

    name, filenames = sound_queue[load_index]
    sound_obj = load_sound(*filenames)
    globals()[name] = sound_obj

    # Set volume for specific sounds when loaded
    if name == "sound_fah" and sound_obj:
        sound_obj.set_volume(0.15)
    if name == "sound_idk" and sound_obj:
        sound_obj.set_volume(0.15)
    if name == "sound_flight" and sound_obj:
        sound_obj.set_volume(0.1)
    if name == "sound_default" and sound_obj:
        sound_obj.set_volume(0.1)

    load_index += 1
    if load_index >= len(sound_queue):
        sounds_loaded = True
# Define mixer channels for sound playback
channel = pygame.mixer.Channel(1)
canel   = pygame.mixer.Channel(4)
chanel  = pygame.mixer.Channel(2)
cannel  = pygame.mixer.Channel(3)
