# _*_ coding: utf-8 _*_

import nltk
import random

file = open('Text/Walden.txt', 'r')
walden = file.read()
walden = walden.split()


def makePairs(arr):
    pairs = []
    for i in range(len(arr)):
        if i < len(arr) - 1:
            temp = (arr[i], arr[i + 1])
            pairs.append(temp)
    return pairs


def generate(cfd, word='the', num=500):
    for i in range(num):
        # make an array with the words shown by proper count
        arr = []
        for j in cfd[word]:
            for k in range(cfd[word][j]):
                arr.append(j)
        print(word, end=' ')

        # choose the word randomly from the conditional distribution
        word = arr[int((len(arr)) * random.random())]

pairs = makePairs(walden)
cfd = nltk.ConditionalFreqDist(pairs)
generate(cfd)
