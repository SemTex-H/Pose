import torch.nn as nn
from torchsummary import summary
import torch

class LSTM(nn.Module):
    def __init__(self):
        pass


class CNN(nn.Module):
    def __init__(self):
        super().__init__()

        self.conv1 = nn.Sequential(
            nn.Conv1d(
                in_channels= 1,
                out_channels= 128,
                kernel_size= 3,
                stride= 1,
                padding= 1,
            ),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2),
        )
        
        self.conv2 = nn.Sequential(
            nn.Conv1d(
                in_channels= 128,
                out_channels= 512,
                kernel_size= 3,
                stride= 1,
                padding= 1,
            ),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2),
        )
        self.conv3 = nn.Sequential(
            nn.Conv1d(
                in_channels= 512,
                out_channels= 1024,
                kernel_size= 3,
                stride= 1,
                padding= 1,
            ),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2),
        )
        self.conv4 = nn.Sequential(
            nn.Conv1d(
                in_channels= 1024,
                out_channels= 2048,
                kernel_size= 3,
                stride= 1,
                padding= 1,
            ),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2),
        )
        self.dropout = nn.Dropout(0.4)
        
        self.flatten = nn.Flatten()

        self.linear = nn.Linear(4096, 64)
        self.softmax = nn.Softmax(dim=1)


    def forward(self, input_data):
        x = input_data.unsqueeze(1)
        
        x = self.conv1(input_data)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        
        x = self.flatten(x)
        logits = self.linear(x)
        predictions =  self.softmax(logits)
        return predictions
    
if __name__ == "__main__":
    model = CNN()

    input_data = torch.tensor([365., 181., 369., 127., 371.,  71., 308., 181., 303., 130., 
                            303.,  75., 354., 288., 359., 358., 363., 432., 316., 290., 
                            314., 355., 310., 429., 177.,  94., 185., 264., 180., 268., 
                            181.,  94.]).unsqueeze(0)  # Adding batch dimension

    output = model(input_data)

    print(output[1])