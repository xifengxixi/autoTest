import sys, os
import re
import time
import pytest
path = os.getcwd()
api_path = path.split("ui_frame")[0] + "api_frame"
sys.path.append(api_path)
sys.path.append(rf'{api_path}\test_case')
sys.path.append(rf'{path}\pageObject')
sys.path.append(path)
sys.path.append(path.split("ui_frame")[0])

from api_frame.config import ApiConfig
from ui_frame.config import UiConfig

_TEMPS = UiConfig.temp_dir
environment_path = UiConfig.testdata_dir + '/environment.properties'

mode = sys.argv[1:]
base_url = mode[0]
is_https = mode[1]
is_all = mode[2]
try:
    moudle = mode[3]
except:
    moudle = ','
os.environ.update({"is_all": is_all})
ApiConfig.baseurl = base_url

if __name__ =="__main__":
    if os.path.exists(_TEMPS):
        for root, dirs, files in os.walk(_TEMPS):
            for name in files:
                os.remove(os.path.join(root, name))
    moudle_list = moudle.split(",")
    moudle_list = [i for i in moudle_list if i != ""]
    with open(environment_path, 'w') as f:
        f.write('base_url={}'.format(base_url))
    with open(environment_path, 'r') as f:
        properties = f.read()
    with open(rf'{_TEMPS}/environment.properties', 'w') as f:
        f.write(properties)
    if len(moudle_list) == 0:
        code = ['--alluredir', _TEMPS, '-v', '-s', rf'{path}/testcases']
    else:
        test_path = rf'{path}/testcases'
        code = ['--alluredir', _TEMPS, '-v', '-s']
        for m in moudle_list:
            code.append(rf'{test_path}/{m}')
    now = time.strftime("%Y%m%d%H%M%S")
    api_test_path = path.split('ui_frame')[0] + "/api_frame"
    pathcase = api_test_path + "/testCase"
    os.chdir(pathcase)
    if is_https.strip() == "True":
        ApiConfig.is_https = True
        base_url = "https://" + base_url
        with open(rf'{path}\config.py', "r", encoding="utf-8") as f:
            content = f.read()
            content = re.sub(r'base_url = ".*"', f'base_url = "{base_url}"', content)
        with open(rf'{path}\config.py', "w", encoding="utf-8") as f:
            f.write(content)
    else:
        ApiConfig.is_https = False
        base_url = "http://" + base_url
        with open(rf'{path}\config.py', "r", encoding="utf-8") as f:
            content = f.read()
            content = re.sub(r'base_url = ".*"', f'base_url = "{base_url}"', content)
        with open(rf'{path}\config.py', "w", encoding="utf-8") as f:
            f.write(content)
    pytest.main([pathcase + "/a_initUser",
                 '-m initUser',
                 "--self-contained-html",
                 "--reruns", "1"])
    with open(path.split('ui_frame')[0] + "/api_frame/testData/account.txt", "r", encoding="utf-8") as f:
        account = f.read()
    with open(path + "/testData/account.txt", "w", encoding="utf-8") as f:
        f.write(account)
    if not os.path.exists(UiConfig.screen_dir):
        os.makedirs(UiConfig.screen_dir)
    print('-----------------开始执行UI自动化-----------------')
    print(f'-----------------当前执行环境:{base_url}-----------------')
    pytest.main(code)
