import binascii
from random import randrange, getrandbits


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def inv(a, m): 
    input_m = m
    y = 0
    x = 1

    while (a > 1) : 
        q = a // m
        t = m

        m = a % m
        a = t
        t = y

        y = x - q * y
        x = t

    if (x < 0):
        x = x + input_m

    return x 


class RSAClass:
    def __init__(self, ):
        self.e = 0
        self.n = 0
        self.p = self.generate_prime_number(length=256)
        self.q = self.generate_prime_number(length=256)
        self.keypair = self.generate_keypair(self.p, self.q)
    
    def generate_keypair(self, p, q):
        if not self.miller_rabin(p) or not self.miller_rabin(q):
            return 'Numbers not prime'

        n = p * q
        phi = (p-1) * (q-1)
        e = randrange(1, phi)  # same as phi - 1
        
        # saving data to model for future
        self.e = e
        self.n = n

        # verify e and phi mutually prime
        g = gcd(e, phi)
        while g != 1:
            print('e and phi was\'t mutually prime')
            e = randrange(1, phi)
            g = gcd(e, phi)

        # generating secret key with eucl. alg.
        d = inv(e, phi)

        return ((e, n), (d, n))

    def generate_prime_number(self, length=1024):
        p = 4
        while not self.miller_rabin(p, 128):
            p = (getrandbits(length) | 1)  # | 1 so it's not even

        return p

    def miller_rabin(self, in_number, test_number=128):
        if in_number == 2:  # 2 is prime
            return True
        if in_number <= 1 or in_number % 2 == 0:
            return False

        s = 0
        d = in_number - 1
        while d & 1 == 0:  # d must be odd
            d //= 2
            s += 1

        for i in range(test_number):  # making n tests
            x = pow(randrange(2, in_number - 1), d, in_number)
  
            if x != in_number - 1 and x != 1:
                for j in range(s):
                    if pow(x, 2, in_number) == 1:
                        return False

                if x != in_number - 1:
                    return False   

        return True

    def encrypt(self, pk, plaintext):
        
        # hashing text
        hex_data = binascii.hexlify(plaintext.encode())
        plaintext = int(hex_data, 16)
        key, n = pk

        # ecnrypting with plaintext ** key % n
        cipher = pow(plaintext, key, n)
        return cipher

    def decrypt(self, pk, ciphertext):
        key, n = pk
        decrypted_text = pow(ciphertext, key, n)

        return binascii.unhexlify(hex(decrypted_text)[2:]).decode()

    def generate_sign(self, plaintext):
        hex_data = binascii.hexlify(plaintext.encode())
        m = int(hex_data, 16)
        return (m, self.keypair[0][0])


def main():
    message = input('Message: ')
    rsa = RSAClass()
    encrypted = rsa.encrypt(rsa.keypair[0], message)
    decrypted = rsa.decrypt(rsa.keypair[1], encrypted)
    sign = rsa.generate_sign(message)
    
    print('Open key: ', rsa.keypair[0][0], '\n\n')
    print('Secret key: ', rsa.keypair[1][0], '\n\n')
    print('Encrypted text: ', encrypted, '\n\n')
    print('Decrypted text: ', decrypted, '\n\n')
    print('Signature: ', sign, '\n\n')


if __name__ == '__main__':
    main()
