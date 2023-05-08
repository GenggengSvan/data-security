#!/usr/bin/python
#coding=utf-8

import re
import os
import base64
import struct
import sys
import traceback
from operator import xor
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util import Counter

nonce = 'c59bcf35'
ENCRYPTION_KEY = 'Sixteen byte key' 
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
# Isolating words and not any punctuation marks
r_word = re.compile("(\w[\w']*\w|\w)")

xorWord = lambda ss,cc: ''.join(chr(ord(s)^ord(c)) for s,c in zip(ss,cc))

def nextWord(fileobj):
    for line in fileobj:
        for word in r_word.findall(line):
            yield word

def chunksplit(chunk, length):
    return (chunk[0+i:length+i] for i in range (0, len(chunk), length))

class Counter:
    def __init__(self, nonce):
        assert(len(nonce)==8)
        self.nonce = nonce
        self.cnt = 0

    def __call__(self):
        righthalf = struct.pack('>Q',self.cnt)
        self.cnt += 1
        return self.nonce + righthalf

class AESCipher:
    def encrypt(self, key,raw):
        iv = 'This is uuuuuuuu'
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return cipher.encrypt(raw) 


# Search word
def searchScheme():
    while True:
        try:
            word2search = raw_input('\nEnter a word to search: ')
            if not word2search:
                print('Must enter some text to proceed')
                continue
            #以下模拟客户端处理过程，生成陷门Tw=(E(K,W),Ki=f(K,Li))
            word2search_padded = word2search.ljust(32, '.') 
            aes_cipher = AESCipher()
            #E(K,W)
            cipher2search = aes_cipher.encrypt(ENCRYPTION_KEY,word2search_padded)
            cipher2search_length = len(cipher2search)/2
            #first_half Li
            Li = cipher2search[:cipher2search_length] 
            #Ki=f(K,Li)
            Ki=aes_cipher.encrypt(ENCRYPTION_KEY,Li)
            for filename in os.listdir('./ciphertext/'):
                success = 0
                with open(os.path.join('./ciphertext/', filename), 'rb') as in_file:
                    in_data = in_file.read(32)
                    while in_data:
                        Ti = xorWord(cipher2search, in_data)
                        Ti = list(chunksplit(Ti, 16))
                        if aes_cipher.encrypt(Ki,Ti[0]) == Ti[1]:
                            success = 1;
                            break
                        in_data = in_file.read(32)
                print ('Present in {0}'.format(filename) if success==1 else 'Not present in {0}'.format(filename))
        except EOFError:
            print ('\nQuitting...\n')
            sys.exit(0)
        except Exception as e:
            print(traceback.format_exc())

searchScheme()
