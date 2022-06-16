import torch
import miditoolkit
import os

class midiData():
    def __init__(self, MelodyDir, BassDir, batchsize):
        self.MelodyPath = []
        self.BassPath = []
        melodyList = os.listdir(MelodyDir)
        BassList = os.listdir(BassDir)
        self.batchsize = batchsize
        for i in melodyList:
            if i in BassList:
                self.MelodyPath.append(MelodyDir + '/' + i)
                self.BassPath.append(BassDir + '/' + i)

    def ReadMidi(self, track, idx):
        if track == 'M':
            mido_obj = miditoolkit.midi.parser.MidiFile(self.MelodyPath[idx])
        else:
            mido_obj = miditoolkit.midi.parser.MidiFile(self.BassPath[idx])
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
    
    def DataClean(self):
        killed = 0
        for i in range(len(self.MelodyPath)):
            try:
                testResultM = self.ReadMidi('M', i - killed)
                testResultB = self.ReadMidi('B', i - killed)
                if len(testResultM) < 100 or len(testResultB) < 100:
                    os.remove(self.MelodyPath[i - killed])
                    os.remove(self.BassPath[i - killed])
                    self.MelodyPath.pop(i - killed)
                    self.BassPath.pop(i - killed)
                    print(len(testResultM), len(testResultB))
                    print('kill ' + self.MelodyPath[i - killed])
                    print('kill ' + self.BassPath[i - killed])
                    killed += 1
            except:
                    os.remove(self.MelodyPath[i - killed])
                    os.remove(self.BassPath[i - killed])
                    self.MelodyPath.pop(i - killed)
                    self.BassPath.pop(i - killed)
                    print('kill ' + self.MelodyPath[i - killed])
                    print('kill ' + self.BassPath[i - killed])
                    killed += 1

    def MakeBatch(self, batchID):
        myBatchM = []
        myBatchB = []
        batchID = int(batchID * len(self.MelodyPath) / self.batchsize)
        #print(self.batchsize)
        for i in range(self.batchsize):
            tempID = (batchID + i) % len(self.MelodyPath)
            myBatchM.append(self.ReadMidi('M', tempID)[0:100])
            myBatchB.append(self.ReadMidi('B', tempID)[0:100])
            #print(i) #Bug here

        return myBatchM, myBatchB


#Dataset = midiData('/hdd2/lmd/0-melody', '/hdd2/lmd/0-bass', 5)
#Dataset.DataClean() #Don't Try this!
#sampleM, sampleB = Dataset.MakeBatch(0)
#print(sampleM)
