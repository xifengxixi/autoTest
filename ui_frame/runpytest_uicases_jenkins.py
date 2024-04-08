import sys, os
import time
import requests
import pytest
import json
function_path = os.path.abspath('.')
function_path2 = os.path.join(function_path,"testCase")
function_path3 = os.path.join(function_path,"pageObject")
sys.path.append(function_path)
sys.path.append(function_path2)
sys.path.append(function_path3)
# 添加接口的路径
function_path4 = os.path.join(function_path.split("autoTest")[0],"autoTest","api_frame")
function_path5 = os.path.join(function_path4,"testCase")
sys.path.append(function_path4)
sys.path.append(function_path5)

from ui_frame.config import UiConfig
from ui_frame.utils.allure_analysis import allureAna,deal_result,get_allure_path,filter_date_dir
import subprocess
args = sys.argv[1:]
print(args)
# 获取测试用例集，字符串，用逗号隔开
plan_id = args[0]
package_id = args[1]
suit_id = args[2]
# 获取账号信息
account_id = args[3]
filename = args[4]
# 获取运行环境信息
base_url = args[5]
browser_type = args[6]
# 重试次数
rerun = 0
try:
    rerun = int(args[7])
except:
    pass

timeout = args[8]
task_id = args[9]
sererity = args[10]
job_name = args[11]
_TEMPS = UiConfig.temp_dir
environment_path = UiConfig.testdata_dir + '/environment.properties'

if __name__ =="__main__":

    path = os.getcwd()
    dir_path = os.path.join(path, "reports")
    # 删除3天之前的报告
    all_files = os.listdir(dir_path)
    files = [dt for dt in all_files if os.path.isdir(os.path.join(dir_path, dt)) and filter_date_dir(dt)]
    try:
        # 获取账号
        url = "http://host:port/auto/job/account/get/last/account"
        if account_id != "-1":
            data = {"id": [account_id]}
        else:
            data = {"job_name": job_name}
        res = requests.post(url=url, json=data).json()
        account = res["data"]["account"]
        account_id = res["data"]["id"]
        account_path = path + f'\\testdatas\\' + filename
        with open(account_path, "w", encoding="utf-8") as f:
            f.write(account)
        # 获取用例
        url = "http://host:port/ui/run/cases/get"
        data = {"plan_id": plan_id,"package_id":package_id,"suit_id":suit_id}
        case_res = requests.post(url=url, json=data).json()
        list_cases = case_res["data"]
        env_id = case_res["env_id"]
        list_case = ["::".join([case_path, case]) for case_path, cases in list_cases.items() for case in cases]
        UiConfig.base_url = base_url
        print("当前运行用例：", list_case)
        if len(list_case)<1:
            raise ValueError("没有有效的测试用例！")
        if not os.path.exists(UiConfig.screen_dir):
            os.makedirs(UiConfig.screen_dir)
        list_ex = [f'./{i}' for i in list_case]
        list_ex.extend(["--alluredir", _TEMPS,])
        if sererity != "all":
            list_ex.extend(["--allure-severities", sererity])
        if rerun > 0:
            print(f"设置重试次数：{rerun}")
            list_ex.extend(["--reruns", f"{rerun}"])
        # 清除temps文件内容
        all_files = os.listdir(_TEMPS)
        files = [dt for dt in all_files if os.path.isfile(os.path.join(_TEMPS, dt))]
        if files:
            for file in files:
                file_del_path = os.path.join(_TEMPS, file)
                os.remove(file_del_path)
        with open(environment_path, 'w') as f:
            f.write('base_url={}'.format(base_url))
        with open(environment_path, 'r') as f:
            properties = f.read()
        with open(rf'{_TEMPS}/environment.properties', 'w') as f:
            f.write(properties)
        pytest.main(list_ex)
        report_dir_name = time.strftime("%Y%m%d%H%M%S",time.localtime())
        report_dir = os.path.join(dir_path,report_dir_name)
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)
        time.sleep(1)
        allure_path = get_allure_path()
        subprocess.call([allure_path,"generate",_TEMPS,"-o",report_dir])
        allure_op = allureAna(report_dir)
        for i in range(10):
            if os.path.exists(allure_op.data_path):
                break
            time.sleep(3)
        data = allure_op.read_suits_file()
        list_case_data = deal_result(data)
        try:
            url = 'http://host:port/ui/run/cases/import'
            data = {
                "case_results":list_case_data,
                "env_id": env_id,
                "account_id":account_id,
                "plan_id":plan_id,
                "task_id":task_id,
                "report_dir":report_dir_name
            }
            analysis_res = requests.post(url=url, json=data).json()
            print("发送平台数据库，返回：",analysis_res)
            if analysis_res["code"] != 200:
                print("数据传给服务器数据库失败：", analysis_res["msg"])
        except Exception as e:
            print("数据传给服务器数据库失败：", e)
    except Exception as e:
        print(e)
        url = 'http://host:port/jenkins/task/update'
        data = {
            "dict_update": {"status": "运行失败"},
            "task_id": task_id
        }
        analysis_res = requests.post(url=url, data=json.dumps(data)).json()
        print("发送平台数据库，返回：", analysis_res)
        if analysis_res["code"] != 200:
            print("数据传给服务器数据库失败：", analysis_res["msg"])
