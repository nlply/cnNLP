
import  torch
import  torch.nn as nn
import  torch.nn.functional as F

class SkipGram(nn.Module):
    def __init__(self,embedding_dim,word_num,character_num,radical_num):
        super(SkipGram, self).__init__()

        # word
        self.word_amplitude_w_embedding = nn.Embedding(word_num,embedding_dim)
        self.word_phase_w_embedding = nn.Embedding(word_num,embedding_dim)

        self.word_amplitude_v_embedding = nn.Embedding(word_num, embedding_dim)
        self.word_phase_v_embedding = nn.Embedding(word_num, embedding_dim)


        # character
        self.character_amplitude_w_embedding = nn.Embedding(character_num, embedding_dim)
        self.character_phase_w_embedding = nn.Embedding(character_num, embedding_dim)

        self.character_amplitude_v_embedding = nn.Embedding(character_num, embedding_dim)
        self.character_phase_v_embedding = nn.Embedding(character_num, embedding_dim)

        # radical
        self.radical_amplitude_w_embedding = nn.Embedding(radical_num, embedding_dim)
        self.radical_phase_w_embedding = nn.Embedding(radical_num, embedding_dim)

        self.radical_amplitude_v_embedding = nn.Embedding(radical_num, embedding_dim)
        self.radical_phase_v_embedding = nn.Embedding(radical_num, embedding_dim)

    def farward(self,pos_u,pos_v,neg_u,neg_v):
        
        pass