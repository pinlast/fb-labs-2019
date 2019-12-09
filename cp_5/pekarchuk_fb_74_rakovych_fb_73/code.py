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
            print('e and phi wasn\'t mutually prime')
            e = randrange(1, phi)
            g = gcd(e, phi)

        # generating secret key with eucl. alg.
        d = inv(e, phi)

        return ((e, n), (d, n))

    def generate_prime_number(self, length=1024):
        p = 4
        while not self.miller_rabin(p, 128):
            p = (getrandbits(length) | 1) + (1 << length)  # | 1 so it's not even

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
                        print('Not approved: ', pow(x, 2, in_number))
                        return False

                if x != in_number - 1:
                    return False   

        return True

    def encrypt(self, pk, plaintext):
        key, n = pk

        cipher = pow(plaintext, key, n)
        return cipher

    def decrypt(self, pk, ciphertext):
        key, n = pk
        decrypted = pow(ciphertext, key, n)

        return decrypted

    def sign(self, message, n, d):
        return (message, pow(message, n, d))

    def verify(self, message, S, e, n):
        return message == pow(S, e, n)

    def send_key(self, message, e, n, d, n_2):
        sign = self.sign(message, d, n_2)

        return (self.encrypt((e, n), sign[0]), self.encrypt((e, n), sign[1]))

    def recieve_key(self, message, e, n, d, n_2):
        s = pow(message, d, n)
        verify = self.verify(message, s, e, n)
        return (verify, self.decrypt((d, n_2), message))


def main():
    rsa_a = RSAClass()
    rsa_b = RSAClass()
    print(rsa_a.p, '\n\n', rsa_a.q, '\n\n')
    print(rsa_b.p, '\n\n', rsa_b.q, '\n\n')

    print(rsa_a.e, '\n', rsa_a.n, '\n', rsa_a.keypair[1][0])
    print(rsa_b.e, '\n', rsa_b.n, '\n', rsa_b.keypair[1][0])
    message = int(input('Message: '))
    encrypted = rsa_a.encrypt(rsa_a.keypair[0], message)
    decrypted = rsa_a.decrypt(rsa_a.keypair[1], encrypted)
    sign_a = rsa_a.sign(message, rsa_a.keypair[1][1], rsa_a.keypair[1][0])
    sign_b = rsa_b.sign(message, rsa_b.keypair[1][1], rsa_b.keypair[1][0])
    print(encrypted)
    print(decrypted)
    print(sign_a)
    print(sign_b)
    # s = pow(message, rsa_a.keypair[1][0], rsa_a.keypair[1][1])
    # verify = rsa_a.verify(message, s, rsa_a.e, rsa_a.n)
    # key = rsa_a.send_key(message, rsa_a.e, rsa_a.n, rsa_a.keypair[1][0], rsa_b.n)
    # recieved = rsa_b.recieve_key(message, rsa_b.e, rsa_b.n, rsa_b.keypair[1][0], rsa_a.n)


if __name__ == '__main__':
    main()
