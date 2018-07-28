"""Play MIDI signals to a virtual MIDI instrument."""

from mido import Message
import mido as midolib

import time

# We need an output port to play anything to and it needs to be global.

outport = None


# Required set-up for MIDI output.


def set_output_port(*args):
    """Set the output port. Set to default port if not specified."""

    global outport

    if not args:
        outport = midolib.open_output(midolib.get_output_names()[0])
    else:
        outport = midolib.open_output(args[1])


# Public methods.


def start_note(note, velocity, channel):
    """Play a note and pitch."""

    __note_control('note_on', note, velocity, channel)


def stop_note(note, channel):
    """Stop a playing note."""

    __note_control('note_off', note, 0, channel)


# Private helper methods.


def __note_control(msgtype, note, velocity, channel):
    if not outport:
        raise NameError("Output port name 'outport' is not defined. Make " +
                        "sure you call 'set_output_port()'")

    msg = Message(msgtype, note=note, velocity=velocity, channel=channel)
    outport.send(msg)


# Demo function definition.


def __demo():
    """Send a beeping middle C note repetitively to the MIDI port."""

    msg = Message('note_on', note=60)
    set_output_port()

    print("Running on: " + str(midolib.get_input_names()[0]))

    start_note(68, 100, 0)
    time.sleep(0.5)

    while True:
        stop_note(68, 0)
        time.sleep(0.5)
        start_note(68, 100, 0)
        time.sleep(0.5)


if __name__ == "__main__":
    __demo()
