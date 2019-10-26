from string import ascii_lowercase
from Cipher import Cipher

class AffineZ26(Cipher):
    
    __alphabet = dict(zip(ascii_lowercase, range(0,26)))
    __inverted_alphabet = {code: letter for letter, code in __alphabet.items()}
    __inverses = {
        1: 1,
        3: 9,
        5: 21,
        7: 15,
        9: 3,
        11: 19,
        15: 7,
        17: 23,
        19: 11,
        21: 5,
        23: 17,
        25: 25
    }
    
    @classmethod
    def encrypt(cls, text, key1, key2):
        encrypted = ''
        charset = set(cls.__alphabet.keys())
        for char in text:
            if char in charset:
                encrypted += cls.__inverted_alphabet[(key1 * cls.__alphabet[char.lower()] + key2) % len(cls.__alphabet)]
            else:
                encrypted += char
        return encrypted


    @classmethod
    def decrypt(cls, text, key1, key2):
        decrypted = ''
        charset = set(cls.__alphabet.keys())
        for char in text:
            if char in charset:
                decrypted += cls.__inverted_alphabet[(cls.__inverses[key1] * (cls.__alphabet[char.lower()] - key2)) % len(cls.__alphabet)]
            else:
                decrypted += char
        return decrypted


    @classmethod
    def cryptoanalysis(cls, encrypted, plain):
        for key1 in cls.__inverses.keys():
            for key2 in cls.__inverted_alphabet.keys():
                if (decrypted := cls.decrypt(encrypted, key1, key2)).startswith(plain):
                    return key1, key2, decrypted
        return -1, -1, ''


    @classmethod
    def bruteforce(cls, text):
        results = ''
        for key1 in cls.__inverses.keys():
            for key2 in cls.__inverted_alphabet.keys():
                results += cls.decrypt(text, key1, key2) + '\n'
        return results