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

class StreamCipher:
    def __init__(self):
        self.len =16

    def generate(self, key,raw):
        if len(key) < 16:
            key += b"\0" * (16 - len(key))
        if len(raw) < 16:
            raw += b"\0" * (16 - len(raw))
        cipher_ctr = AES.new(key, mode=AES.MODE_CTR, counter=Counter(nonce))
        return cipher_ctr.encrypt(raw)   
    
    def decrypt(self, enc):
        cipher_ctr = AES.new(key, mode=AES.MODE_CTR, counter=Counter(nonce))
        return cipher_ctr.decrypt(enc)

class AESCipher:
    def encrypt(self, key,raw):
        iv = 'This is uuuuuuuu'
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return cipher.encrypt(raw) 

# The final scheme for encryption
def encryptionScheme():
    # Remove all encrypted files
    os.popen('find ./ciphertext/ -maxdepth 1 -type f -delete')
    stream_cipher = StreamCipher()
    aes_cipher = AESCipher()
    for filename in os.listdir("./raw/"):
        with open(os.path.join('./raw/', filename), 'rb') as in_file:
            with open(os.path.join('./ciphertext/', filename + '.enc'), 'wb') as out_file:
                file_size = os.path.getsize(os.path.join('./raw/', filename))
                tempwordnum=0
                for word in nextWord(in_file):
                    tempwordnum+=1
                    my_word = word.ljust(32, '.')
                    EWi = aes_cipher.encrypt(ENCRYPTION_KEY,my_word)
                    EWi_length = len(EWi)/2
                    #first_half Li
                    Li = EWi[:EWi_length] 
                    #Random stream Si
                    STREAM_CIPHER_RAW = str(tempwordnum)
                    STREAM_CIPHER_KEY=str(file_size)
                    Si = stream_cipher.generate(STREAM_CIPHER_KEY,STREAM_CIPHER_RAW)
                    #Ki=f(K,Li)
                    Ki=aes_cipher.encrypt(ENCRYPTION_KEY,Li)
                    #FiSi=F(Ki,Si)
                    FiSi = aes_cipher.encrypt(Ki,Si)
                    Ti = Si + FiSi # lengh 282 
                    ciphertext = xorWord(EWi, Ti)
                    out_file.write(ciphertext)



encryptionScheme()

