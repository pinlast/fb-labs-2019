import sys


def get_file_data():
    with open('TEXT', 'r') as f:
        return f.readlines()


def encrypt(in_file, out_file, lang, key, if_encrypt=False):
    rus = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    eng = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']    
    lang_list = eval(lang)

    encrypted_text = ""
    keyStep = 0
    with open(in_file, "r") as f:
        for line in f.readlines():
            for elem in line:
                if elem.lower() not in lang_list:
                    encrypted_text += elem
                else:  
                    elem_pos = lang_list.index(elem.lower())
                    moved_elem = lang_list.index(key[keyStep])
                    encrypt_pos = (elem_pos + moved_elem) % len(lang_list) if if_encrypt else (elem_pos - moved_elem) % len(lang_list)
                    
                    if elem.islower() == True:
                        encrypted_text += lang_list[encrypt_pos]
                    else:
                        encrypted_text += lang_list[encrypt_pos].upper()

                    keyStep += 1
                    keyStep %= len(key)
    
    with open(out_file, "w") as f:
        f.write(encrypted_text)


def main():
    lang = sys.argv[1]
    key = sys.argv[2]
    in_file = sys.argv[3]
    out_file = sys.argv[4]
    if_encrypt = (sys.argv[5] == "True")
    encrypt(in_file, out_file, lang, key, if_encrypt)


if __name__ == '__main__':
    main()
