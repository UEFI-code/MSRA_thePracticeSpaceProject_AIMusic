import torch

class myMidiEmbedding(torch.nn.Module):
    
    def __init__(self, EmbDim, OutDim):
        
        self.layer1 = torch.nn.Embedding(EmbDim, OutDim)

    def forward(self, x):

        return self.layer1(x)
