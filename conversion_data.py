# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 09:18:24 2019

@author: Hanan Bahy1
"""


def convert_Q_A_Dataset(file_path, new_file_path):

    with open(new_file_path, '+w') as new_file:
        i = 0
        repeat = 0
        prev_Q = None  # to track repeated questions
        prev_A = None
        temp_Q = None  # to track unique questions
        temp_A = None
        A_to_write = None  # to compare between answers of the similar questions

        for line in open(file_path, 'r'):
            if i == 0:  # skip first line in file
                i = 1
                continue
            else:
                items = line.rstrip().split('\t')
                if items[1] == 'NULL' or items[2] == 'NULL' or items[2] == '':  # ignore this line
                    continue

                Question = items[1]
                Answer = items[2]
                # print(Question,temp_Q)
                if Question == prev_Q:
                    repeat += 1
                    temp_Q = None  # means previous question not unique
                    temp_A = None
                    if (len(prev_A) < len(Answer)-1) and ('blah' not in Answer):
                        A_to_write = Answer
                    else:
                        A_to_write = prev_A

                else:

                    if repeat != 0:  # prev_Q is the last one in repeated questions
                        new_file.write("%s\t%s\n" % (prev_Q, A_to_write))
                        repeat = 0
                        #temp_Q = Question
                        #temp_A = Answer
                    else:
                        if temp_Q != None:
                            new_file.write("%s\t%s\n" % (temp_Q, temp_A))

                    temp_Q = Question
                    temp_A = Answer

                prev_Q = Question
                prev_A = Answer

        # for the end question or repeated question in the end of file
        new_file.write("%s\t%s\n" % (prev_Q, prev_A))


# E:\Graduation project 2018-2019\3-Chatbot\datasets\Question_Answer_Dataset_v1.2\S08
#convert_Q_A_Dataset('Question_Answer_Dataset_v1.2\S08\question_answer_pairs.txt' ,'Q_A_pairs8.txt')
#convert_Q_A_Dataset('test2.txt' ,'test2_after2.txt')

def convert_movies_lines(movies_path, conversation_path, Q_A_path):
    lines = open(movies_path, encoding='utf-8',
                 errors='ignore').read().split('\n')
    conversations = open(conversation_path, encoding='utf-8',
                         errors='ignore').read().split('\n')

    id2line = {}
    for line in lines:
        # convert line to list , note the question o answer is last item in list
        items = line.split(' +++$+++ ')
        id2line[items[0]] = items[-1]

    conv_ids = []
    for conv in conversations:
        # convert to separated-comma of ids string
        _conv = conv.split(
            ' +++$+++ ')[-1][1:-1].replace("'", "").replace(" ", "")
        conv_ids.append(_conv.split(','))  # list of ids ,each id is string

    with open(Q_A_path, 'a') as f:
        for conv in conv_ids:
            for i in range(0, len(conv)-1, 2):
                # print(i)
                Question = id2line[conv[i]]
                Answer = id2line[conv[i+1]]
                f.write("%s\t%s\n" % (Question, Answer))


convert_movies_lines('movie_lines\movie_lines.txt',
                     'movie_lines\movie_conversations.txt', 'movie_Q_A.txt')


def convert_twitter_data(file_path, new_path):

    with open(new_path, 'a') as f:
        prev_line = None
        # data source: https://github.com/Phylliida/Dialogue-Datasets
        for line in open(file_path):
            line = line.rstrip()

            if prev_line and line:
                f.write("%s\t%s\n" % (prev_line, line))

            # note:
            # between conversations there are empty lines
            # which evaluate to false

            prev_line = line
#convert_twitter_data('Twitter_Data/TwitterLowerAsciiCorpus.txt' ,'Twitter_Data/twitter_tab_format.txt')
