import sys
import re
import math

from itertools import groupby 
from operator import itemgetter
from collections import defaultdict


def get_file_lines():
    with open('TEXT') as f:
        return f.readlines()

    
def remove_not_alpha(data):
    res = list()
    for line in data:
        line = re.sub('[^а-яА-Я]+', '', line.lower())
        res.append(line)
    
    return res


def get_ngram_dict(lines, n=2):
    ngram_dict = defaultdict(int)
    for line in lines:
        for i in range(0, len(line), n):
            ngram = line[i:i+n]
            if len(ngram) == n:
                ngram_dict[ngram] += 1

    print(ngram_dict)

    res_dict = dict()
    ngram_dict_len = len(ngram_dict)
    for item, value in ngram_dict.items():
        res_dict[item] = value / ngram_dict_len

    return res_dict


def get_entropy(ngram_dict, num):
    result=0
    
    grouped_dict = defaultdict(list)
    for key, value in sorted(ngram_dict.items()):
        grouped_dict[value].append(key)
    
    print(grouped_dict)

    for item, value in grouped_dict.items():
        result+=(item*math.log(item,2))*len(value)

    return result * (-1/num)


def get_redundancy(entropy):
    return 1-(entropy/(math.log(33,2)))


def main():
    num = 2

    lines = get_file_lines()
    filtered_lines = remove_not_alpha(lines)
    ngram_dict = get_ngram_dict(filtered_lines, num)

    entropy = get_entropy(ngram_dict, num)
    redundancy = get_redundancy(entropy)
    
    print(len(ngram_dict))
    
    for item, value in ngram_dict.items():
        print(item, ' -> ', value)

    print("entropy: ", entropy)
    print("redundancy: ", redundancy)


if __name__ == '__main__':
    main()
