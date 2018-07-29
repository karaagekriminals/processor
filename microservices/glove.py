"""Pipeline for glove to translate MQTT data to pitch/velocity."""

import paho.mqtt.client as mqtt
from utils import midi2daw

import json
import math
import random
from time import sleep

# We store the previous note to ensure no note plays indefinitely.

prev_note = None
curr_note = None
curr_velo = None

prev_filter = None
curr_filter = None

prev_fader = None
curr_fader = None

# Define scales.

PENTATONIC_MAJOR = [3, 2, 2, 3, 2]
MAJOR = [2, 2, 1, 2, 2, 2, 1]
MAJOR_TRIAD = [4, 3, 5]
MAJOR_SEVENTH = [4, 3, 4, 1]

# Define note ranges.

STARTING_NOTE = 67
NOTE_PROGRESSION = PENTATONIC_MAJOR
OCTAVES = 2
NOTES_IN_KEY = [STARTING_NOTE]

# Create the octaves of the scale.

running_sum = STARTING_NOTE

for i in range(OCTAVES):
    for addition in NOTE_PROGRESSION:
        running_sum += addition

        NOTES_IN_KEY.append(running_sum)


def on_connect(client, userdata, flags, rc):
    """Callback for client connects to the broker."""

    # Subscribe to the topic(s).

    client.subscribe('euler/c4be8471a302')
    client.subscribe('euler/98072d3b1a82')


def on_message(client, userdata, msg):
    """Callback for PUBLISH message received from server."""

    global curr_note
    global curr_velo
    global curr_filter
    global curr_fader

    json_data = json.loads(msg.payload)

    # Calculate pitch and roll.

    pitch = (math.degrees(json_data["pitch"]) + 270) % 180
    roll = (math.degrees(json_data["roll"]) + 380) % 180

    if "98" in msg.topic:
        # Calculate percentages as wholes.

        pitch = round(1000 * pitch / 180)
        roll = round(1000 * roll / 180)

        # Set the current faders.

        curr_fader = round(pitch / 10)
    else:
        # Calculate percentages as wholes.

        pitch = round(1000 * pitch / 180)
        roll = round(1000 * roll / 180)

        # Set the current pitch and velocity.

        curr_note = determine_note(pitch)
        curr_velo = 90

        # Send to the second channel the control for the filter.

        curr_filter = round(roll / 10)


def initiate_client():
    """Initiate client to connect to the MQTT server."""

    # TODO: Remove hardcoding.

    client = mqtt.Client("myclient")
    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set("admin", "secretpassword")

    host_name = "10.77.0.18"
    client.connect_async(host_name, port=1883,
                         keepalive=60, bind_address="")
    client.loop_start()


def determine_note(pitch):
    """Use message data to determine a pitch."""

    index = math.floor(len(NOTES_IN_KEY) * (pitch / 1000))

    return NOTES_IN_KEY[index]


if __name__ == "__main__":
    initiate_client()
    midi2daw.set_output_port()

    # Keep server running indefinitely.

    while True:
        """
        Every tenth of a second, we check if we have a different pitch than
        we had previously. If we do, we stop the previous note and start a new
        one using the sensor data.
        """

        sleep(0.005)

        if (curr_note != prev_note) and curr_note:
            if prev_note:
                # TODO: Remove channel hardcoding.

                midi2daw.stop_note(prev_note, 0)

            midi2daw.start_note(curr_note, curr_velo, 0)

            # print(curr_note)

            prev_note = curr_note
            curr_note = None

        if (curr_filter != prev_filter) and curr_filter:
            if prev_filter:
                # TODO: Remove channel hardcoding.

                midi2daw.change_knob(0, prev_filter)

            midi2daw.change_knob(0, curr_filter)

            prev_filter = curr_filter
            curr_filter = None

        if (curr_fader != prev_fader) and curr_fader:
            if prev_fader:
                midi2daw.change_knob(2, prev_fader)

            midi2daw.change_knob(2, curr_fader)

            print(curr_fader)

            prev_fader = curr_fader
            curr_fader = None
