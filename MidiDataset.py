import torch
import miditoolkit
import os

class midiData():
    def __init__(self, pathdir, batchsize):
        self.midiPath = []
        midiList = os.listdir(pathdir)
        self.batchsize = batchsize
        for i in range(len(midiList)):
            self.midiPath.append(pathdir + '/' + midiList[i])

    def ReadMidi(self, idx):
        mido_obj = miditoolkit.midi.parser.MidiFile(self.midiPath[idx])
        NoteSet = []
        lastEnd = mido_obj.instruments[0].notes[0].start #Bug bypass
        for i in mido_obj.instruments[0].notes:
            if i.start == lastEnd:
                #Atarashi Note
                lastEnd = i.end
                NoteSet.append([i.pitch, i.velocity, 0, 0, 0, 0])
                t = 2
            else:
                if t < 5:
                    NoteSet[len(NoteSet)-1][t] = i.pitch
                    NoteSet[len(NoteSet)-1][t+1] = i.velocity
                    t = t + 2
        return NoteSet

    def MakeBatch(self, batchID):
        myBatch = []
        for i in range(self.batchsize):
            tempID = (batchID + i) % len(self.midiPath)
            myBatch.append(self.ReadMidi(tempID))
        return myBatch


Dataset = midiData('/hdd2/lmd/0/', 5)
sample = Dataset.MakeBatch(0)
print(sample)
