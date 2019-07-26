import tensorflow as tf
import re
import numpy as np
#import tensorflow as tf
import os


def clean_text(text):
    #text = text.lower()
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"that's", "that is", text)
    text = re.sub(r"what's", "what is", text)
    text = re.sub(r"where's", "where is", text)
    text = re.sub(r"how's", "how is", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"n't", " not", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "cannot", text)
    # text = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", text)
    return text


def gru(units):
    # If you have a GPU, we recommend using CuDNNGRU(provides a 3x speedup than GRU)
    # the code automatically does that.
    if tf.test.is_gpu_available():
        return tf.keras.layers.CuDNNGRU(units,
                                        return_sequences=True,
                                        return_state=True,
                                        recurrent_initializer='glorot_uniform')
    else:
        return tf.keras.layers.GRU(units,
                                   return_sequences=True,
                                   return_state=True,
                                   recurrent_activation='sigmoid',
                                   recurrent_initializer='glorot_uniform')


def lstm(units):
    # If you have a GPU, we recommend using CuDNNGRU(provides a 3x speedup than GRU)
    # the code automatically does that.
    if tf.test.is_gpu_available():
        print('Yes')
        return tf.keras.layers.CuDNNLSTM(units,
                                         return_sequences=True,
                                         return_state=True,
                                         bias_initializer="zeros",
                                         recurrent_initializer='glorot_uniform')
    else:
        print('No')
        return tf.keras.layers.LSTM(units,
                                    return_sequences=True,
                                    return_state=True,              
                                    recurrent_activation='sigmoid',
                                    recurrent_initializer='glorot_uniform')
        
def lstmb(units):
  # If you have a GPU, we recommend using CuDNNGRU(provides a 3x speedup than GRU)
  # the code automatically does that.
  if tf.test.is_gpu_available():
    return tf.keras.layers.CuDNNLSTM(units, 
                                    return_sequences=True, 
                                    return_state=True, 
                                    go_backwards=True,
                                    recurrent_initializer='glorot_uniform')
  else:
    return tf.keras.layers.LSTM(units, 
                               return_sequences=True, 
                               return_state=True,
                               go_backwards=True,
                               recurrent_activation='sigmoid', 
                               recurrent_initializer='glorot_uniform')
        
        
def blstm(units):
  # If you have a GPU, we recommend using CuDNNGRU(provides a 3x speedup than GRU)
  # the code automatically does that.
  if tf.test.is_gpu_available():
    return tf.keras.layers.Bidirectional(tf.keras.layers.CuDNNLSTM(units, 
                                    return_sequences=True, 
                                    return_state=True, 
                                    recurrent_initializer='glorot_uniform'), merge_mode='concat')
  else:
    return tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(units, 
                               return_sequences=True, 
                               return_state=True, 
                               recurrent_activation='sigmoid', 
                               recurrent_initializer='glorot_uniform'), merge_mode='concat')

        ##########word vectors######

        

def pretrained_embeddings(file_path, EMBEDDING_DIM, VOCAB_SIZE, word2idx):
    
    # 1.load in pre-trained word vectors     #feature vector for each word
    print('Loading word vectors...')
    word2vec = {}
    with open(os.path.join(file_path+'.%sd.txt' % EMBEDDING_DIM), errors='ignore', encoding='utf8') as f:
        # is just a space-separated text file in the format:
        # word vec[0] vec[1] vec[2] ...
        for line in f:
            #print(line)
            values = line.split()
            word = values[0]
            vec = np.asarray(values[1:], dtype='float32')
            word2vec[word] = vec

    print('Found %s word vectors.' % len(word2vec))

    # 2.prepare embedding matrix
    print('Filling pre-trained embeddings...')
    num_words = VOCAB_SIZE
    # initialization by zeros
    embedding_matrix = np.zeros((num_words, EMBEDDING_DIM))
    for word, i in word2idx.items():
        if i < VOCAB_SIZE:
            embedding_vector = word2vec.get(word)
            if embedding_vector is not None:
                # words not found in embedding index will be all zeros.
                embedding_matrix[i] = embedding_vector
                
    return embedding_matrix
