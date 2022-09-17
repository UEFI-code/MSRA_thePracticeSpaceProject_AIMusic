import torch

class myCNN(torch.nn.Module):
    def __init__(self):
        super(myCNN, self).__init__() 
        self.relu = torch.nn.ReLU(True)
        self.softmax = torch.nn.Softmax()
        self.glu = torch.nn.GLU(dim=1)
        self.conv1 = torch.nn.Conv1d(6, 64, 3, 2, 1)
        self.conv2 = torch.nn.Conv1d(32, 32, 3, 2, 1)
        self.conv3 = torch.nn.Conv1d(16, 16, 2, 2, 1)
        self.li1 = torch.nn.Linear(208, 1024)
        self.li2 = torch.nn.Linear(1024, 1024)
        self.li3 = torch.nn.Linear(1024, 1024)
        self.li4 = torch.nn.Linear(1024, 600)

    def forward(self, x):
        x = x.view(x.size(0), 6, 100)
        x = self.conv1(x)
        x = self.glu(x)
        x = self.conv2(x)
        x = self.glu(x)
        x = self.conv3(x)
        x = self.relu(x)
        x = x.view(x.size(0), -1)
        x = self.li1(x)
        x = self.relu(x)
        x = self.li2(x)
        x = self.relu(x)
        x = self.li3(x)
        x = self.relu(x)
        x = self.li4(x)
        x = self.relu(x)
        x = x.view(x.size(0), 100, 6)
        return x
