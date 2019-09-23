import sys
import math
import re
from collections import defaultdict


def get_file_lines(fname):
    with open(fname) as f:
        return f.readlines()


def remove_not_alpha(data, need_space):
    return_list = list()
    for line in data:
        re_check = '[^а-яА-Я{}]+'.format(' ' if need_space else '')
        line = re.sub(re_check, '', line.lower())
        return_list.append(line)

    return return_list


def get_ngram_dict(lines, ngram_num=2):
    ngram_counter = 0
    ngram_dict = defaultdict(int)
    for line in lines:
        for i in range(0, len(line), ngram_num):
            ngram = line[i:i+ngram_num]
            if len(ngram) != ngram_num:
                continue

            ngram_dict[ngram] += 1
            ngram_counter += 1

    return_dict = dict()
    for elem, amount in ngram_dict.items():
        return_dict[elem] = amount / ngram_counter

    return return_dict


def get_entropy(ngram_dict, num):
    result = 0

    grouped_dict = dict()
    for item, value in ngram_dict.items():
        try:
            grouped_dict[value].append(item)
        except KeyError:
            grouped_dict[value] = [item]

    for item, value in grouped_dict.items():
        result += (item * math.log(item, 2)) * len(value)

    return result * (-1/num)


def get_redundancy(entropy):
    return 1-(entropy/(math.log(33, 2)))


def main():
    num = int(sys.argv[1]) if len(sys.argv) >= 2 else 2
    need_space = eval(sys.argv[2]) if len(sys.argv) >= 3 else False
    fname = sys.argv[3] if len(sys.argv) >= 4 else 'TEXT'

    lines = get_file_lines(fname)
    filtered_lines = remove_not_alpha(lines, need_space)
    ngram_dict = get_ngram_dict(filtered_lines, num)

    entropy_val = get_entropy(ngram_dict, num)
    redundancy_val = get_redundancy(entropy_val)

    for item, value in ngram_dict.items():
        print(item, ' -> ', value)

    print("entropy: ", entropy_val)
    print("redundancy: ", redundancy_val)


if __name__ == '__main__':
    main()
