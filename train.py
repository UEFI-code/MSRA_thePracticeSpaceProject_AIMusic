import torch
import numpy
import MidiDataset
from config import Config as config
import BPN

Dataset = MidiDataset.midiData(config.midiXPath, config.midiTPath, config.batchsize)

dataLen = len(Dataset.MelodyPath)

batchNum = int(dataLen / config.batchsize)

myLoss = torch.nn.L1Loss()

myBPN = BPN.myBPN().cuda()

for i in range(config.epoch):
    for j in range(batchNum):
        dataM, dataB = Dataset.MakeBatch(j)
        dataM = numpy.array(dataM, dtype=object).astype(float)
        dataB = numpy.array(dataB, dtype=object).astype(float)
        dataM = torch.tensor(dataM).float().cuda() / 128
        dataB = torch.tensor(dataB).float().cuda() / 128
        y = myBPN(dataM.view(config.batchsize, -1))
        y = y.view(config.batchsize, 8, 6)
        loss = myLoss(y, dataB)
        print('epoch %d batchID %d/%d loss %f' % (i, j, batchNum, loss))
