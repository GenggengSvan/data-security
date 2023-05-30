#include "math.h"
#include <stdio.h>
#include <string.h>
#include "laplace.h"
#include "csvpackage.h"
#include <time.h>
extern int rand();
extern void srand(unsigned);


/*
函数功能：	对传入的csv文件查询结果，并对结果使用拉普拉斯噪音加噪
输入参数说明：
path		csv文件的存储位置
beta		拉普拉斯分布参数
seed	    长整型指针变量， *seed 为伪随机数的种子
*/
double csv_analysis(char* path, double beta, long int seed)
{
	//读取指定路径的数据集
	FILE *original_file = fopen(path,"r+"); 
	struct Animals * original_data = NULL;
	original_data = csv_parser(original_file);
	//查询数据集中满足条件的真实结果
	double sum=0;
	int i=0;
	while(original_data[i].name)
	{
		if(original_data[i].carrots>=55)
			sum++;
		i++;
	}
	double x=0;
	x = laplace_data(beta,&seed); //产生拉普拉斯随机数
	printf("Added noise:%f\n",x); //此处分别列出了每条具体添加的噪音和加噪的结果。当投入较少预算时，可能会出现负数
	sum=sum+x;
	printf("Animals which carrots cost > 55 (Under DP):未舍入：%f\t舍入后：%0.f\n",sum,round(sum)); //输出加噪后的搜索结果中，每日食用胡萝卜大于55的动物个数
    return sum;
}

/*
参数表：
seed	    长整型指针变量， *seed为伪随机数的种子
sen			数据集的敏感度
x			用于储存拉普拉斯分布噪音的临时变量
beta		隐私预算，在输入后根据公式转换为拉普拉斯分布参数
*/
int main()
{
	long int seed;
	int sen = 1;  //对于一个单属性的数据集，其敏感度为1
    int num=20; //支持查询次数
    int num_all=200; //实验中的查询次数
	double beta;
	srand((unsigned)time( NULL )); //生成基于时间的随机种子（srand方法）
	beta = 0;
	printf("Please input laplace epsilon:");
	scanf("%lf", &beta);
	if(beta<=0 || !beta)//当输入的beta值无效时，默认设定beta值为1
	{
		beta = 1.0;
	} 
	printf("Under privacy budget %f, sanitized original data with fake animal name and laplace noise:\n",beta);
	beta = sen / (beta/num); //拉普拉斯机制下，实际公式的算子beta为敏感度/预算
	                         //在交互式方法下，预算的计算与 查询次数k 有关，预算= 输入预算/k，在查询次数内满足 e-差分隐私
	
	//查询num_all次，输出每次查询结果和查询i次后计算的平均值
	double sum_all=0;
	for(int i=0;i<num;i++){
		seed = rand()%10000+10000; //随机种子产生
	    printf("第 %d 次查询：",i+1);
	    sum_all+=csv_analysis("./zoo.csv",beta,seed); 
	    printf("第 %d 次查询后的平均值 %f 舍入后：%0.f\n\n",i+1,(sum_all/(i+1)),round(sum_all/(i+1)));
	}

	//获取真实的查询结果作为对照
	FILE *original_file = fopen("./zoo.csv","r+"); 
	struct Animals * original_data = NULL;
	original_data = csv_parser(original_file);
	int sum=0,i=0;
	while(original_data[i].name)
	{
		if(original_data[i].carrots>=55)
			sum++;
		i++;
	}
	printf("Animals which carrots cost > 55 (original): %d\n",sum);

	printf("==================Using neighbour dataset==================\n");

	//查询邻居数据集（比原数据集少一行数据）
	sum_all=0;
	for(int i=0;i<num;i++){
		seed = rand()%10000+10000; //随机种子产生
	    printf("第 %d 次查询：",i+1);
	    sum_all+=csv_analysis("./zoo_nb.csv",beta,seed); 
	    printf("第 %d 次查询后的平均值 %f 舍入后：%0.f\n\n",i+1,(sum_all/(i+1)),round(sum_all/(i+1)));
	}

	//获取邻居数据集真实的查询结果作为对照
	FILE *original_file_nb = fopen("./zoo_nb.csv","r+"); 
	struct Animals * original_data_nb = NULL;
	original_data_nb = csv_parser(original_file_nb);
	sum=0,i=0;
	while(original_data_nb[i].name)
	{
		if(original_data_nb[i].carrots>=55)
			sum++;
		i++;
	}
	printf("Animals which carrots cost > 55 (original): %d\n",sum);

	return 0;
}