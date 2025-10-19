import json
import random
import os

# --- Configuration ---
MAP_SIZE = 10
FILE_NAME = 'map_state.json'
EMPTY = 0
HOUSE = 'H'
ONLINE_SHOPPING = "W"  # <-- CHANGED TO CAPITAL 'W' for warehouse
SHOPPING = "F"  # factory
EATING_OUT = "M"  # WHACKDONALD'S (Changed to 'M' for consistency)
NIGHT = "N"  # nightclub
GROCERIES = "T"  # A TREE (Added, but not currently used)

# List of all available non-house building types
ALL_BUILDING_TYPES = [ONLINE_SHOPPING, SHOPPING, EATING_OUT, NIGHT, GROCERIES]


def load_game_state(file_name):
    """Loads game state from a JSON file and ensures all necessary keys exist."""

    # Define default values for a new map
    initial_map = [[EMPTY] * MAP_SIZE for _ in range(MAP_SIZE)]
    default_state = {
        'map_data': initial_map,
        'house_placed': False,
        'house_location': None,
        # Keys added for tracking other buildings (for backward compatibility)
        'buildings_placed': False,
        'building_locations': []
    }

    if os.path.exists(file_name):
        print(f"Loading existing state from {file_name}...")
        with open(file_name, 'r') as f:
            loaded_state = json.load(f)

        # Compatibility Check: Add missing keys from default state
        for key, default_value in default_state.items():
            if key not in loaded_state:
                loaded_state[key] = default_value
                print(f"  --> Added missing key '{key}' for compatibility.")

        return loaded_state
    else:
        print("No existing state found. Initializing new map...")
        return default_state


def save_game_state(state, file_name):
    """Saves the current game state to a JSON file."""
    with open(file_name, 'w') as f:
        json.dump(state, f, indent=4)
    print(f"State successfully saved to {file_name}")


def place_house(state):
    """Randomly generates and places the house if it hasn't been placed."""
    if state['house_placed']:
        print(f"House already placed at {state['house_location']}. Skipping placement.")
        return state

    # Determine random coordinates (0 to 9)
    row = random.randint(0, MAP_SIZE - 1)
    col = random.randint(0, MAP_SIZE - 1)

    # Update the map and state variables
    state['map_data'][row][col] = HOUSE
    state['house_placed'] = True
    state['house_location'] = [row, col]  # Store as a list for JSON serialization

    print(f"House randomly placed at Row: {row}, Col: {col}")
    return state


def place_building_random(state, building_type):
    """
    Generates a random, unoccupied location and places the specified building.
    Returns the updated state and the location [row, col] of the placement.
    """
    # Repeatedly attempt to find an empty spot
    while True:
        row = random.randint(0, MAP_SIZE - 1)
        col = random.randint(0, MAP_SIZE - 1)

        # Check if the spot is EMPTY
        if state['map_data'][row][col] == EMPTY:
            # Place the building and exit the loop
            state['map_data'][row][col] = building_type
            location = [row, col, building_type]  # Include type in the location record

            print(f"Building {building_type} randomly placed at Row: {row}, Col: {col}")
            return state, location  # Return the updated state and the location
def add_building(building_type, game_state):
    game_state,new_location = place_building_random(game_state, building_type)
    # Manually update the building_locations list and flag:
    game_state['building_locations'].append(new_location)
    game_state['buildings_placed'] = True


# --- Main Logic (Corrected to run placement only once) ---

# 1. Load the state from the file
game_state = load_game_state(FILE_NAME)

# 2. Run the house placement logic
game_state = place_house(game_state)

# 3. INITIAL BUILDING PLACEMENT: #uncomment this if you need to add a new building

#add_building(SHOPPING, game_state)



# 4. Save the updated state permanently
save_game_state(game_state, FILE_NAME)

# 5. Display the result
