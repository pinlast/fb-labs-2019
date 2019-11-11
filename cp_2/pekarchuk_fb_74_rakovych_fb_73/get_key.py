import collections
import sys
from collections import Counter, defaultdict
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

eng_freq_dict = {
    'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253, 'e': 0.12702,
    'f': 0.02228, 'g': 0.02015, 'h': 0.06094, 'i': 0.06966, 'j': 0.00153,
    'k': 0.00772, 'l': 0.04025, 'm': 0.02506, 'n': 0.06749, 'o': 0.07507,
    'p': 0.01929, 'q': 0.00095, 'r': 0.05987, 's': 0.06327, 't': 0.09056,
    'u': 0.02758, 'v': 0.00978, 'w': 0.02360, 'x': 0.00150, 'y': 0.01974,
    'z': 0.00074
}

rus_freq_dict = {
    'о': 0.10983, 'е': 0.08483, 'а': 0.07998, 'и': 0.07367, 'н': 0.0670,
    'т': 0.06318, 'с': 0.05473, 'р': 0.04746, 'в': 0.04533, 'л': 0.04343,
    'к': 0.03486, 'м': 0.03203, 'д': 0.02977, 'п': 0.02804, 'у': 0.02615,
    'я': 0.02001, 'ы': 0.01898, 'ь': 0.01735, 'г': 0.01687, 'з': 0.01641,
    'б': 0.01592, 'ч': 0.01450, 'й': 0.01208, 'х': 0.00966, 'ж': 0.00940,
    'ш': 0.00718, 'ю': 0.00639, 'ц': 0.00486, 'щ': 0.00361, 'э': 0.00331,
    'ф': 0.00267, 'ъ': 0.00037,
}

eng = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
rus = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']


def get_IC(text_part):
    global rus
    lang_list = rus

    text = "".join([x for x in text_part.split() if x.isalpha()])
    if len(text) > 1:
        N = len(text)
    else:
        return
    freqs = collections.Counter(text)
    freqsum = 0.0
    for letter in lang_list:
        freqsum += freqs[letter] * (freqs[letter] - 1)

    IC = freqsum / (N * (N - 1))
    return IC


def get_subseq(i, text):
    sub_seq = defaultdict(list)
    for j in range(0, len(text), i):
        for c in range(i):
            try:
                sub_seq[c].append(text[j + c])
            except IndexError:
                continue

    return sub_seq


def get_key_length(text):
    avrg_ics = dict()
    for i in range(1, 30):
        ic = 0.0
        seqs = get_subseq(i, text)
        for seq in seqs.values():
            seq_str = "".join(seq)
            val = get_IC(seq_str) if get_IC(seq_str) else 0.0
            ic += val
        avrg_ics[i] = ic / i
    
    sorted_ic = [(k, avrg_ics[k]) for k in sorted(avrg_ics, key=avrg_ics.get, reverse=True)]
    print("\nIC: ", sorted_ic[:6], '\n')
    
    plt.bar([x[0] for x in sorted_ic], [x[1] for x in sorted_ic], align='center', alpha=1)
    plt.ylabel('IC')
    plt.title('IC for different key length while decrypting')
    plt.show()

    return sorted_ic[0]


def get_key(key_len, text):
    global rus
    global rus_freq_dict
    lang_freq = rus_freq_dict

    subseqs = get_subseq(key_len, text)
    subseqs_counter = list()
    for seq in subseqs.values():
        counter = Counter(seq)
        subseqs_counter.append({key: counter[key] for key in lang_freq.keys()})

    key = find_key(subseqs_counter)
    return key


def find_key(freq_dicts):
    global rus
    global rus_freq_dict
    lang_list = rus
    lang_freq_dict = rus_freq_dict

    lang_list_len = len(lang_list)
    res = ""
    for freq_dict in freq_dicts:
        temp_max = 0
        for i in range(lang_list_len):
            temp_sum = 0
            for char in lang_freq_dict:
                try:
                    t_plus_g = lang_list[(lang_list.index(char) + i) % lang_list_len]
                    temp_sum += lang_freq_dict[char] * freq_dict[t_plus_g]

                except Exception as e:
                    print(e)
                    break

            if temp_sum > temp_max:
                temp_max = temp_sum
                letter = lang_list[i]

        res += letter
    return res


def main(in_file):
    with open(in_file, "r") as f:
        text = "".join([x.lower().strip() for x in f.read().split() if x.isalpha()])
        key_len = get_key_length(text)[0]
        key = get_key(key_len, text)
        print("Ключ: ", key)


if __name__ == "__main__":
    in_file = sys.argv[1]

    main(in_file)
