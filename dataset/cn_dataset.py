import torch
from torch.utils import data
import numpy as np
from external.radical.radical import Radical

class CnDataset(data.Dataset):
    def __init__(self,input_file_name,min_count=3,window_size = 2):
        self.index = 0 # 中心词索引
        self.window_size = window_size
        self.word_pair_list = []

        self.min_count = min_count # 数量少于min_count的词被删除
        self.input_file_name = input_file_name
        self.input_file = open(self.input_file_name,"r",encoding='utf-8')

        self.wordid_frequency_dict = dict()
        self.word_count = 0 # 字典词总数
        self.word_count_sum = 0 # 文本中所有词总数

        self.sentence_count = 0 # 句子个数
        self.id2word_dict = dict()
        self.word2id_dict = dict()
        self._init_word_dict()

        self.sample_table = []
        self._init_sampel_table() # 初始化负采样映射表
        self._get_wordid_list()
        self._init_word_data()

        # 生成字符字典
        self.char_count = 0
        self.id2char_dict = dict()
        self.char2id_dict = dict()
        self._init_char_dict()
        self.char_pair_list = []

        # 这里保存了所有字符的部首字典
        self.char2radical_dict = dict()

        # 生成部首字典
        self.radical_count = 0
        self.id2radical_dict = dict()
        self.radical2id_dict = dict()
        self._init_radical_dict()
        self.radical_pair_list = []

        self._init_char_radical_data()



        print('word count is ',self.word_count)
        print('word count sum is ',self.word_count_sum)
        print('sentence count is ',self.sentence_count)
        print('char count is ',self.char_count)
        print('radical_count count is ',self.radical_count)


    # 初始化词字典
    def _init_word_dict(self):
        word_freq = dict()
        for line in self.input_file:
            line  = line.strip().split()
            self.word_count_sum += len(line)
            self.sentence_count += 1
            for i,word in enumerate(line):
                if word_freq.get(word) == None:
                    word_freq[word] = 1
                else:
                    word_freq[word] += 1

        for i,word in enumerate(word_freq):
            if i % 1000 == 0:
                print(i , len(word_freq))
            if word_freq[word] < self.min_count:
                self.word_count_sum -= word_freq[word]
                continue
            self.word2id_dict[word] = len(self.word2id_dict)
            self.id2word_dict[len(self.id2word_dict)] = word
            self.wordid_frequency_dict[len(self.word2id_dict) - 1] = word_freq[word]
        self.word_count = len(self.word2id_dict)

    def _init_sampel_table(self):
        sample_table_size = 1e8
        pow_frequency = np.array(list(self.wordid_frequency_dict.values())) ** 0.75
        word_pow_sum = sum(pow_frequency)
        ratio_array = pow_frequency / word_pow_sum
        word_count_list = np.round(ratio_array * sample_table_size)
        for word_index,word_freq in enumerate(word_count_list):
            self.sample_table += [word_index] * int(word_freq)
        self.sample_table = np.array(self.sample_table)
        np.random.shuffle(self.sample_table)

    def _get_wordid_list(self):
        self.input_file = open(self.input_file_name,encoding='utf-8')
        sentences = self.input_file.readlines()
        wordid_list = [] # 一句话中所有word 对应的 id
        for i,sentence in enumerate(sentences):
            if i % 1000 == 0:
                print(i, len(sentences))

            sentence = sentence.strip().split(' ')

            for j,word in enumerate(sentence):
                # todo:这里可以对oov词进行pad处理
                try:
                    word_id = self.word2id_dict[word]
                    wordid_list.append(word_id)
                except:
                    continue
        self.wordid_list = wordid_list

    def _init_word_data(self):
        while self.index < len(self.wordid_list)-1:
            wordid_w = self.wordid_list[self.index]
            for i in range(max(self.index - self.window_size, 0 ),min(self.index + self.window_size + 1,len(self.wordid_list))):
                wordid_v = self.wordid_list[i]
                if self.index == i:
                    # 上下文词=中心词 跳过
                    continue

                self.word_pair_list.append([wordid_w,wordid_v])
            self.index += 1
        self.word_pair_list = np.asarray(self.word_pair_list)

    # 初始化字符字典
    def _init_char_dict(self):
        char_freq_dict = dict()
        for word in self.word2id_dict.keys():
            for char in word:
                if char_freq_dict.get(char) == None:
                    char_freq_dict[char] = 1
                else:
                    char_freq_dict[char] += 1

        self.char_count = len(char_freq_dict)
        for char in char_freq_dict.keys():
            self.char2id_dict[char] = len(self.char2id_dict)
            self.id2char_dict[len(self.id2char_dict)] = char

    def _init_char_radical_data(self):
        print('_init_char_radical_data...')
        for i,word_pair in enumerate(self.word_pair_list):
            if i % 10000 == 0:
                print(i, len(self.word_pair_list))

            w_wordid = word_pair[0]
            w_word = self.id2word_dict[w_wordid]
            w_word_char_list = []

            w_char_radical_list = []
            for char in w_word:
                char_id = self.char2id_dict[char]
                w_word_char_list.append(char_id)

                rad = self.char2radical_dict.get(char)
                radical_id = self.radical2id_dict[rad]
                w_char_radical_list.append(radical_id)

            v_wordid = word_pair[1]
            v_word = self.id2word_dict[v_wordid]
            v_word_char_list = []

            v_char_radical_list = []
            for char in v_word:
                char_id = self.char2id_dict[char]
                v_word_char_list.append(char_id)

                rad = self.char2radical_dict.get(char)
                radical_id = self.radical2id_dict[rad]
                v_char_radical_list.append(radical_id)

            self.char_pair_list.append([w_word_char_list,v_word_char_list])
            self.radical_pair_list.append([w_char_radical_list,v_char_radical_list])
        # self.char_pair_list = np.asarray(self.char_pair_list)
        # self.radical_pair_list = np.asarray(self.radical_pair_list)

    def _init_radical_dict(self):
        radical = Radical()
        for char in self.char2id_dict.keys():
            rad = radical.get_radical(char)
            if rad == None:
                rad = char
            if self.char2radical_dict.get(char) == None:
                self.char2radical_dict[char] = rad


        for key,value in self.char2radical_dict.items():
            self.radical2id_dict[value] = len(self.radical2id_dict)
            self.id2radical_dict[len(self.id2radical_dict)] = value
        self.radical_count = len(self.radical2id_dict)

    def __getitem__(self, index):
        word_pair = self.word_pair_list[index]
        char_pair = self.char_pair_list[index]
        radical_pair = self.radical_pair_list[index]
        # label = torch.tensor(self.label[index])
        return word_pair,char_pair,radical_pair


    def __len__(self):
        return len(self.word_pair_list)