import sys
import re
import math

from operator import itemgetter
from itertools import groupby 

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
    res_dict = dict()
    for line in lines:
        for i in range(0, len(line), n):
            ngram = line[i:i+n]
            ngram_dict[ngram] += 1


    ngram_dict_len = len(ngram_dict)
    for item, value in ngram_dict.items():
        res_dict[item] = value / ngram_dict_len

    return res_dict


def get_entropy(ngram_dict, num):
    res=0
    for elem in ngram_dict:
        res+=(elem*math.log(elem,2))*len(ngram_dict[elem])
    res*=(-1/num)

    return res


def get_redundancy(entropy):
    return 1-(entropy/(math.log(33,2)))


def main():
    num = 2

    lines = get_file_lines()
    filtered_lines = remove_not_alpha(lines)
    ngram_dict = get_ngram_dict(filtered_lines, num)

    snd = itemgetter(1)

    inv_map = dict()
    grouped = groupby(sorted(ngram_dict.items(), key=snd), snd)
    for number, var in grouped:
        inv_map.update({number: [item for item, _ in var]})


    entropy = get_entropy(inv_map, num)
    redundancy = get_redundancy(entropy)
    
    print(len(ngram_dict))
    
    for item, value in ngram_dict.items():
        print(item, ' -> ', value)

    print(entropy)
    print(redundancy)


if __name__ == '__main__':
    main()
