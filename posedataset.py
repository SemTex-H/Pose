import pandas as pd
import os
import torch
from torch.utils.data import Dataset
class Posedataset(Dataset):
    def __init__(self, path):
        self.data = pd.read_csv(path)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        poses = torch.tensor(self.data.iloc[index, 1:-1].values.flatten().tolist())
        poses = poses.float()
        return poses, self.data.iloc[index, 0]
    
if __name__ == "__main__":
    PATH = 'dataset.csv'
    dataset = Posedataset(PATH)

    print(dataset[2000][1])