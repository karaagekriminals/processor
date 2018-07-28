from mido import Message 
import mido as midolib
#Tested on windows with LoopBe1 emulator
#Mido used for midi, this library requires:
# https://mido.readthedocs.io/en/latest/installing.html
import time

## ************* Instructions ********
# 1.) set the output port first using the setOutputPort method
# 2.) use startNote(pitch) to begin playing a note and then stopNote(pitch) to stop it playing


#For middle C use note = 60
outport = None
def setOutputPort(*args):
    #Optional argument of MidiOutput Port.
    #If this isn't used then it picks the first port 
    #from a list of all available.
    global outport
    if not args:
        outport = midolib.open_output(midolib.get_output_names()[0])
    else:
        outport = midolib.open_output(args[1])

#Must setOutputPort before Playing Note
def NoteCtrl(msgtype,note,time):
    msg = Message(msgtype, note=note,velocity=vel) 
    outport.send(msg)

#Start note - pass in value (middle C is 60)
def startNote(note,velocity):
    NoteCtrl('note_on',note,0)

#Stop note function - pass in value (middle C is 60)
def stopNote(note):
    NoteCtrl('note_off',note,0)

## For demo purposes only, don't call this function
def MidiDemo():
    msg = Message('note_on', note=60) 
    outport = midolib.open_output(midolib.get_output_names()[0])
    print(midolib.get_input_names()[0])
    while True:
        time.sleep(0.5)
        outport.send(msg)