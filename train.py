import torch
import torch.nn.functional as F
import numpy
import MidiDataset
from config import Config as config
import BPN
import WindUper

Dataset = MidiDataset.midiData(config.midiXPath, config.midiTPath, config.batchsize)

dataLen = len(Dataset.MelodyPath)

batchNum = int(dataLen / config.batchsize)

def myLoss(y, t):
    loss = F.cosine_similarity(y, t, 0).sum()
    return loss

myBPN = BPN.myBPN().cuda()

optimizer = torch.optim.SGD(myBPN.parameters(), lr=config.learningRate)

for i in range(config.epoch):
    for j in range(batchNum):
        dataM, dataB = Dataset.MakeBatch(j)
        dataM = numpy.array(dataM, dtype=object).astype(float)
        dataB = numpy.array(dataB, dtype=object).astype(float)
        dataM = torch.tensor(dataM).float().cuda() / 128
        dataB = torch.tensor(dataB).float().cuda() / 128
        optimizer.zero_grad()
        y = myBPN(dataM.view(config.batchsize, -1))
        y = y.view(config.batchsize, 100, 6)
        loss = myLoss(y, dataB)
        loss.backward()
        optimizer.step()
        print('epoch %d batchID %d/%d loss %f' % (i, j, batchNum, loss))
    torch.save(myBPN.state_dict(), config.pthsave)
    dumpY = y.cpu().detach() * 128
    dumpM = dataM.cpu() * 128
    WindUper.ArrayToMidi(dumpY[0], config.midisave + '/testY.midi')
    WindUper.ArrayToMidi(dumpM[0], config.midisave + '/testM.midi')
