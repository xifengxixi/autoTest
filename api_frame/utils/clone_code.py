import sys
import os

parameter1 = sys.argv[1]
list = [parameter1]
print(list)
for type in list:
    if type[0:2] == '-m':
        parameter1 = type[2:]

# 判断当前路径下是否存在已拉取的代码文件，如果有则删除，如果没有则创建最新代码文件夹
path = f"d:\\new_master"
master_path = path + f'\\' + parameter1
master_flag = os.path.exists(master_path)

if master_flag:
    os.system(f'rmdir /s /q {master_path}')
    os.mkdir(master_path)
    os.chdir(master_path)
    os.system(f'git clone -b {parameter1} https://gitee.com/xifengxixi/autoTest.git')
else:
    os.mkdir(master_path)
    os.chdir(master_path)
    os.system(f'git clone -b {parameter1} https://gitee.com/xifengxixi/autoTest.git')
