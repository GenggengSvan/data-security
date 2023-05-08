#!/usr/bin/python
#coding=utf-8

from Crypto.Cipher import DES3
import os

# 加密密码（长度必须是8的倍数）
Key = 'This is a 24-byt'
Iv = 'This is '

def Decrypt(key,iv):
    for filename in os.listdir("./encryption/"):
        # 创建一个DES3加密器
        cipher = DES3.new(key, DES3.MODE_CBC, iv)
        # 打开需要解密的文件
        with open(os.path.join('./encryption/', filename), 'rb') as enc_file:
            # 创建一个新的解密后的文件
            with open(os.path.join('./decryption/', filename[:len(filename)-4] + '.txt'), "wb") as decrypted_file:
                while True:
                    # 每次读取8字节的数据块
                    enc_data = enc_file.read(8)
                    # 如果读到文件末尾，则停止循环
                    if not enc_data:
                        break
                    # 如果读到的数据块长度不是8字节，则用空字节补齐
                    if len(enc_data) < 8:
                        enc_data += b"\0" * (8 - len(enc_data))
                    # 将数据块解密
                    data = cipher.decrypt(enc_data)
                    # 将解密后的数据块写入新文件
                    decrypted_file.write(data)

Decrypt(Key,Iv)
