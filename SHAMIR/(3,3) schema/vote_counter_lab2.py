import ss_function as ss_f
#设置模数 p
p=1000000007
#随机选取两个参与方，例如 student2 和 student3，获得 d2,d3，从而恢复出 d=a+b+c
#读取 d2,d3
d_123=[]
for i in range(1,4):
 with open(f'd_{i}_lab2.txt', "r") as f: #打开文本
  d_123.append(int(f.read())) #读取文本
#加法重构获得 d
d=ss_f.restructure_polynomial([1,2,3],d_123,3,p)
d=d/3;
print(f'秘密值的平均值为：{d}')
