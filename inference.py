import torch
import BPN
import miditoolkit
import numpy
import WindUper
from config import Config as config

def ReadMidi(midipath):
    mido_obj = miditoolkit.midi.parser.MidiFile(midipath)
    NoteSet = []
    #lastEnd = mido_obj.instruments[0].notes[0].start #Bug bypass
    lastStart = -1
    for i in mido_obj.instruments[0].notes:
        if i.start != lastStart:
            #Atarashi Note
            lastStart = i.start
            NoteSet.append([i.pitch, i.velocity, 0, 0, 0, 0])
            t = 2
        else:
            if t < 5:
                NoteSet[len(NoteSet)-1][t] = i.pitch
                NoteSet[len(NoteSet)-1][t+1] = i.velocity
                t = t + 2
    return NoteSet

myNet = BPN.myBPN()
myNet.load_state_dict(torch.load(config.pthsave))
X = ReadMidi('tryM.midi')[0:100]
X = numpy.array(X, dtype=object).astype(float)
X = torch.tensor(X).float() / 128
Y = myNet(X.view(1, 600)).view(100, 6).detach() * 128
WindUper.ArrayToMidi(Y, 'niceB.midi')
