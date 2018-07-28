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

# Constants.

STARTING_NOTE = 48
NOTE_PROGRESSION = [3, 2, 2, 3, 2]
OCTAVES = 1
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

    client.subscribe('euler/98072d27a984')
    # client.subscribe('telemetry/98072d27a984/movement')


def on_message(client, userdata, msg):
    """Callback for PUBLISH message received from server."""

    json_data = json.loads(msg.payload)

    # Calculate pitch.

    heading = (math.degrees(json_data["heading"]) + 210) % 180
    pitch = (math.degrees(json_data["pitch"]) + 270) % 180
    roll = (math.degrees(json_data["roll"]) + 180) % 180

    # Calculate percentages as wholes.

    heading = 1000 - math.floor(1000 * heading / 180)
    pitch = math.floor(1000 * pitch / 180)
    roll = max(750, math.floor(1000 * roll / 180))

    # Set the current pitch and velocity.

    curr_note = determine_note(pitch)
    curr_velo = determine_velo(roll)


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


def determine_velo(roll):
    """Use message data to determine a velocity."""

    return math.floor(roll / 10)


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

            print(curr_note)

            prev_note = curr_note
            curr_note = None
