# saves.py
# Module for handling game save data persistence
import os

# Get base directory for save file path
base = os.path.dirname(__file__)
# Path to the save file
save_path = os.path.join(base, "save.txt")

# Default save data
owned_skins  = ["0_Default.png"]
equipped_skin = "0_Default.png"
secret_lebron_unlocked = False
wins = 0

# Function to save all data to file
def save_data():
    # Open save file for writing
    with open(save_path, "w") as fh:
        # Write wins
        fh.write(f"wins={wins}
")
        # Write equipped skin
        fh.write(f"equipped_skin={equipped_skin}
")
        # Write owned skins as comma-separated
        fh.write(f"owned_skins={,.join(owned_skins)}
")
        # Write secret unlock status
        fh.write(f"secret_lebron_unlocked={"1" if secret_lebron_unlocked else "0"}
")
        fh.write(f"bg_volume={bg_volume}
")
        fh.write(f"sfx_volume={sfx_volume}
")
        fh.write(f"step_sounds_enabled={"1" if step_sounds_enabled else "0"}
")
        fh.write(f"color_change_enabled={"1" if color_change_enabled else "0"}
")
        fh.write(f"step_sounds_enabled={"1" if step_sounds_enabled else "0"}
")
        fh.write(f"color_change_enabled={"1" if color_change_enabled else "0"}
")
")
")
        fh.write(f"step_sounds_enabled={"1" if step_sounds_enabled else "0"}
")
")
        fh.write(f"color_change_enabled={"1" if color_change_enabled else "0"}
")
")

# Function to load data from file
def load_data():
    # Declare globals to modify
    global owned_skins, equipped_skin, secret_lebron_unlocked, wins
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
                        owned_skins = value.split(",")
                    elif key == "secret_lebron_unlocked":
                        # Parse as boolean
                        secret_lebron_unlocked = value == "1"
                    elif key == "bg_volume":
                        try:
                            bg_volume = float(value)
                        except ValueError:
                            bg_volume = 1.0
                    elif key == "sfx_volume":
                        try:
                            sfx_volume = float(value)
                        except ValueError:
                            sfx_volume = 1.0
                    elif key == "step_sounds_enabled":
                        step_sounds_enabled = value == "1"
                    elif key == "color_change_enabled":
                        color_change_enabled = value == "1"

# Load data on module import
load_data()

# Function to save wins specifically
def save_wins():
    save_data()

# Function to save skin state
def save_skin_state():
def save_settings():
    save_data()
    save_data()
