import torch

import random
import os
import numpy as np

from model.SkipGram import SkipGram
from dataset.cn_dataset import CnDataset
from torch.utils import data


# 设置种子
def seed_everthing(seed = 1024):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True

def main():
    arch = 'cw2vec'
    seed = 1024
    seed_everthing(seed = seed)

    print('加载数据集')
    train_dataset = CnDataset(input_file_name='data/zhihu.txt')
    print('初始化模型')
    model = SkipGram(embedding_dim=100,word_num=5,character_num=3,radical_num=3)

    print('读取数据')
    data_loader = data.DataLoader(train_dataset,batch_size=1,shuffle=True,num_workers=0)

    for i,traindata in enumerate(data_loader):
        # 还需要输出负采样的样本
        print('i:', i)
        word_pair,char_pair,radical_pair = traindata
        print('word_pair:', word_pair)
        print('char_pair:', char_pair)
        print('radical_pair:', radical_pair)
        model(word_pair,char_pair,radical_pair)


if __name__ == '__main__':
    main()