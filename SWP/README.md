# song-wagner-perrig

Practical Techniques for Searches on Encrypted Data 论文中描述的最终方案的实现。

## 实验环境

Ubuntu 18.04虚拟机、Python 2.7并安装pycrypto包

## 文件目录

encrypt.py对/raw目录下文件加密（/raw目录下是文件明文），加密文件存储在/encryption目录下

trapdoorgenerate.py对/raw目录下文件进行陷门生成，生成陷门存储在/ciphertext目录下

search.py进行检索过程，输入单词，检索/ciphertext目录，获取存储该单词的明文文件

decrypt.py对/encryption目录下的加密文件进行解密，解密结果存储在/decryption目录下

