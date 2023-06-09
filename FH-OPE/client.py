import pymysql
import random
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
from time import sleep

local_table = {}
key = get_random_bytes(16)
base_iv = get_random_bytes(16)

def AES_ENC(plaintext, iv):
    # AES加密
    aes = AES.new(key, AES.MODE_CBC, iv=iv)
    padded_data = pad(plaintext, AES.block_size, style='pkcs7')
    ciphertext = aes.encrypt(padded_data)
    return ciphertext

def AES_DEC(ciphertext, iv):
    # AES解密
    aes = AES.new(key, AES.MODE_CBC, iv=iv)
    padded_data = aes.decrypt(ciphertext)
    plaintext = unpad(padded_data, AES.block_size, style='pkcs7')
    return plaintext

def Random_Encrypt(plaintext):
    # 随机生成iv来保证加密结果的随机性
    iv = get_random_bytes(16)
    ciphertext = AES_ENC(iv + AES_ENC(plaintext.encode('utf-8'), iv), base_iv)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext.decode('utf-8')

def Random_Decrypt(ciphertext):
    plaintext = AES_DEC(base64.b64decode(ciphertext.encode('utf-8')) ,base_iv)
    plaintext = AES_DEC(plaintext[16:],plaintext[:16])
    return plaintext.decode('utf-8')

def CalPos(plaintext):
    # 插入plaintext，返回对应的Pos
    presum = sum([v for k, v in local_table.items() if k < plaintext])
    if plaintext in local_table:
        local_table[plaintext] += 1
        return random.randint(presum, presum + local_table[plaintext] - 1)
    else:
        local_table[plaintext] = 1
        return presum

def GetLeftPos(plaintext):
    return sum([v for k, v in local_table.items() if k < plaintext])

def GetRightPos(plaintext):
    return sum([v for k, v in local_table.items() if k <= plaintext])

def Insert(plaintext):
    ciphertext = Random_Encrypt(plaintext)
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='user',
                           passwd='123456', database='test_db')
    cur = conn.cursor()
    cur.execute(f"call pro_insert({CalPos(plaintext)},'{ciphertext}')")
    conn.commit()
    conn.close()

def Search(left, right):
    # 搜索[left,right]中的信息
    left_pos = GetLeftPos(left)
    right_pos = GetRightPos(right)
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='user',
                           passwd='123456', database='test_db')
    cur = conn.cursor()
    cur.execute(
        f"select ciphertext from example where encoding >= FHSearch({left_pos}) and encoding < FHSearch({right_pos})")
    rest = cur.fetchall()
    for x in rest:
        print(f"ciphtertext: {x[0]} plaintext: {Random_Decrypt(x[0])}")

if __name__ == '__main__':
    # 插入明文，同时设置了一部分重复的内容
    for ciphertext in ['apple', 'pear', 'banana', 'orange', 'cherry', 'apple', 'cherry', 'orange']:
        Insert(ciphertext)

    # 假设我们搜索b和p之间的数据
    Search('b', 'c')
    sleep(30) # 这里我们暂停100秒
    ciphertext='banana'
    Insert(ciphertext)
    Search('b', 'c')

    sleep(30) # 这里我们暂停100秒
    ciphertext='banana'
    Insert(ciphertext)
    Search('b', 'c')

    sleep(30) # 这里我们暂停100秒
    ciphertext='banana'
    Insert(ciphertext)
    Search('b', 'c')


