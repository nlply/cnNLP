import torch
from torch.utils import data
import numpy as np

class TestDataset(data.Dataset):
    def __init__(self):
        self.data = np.asarray([[1,2],[3,4],[5,6],[7,8],[9,0]]) # this is data
        self.label = np.asarray([0,1,0,1,2]) # this is label

    def __getitem__(self, index):
        txt = torch.LongTensor(self.data[index])
        label = torch.tensor(self.label[index])
        return txt,label

    def __len__(self):
        return len(self.data)


if __name__ == '__main__':
    test = TestDataset()
    print(test[2])
    print(test.__len__())

    test_loader = data.DataLoader(test,batch_size=2,shuffle=True,num_workers=2)
    for i,traindata in enumerate(test_loader):
        print('i:',i)
        data,label = traindata
        print('data:',data)
        print('label:',label)


