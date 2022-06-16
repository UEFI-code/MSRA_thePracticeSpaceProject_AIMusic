import torch

class myBPN(torch.nn.Module):
    def __init__(self):
        super(myBPN, self).__init__() 
        self.relu = torch.nn.ReLU(True)
        self.softmax = torch.nn.Softmax()
        self.li1 = torch.nn.Linear(600, 1024)
        self.li2 = torch.nn.Linear(1024, 1024)
        self.li3 = torch.nn.Linear(1024, 1024)
        self.li4 = torch.nn.Linear(1024, 600)

    def forward(self, x):
        x = self.li1(x)
        x = self.relu(x)
        x = self.li2(x)
        x = self.relu(x)
        x = self.li3(x)
        x = self.relu(x)
        x = self.li4(x)
        x = self.relu(x)
        return x
