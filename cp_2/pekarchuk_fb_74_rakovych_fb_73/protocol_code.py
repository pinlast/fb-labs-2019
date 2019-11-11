import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from cipher import encrypt
from get_key import get_IC

eng = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
rus = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']


def main():
    in_file = 'test.txt'
    lang = 'rus'
    keys = ['фб', 'фбе', 'ключ', 'шесть', 'десятьбключ', 'улановсеребряныепули']
    out_files = [in_file]
    for key in keys:
        out_file = f'out_file_{len(key)}.txt'
        out_files.append(out_file)
        encrypt(in_file, out_file, lang, key)

    res_values = list()
    for out_file in out_files:
        with open(out_file, 'r') as f:
            text = "".join([x.lower().strip() for x in "".join(f.readlines()).split() if x.isalpha()])
            res_values.append((get_IC(text), out_file[:-4].split('_')[-1]))
            print("IC: ", res_values[-1][0], ' -> key_len:', res_values[-1][1])
        

    plt.bar([x[1] for x in res_values], [x[0] for x in res_values], align='center', alpha=1)
    plt.ylabel('IC')
    plt.title('Different IC for different keys')

    plt.show()


if __name__ == '__main__':
    main()
