import torch

class MidiCNN(torch.nn.Module):
    
    def __init__(self, inputDim):
        
        self.relu = nn.ReLU(True)
        self.glu = nn.GLU()
        self.layer1 = nn.Conv1D(inputDim, 1024, 5, 2, 1)
        self.BN1024 = nn.BatchNorm(1024)
        self.layer2 = nn.Conv1D(512, 1024, 5, 2, 1)
        self.layer3 = nn.Conv1D(512, 1024, 5, 2, 1)
        self.li1 = nn.Linear(12000, 4096)
        self.li2 = nn.Linear(4096, 4096)
        self.li3 = nn.Linear(4096, 4096)

    def forward(self, x):

        x = self.layer1(x)
        x = self.BN1024(x)
        x = self.glu(x)
        x = self.layer2(x)
        x = self.BN1024(x)
        x = self.glu(x)
        x = self.layer3(x)
        x = self.BN1024(x)
        x = self.glu(x)
        x = self.li1(x)
        x = self.relu(x)
        x = self.li2(x)



