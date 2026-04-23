# saves.py
# Module for handling game save data persistence
import os
import config

# Get base directory for save file path
base = os.path.dirname(__file__)
# Path to the save file
save_path = os.path.join(base, "save.txt")

# Default save data
owned_skins  = ["0_Default.png"]
equipped_skin = "0_Default.png"
secret_lebron_unlocked = False
wins = 0
bg_volume = config.DEFAULT_BG_VOLUME
sfx_volume = config.DEFAULT_SFX_VOLUME
step_sounds_enabled = config.DEFAULT_STEP_SOUNDS_ENABLED
color_change_enabled = config.DEFAULT_COLOR_CHANGE_ENABLED

# Function to save all data to file
def save_data():
    # Open save file for writing
    with open(save_path, "w") as fh:
        # Write wins
        fh.write(f"wins={wins}\n")
        # Write equipped skin
        fh.write(f"equipped_skin={equipped_skin}\n")
        # Write owned skins as comma-separated
        fh.write(f"owned_skins={','.join(owned_skins)}\n")
        # Write secret unlock status
        fh.write(f"secret_lebron_unlocked={'1' if secret_lebron_unlocked else '0'}\n")
        fh.write(f"bg_volume={bg_volume}\n")
        fh.write(f"sfx_volume={sfx_volume}\n")
        fh.write(f"step_sounds_enabled={'1' if step_sounds_enabled else '0'}\n")
        fh.write(f"color_change_enabled={'1' if color_change_enabled else '0'}\n")

# Function to load data from file
def load_data():
    # Declare globals to modify
    global owned_skins, equipped_skin, secret_lebron_unlocked, wins, bg_volume, sfx_volume, step_sounds_enabled, color_change_enabled
    # Check if save file exists
    if os.path.exists(save_path):
        # Open and read file
        with open(save_path, "r") as fh:
            for line in fh:
                # Strip whitespace
                line = line.strip()
                # Check for key=value format
                if "=" in line:
                    key, value = line.split("=", 1)
                    if key == "wins":
                        # Parse wins as int, default 0 on error
                        try:
                            wins = int(value)
                        except ValueError:
                            wins = 0
                    elif key == "equipped_skin":
                        equipped_skin = value
                    elif key == "owned_skins":
                        # Split owned skins by comma
                        owned_skins = [skin for skin in value.split(",") if skin]
                    elif key == "secret_lebron_unlocked":
                        # Parse as boolean
                        secret_lebron_unlocked = value == "1"
                    elif key == "bg_volume":
                        try:
                            bg_volume = max(0.0, min(1.0, float(value)))
                        except ValueError:
                            bg_volume = config.DEFAULT_BG_VOLUME
                    elif key == "sfx_volume":
                        try:
                            sfx_volume = max(0.0, min(1.0, float(value)))
                        except ValueError:
                            sfx_volume = config.DEFAULT_SFX_VOLUME
                    elif key == "step_sounds_enabled":
                        step_sounds_enabled = value == "1"
                    elif key == "color_change_enabled":
                        color_change_enabled = value == "1"

    if not owned_skins:
        owned_skins = ["0_Default.png"]
    if equipped_skin not in owned_skins:
        equipped_skin = owned_skins[0]

# Load data on module import
load_data()

# Function to save wins specifically
def save_wins():
    save_data()

# Function to save skin state
def save_skin_state():
    save_data()

def save_settings():
    save_data()
