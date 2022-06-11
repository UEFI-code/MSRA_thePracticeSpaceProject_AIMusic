import torch

class MidiWindUper(torch.nn.Module):

    def __init__(self)
        self.layer = nn.Linear(4096, 4096)
        self.softmax = nn.Softmax()

    def forward(self,x)
        x = self.layer(x)
        x = self.softmax(x)
