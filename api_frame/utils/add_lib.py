import os
import time
import subprocess


def addLibs():
    path = os.path.abspath(os.path.dirname(__file__))
    path = path.split('api_frame')[0]
    path = f'{path}api_frame'
    os.chdir(path)
    file_name = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_name.append(file)
    try:
        if 'requirements.txt' in file_name:
            libs = os.popen('pip list').read()
            with open('libs_backup.txt', 'w') as f:
                f.write(libs)
            with open('libs_backup.txt', 'r') as f:
                lines = f.readlines()
                for i in lines:
                    line = i.strip().split(' ')
                    if line[0] == 'Package':
                        pass
                    elif '---' in line[0]:
                        pass
                    else:
                        with open('doc.txt', 'a') as f:
                            f.write(f'{line[0]}=={line[len(line) - 1]}\n')
            os.remove('libs_backup.txt')
            lib_list = []
            try:
                with open('requirements.txt', 'r') as fr:
                    with open('doc.txt', 'r') as fd:
                        requirments = fr.readlines()
                        doc = fd.read()
                        for fr_line in requirments:
                            if fr_line not in doc:
                                lib_list.append(fr_line.strip())
                if len(lib_list) != 0:
                    print('发现缺少以下版本')
                    print(lib_list)
                    time.sleep(2)
                    print('升级当前PIP')
                    cmd = 'python -m pip install --upgrade pip -i https://pypi.douban.com/simple'
                    output = subprocess.Popen(
                        cmd, shell=True, stdout=subprocess.PIPE)
                    for line in output.stdout:
                        print(line)
                    for lib in lib_list:
                        print(f'当前正在安装 {lib}, 请稍等...')
                        cmd = f'pip install -i http://pypi.douban.com/simple/ {lib} --trusted-host pypi.douban.com'
                        output = subprocess.Popen(
                            cmd, shell=True, stdout=subprocess.PIPE)
                        for line in output.stdout:
                            print(line)
                    print('所有缺失库已安装完成')
                else:
                    print('当前未发现缺失第三库')

            finally:
                try:
                    print(os.getcwd())
                    os.remove('doc.txt')
                except:
                    pass
        else:
            raise ('请在api_frame文件夹下添加requirements.txt')
    except:
        pass

