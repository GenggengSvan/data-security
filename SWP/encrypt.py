#!/usr/bin/python
#coding=utf-8

from Crypto.Cipher import DES3
import os

# 加密密码（长度必须是8的倍数）
Key = 'This is a 24-byt'
Iv = 'This is '

def Encrypt(key,iv):
    for filename in os.listdir("./raw/"):
        # 创建一个DES3加密器
        cipher = DES3.new(key, DES3.MODE_CBC, iv)
        # 需要加密的文件路径
        with open(os.path.join('./raw/', filename), 'rb') as f:
            # 创建一个新的加密后的文件
            with open(os.path.join('./encryption/', filename + '.enc'), 'wb') as enc_file:
                while True:
                    # 每次读取8字节的数据块
                    data = f.read(8)
                    # 如果读到文件末尾，则停止循环
                    if not data:
                        break
                    # 如果读到的数据块长度不是8字节，则用空字节补齐
                    if len(data) < 8:
                        data += b"\0" * (8 - len(data))
                    # 将数据块加密
                    enc_data = cipher.encrypt(data)
                    # 将加密后的数据块写入新文件
                    enc_file.write(enc_data)



Encrypt(Key,Iv)


