import torch.nn as nn
import pandas as pd
from torch.utils.data import DataLoader
from posedataset import Posedataset
import torch
from model import *
PATH = "dataset.csv"
EPOCHS = 100

def train_one_epoch(model, dataloader, loss_fn, optimiser, device):
    for x, y in dataloader:
        x = x.unsqueeze(1)
        x, y = x.to(device), y.to(device)
        optimiser.zero_grad()

        predictions = model(x)
        loss = loss_fn(predictions, y)

        loss.backward()
        optimiser.step()
    
    print(f'Loss: {loss.item()}')



def train(model, dataloader, loss_fn, optimiser, device, epochs):
    for i in range(epochs):
        print(f'EPOCH: {i+1}')
        train_one_epoch(model, dataloader, loss_fn, optimiser, device)
        print('-'*10)
    print('DONE')

if __name__ == '__main__':
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f'Using {device}')

    posedataset = Posedataset(PATH)
    train_dataloader = DataLoader(posedataset, 16, shuffle=True)


    cnn = CNN().to(device)
    loss_fn = nn.CrossEntropyLoss()
    optimiser = torch.optim.Adam(cnn.parameters(),
                                 lr=0.01)
    train(cnn, train_dataloader, loss_fn, optimiser, device, EPOCHS)

    torch.save(cnn.state_dict(), "cnn.pth")