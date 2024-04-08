import re
import os
import sys
import time
import pytest
import subprocess
import configparser
from py.xml import html
sys.path.append(os.getcwd())
sys.path.append(os.getcwd().split("api_frame")[0])
from api_frame.config import ApiConfig
from ui_frame.config import UiConfig


source_dir = os.getcwd()
if source_dir.find("ui_frame") > -1:
    account_filename = UiConfig.filename
else:
    account_filename = ApiConfig.filename


def get_user_account_conftest(file_name=account_filename):
    """
    获取人员帐号信息
    :param file_name:
    :return:
    """
    base_dir = os.path.dirname(__file__)
    base_dir = os.path.join(base_dir, 'testData')
    file_path = os.path.abspath(os.path.join(base_dir, file_name))
    user_file = open(file_path, 'r', encoding="UTF-8")
    users = user_file.readlines()
    name = []
    username = []
    password = []
    remark = []
    teams = []
    for u in users:
        name.append(u.split(',')[0].strip())
        username.append(u.split(',')[1].strip())
        password.append(u.split(',')[2].strip())
        remark.append(u.split(',')[3].strip())
        teams.append(u.split(',')[4].strip())
    return name, username, password, remark, teams


def get_base_url():
    base_url = ApiConfig.baseurl
    base_url = base_url.replace("apps", "www")
    return base_url


def pytest_sessionstart():
    """
    检查是否有requirements.txt文件，如果有则检查是否有缺失的库，如果有则安装
    :return:
    """
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
            with open('libs_backup.txt', 'w')as f:
                f.write(libs)
            with open('libs_backup.txt', 'r')as f:
                lines = f.readlines()
                for i in lines:
                    line = i.strip().split(' ')
                    if line[0] == 'Package':
                        pass
                    elif '---' in line[0]:
                        pass
                    else:
                        with open('doc.txt', 'a')as f:
                            f.write(f'{line[0]}=={line[len(line) - 1]}\n')
            os.remove('libs_backup.txt')
            lib_list = []
            try:
                with open('requirements.txt', 'r')as fr:
                    with open('doc.txt', 'r')as fd:
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


tags = ''
def pytest_configure(config):
    """
    获取 pytest.ini 文件中所有标签
    :param config:
    :return: pytest.ini中标签组成的列表：["module:module", "task:task"]
    """
    markers = config.getini("markers")
    #将markers信息赋值给上方的tags
    global tags
    tags = markers


def passedRate(summary):
    """
    获取报告通过率
    :param summary:
    :return:
    """
    reg = re.compile(r'\d+')
    passed = int(reg.findall(str(summary[3]))[0])
    failed = int(reg.findall(str(summary[9]))[0])
    error = int(reg.findall(str(summary[12]))[0])
    if passed + failed + error == 0:
        return "0.00%"
    passRate = f'{(passed/(passed + failed + error))*100}%'
    return passRate


@pytest.mark.optionalhook
def pytest_html_results_summary(prefix, summary, postfix):
    """
    pytest_html报告添加测试环境、测试账号、全量测试通过率
    :param prefix:
    :param summary:
    :param postfix:
    :return:
    """
    passRate = passedRate(summary)
    try:
        https_conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'https_conf.ini')
        conf_file = configparser.ConfigParser()
        conf_file.read(https_conf_path, "utf-8")
        ht = 'https://' if ApiConfig.is_https else 'http://'
    except:
        import time
        time.sleep(1)
        https_conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'https_conf.ini')
        conf_file = configparser.ConfigParser()
        conf_file.read(https_conf_path, "utf-8")
        ht = 'https://' if ApiConfig.is_https else 'http://'
    prefix.extend([html.p("测试环境: " + ht + get_base_url())])
    prefix.extend([html.h2("测试账号:")])
    cells = [
        html.th('用户名'),
        html.th('账号'),
        html.th('密码'),
        html.th('备注'),
        html.th('团队')
    ]
    cell_data = []
    account_tuple = get_user_account_conftest()
    name_list = account_tuple[0]
    uid_list = account_tuple[1]
    password_list = account_tuple[2]
    text_list = account_tuple[3]
    depart_list = account_tuple[4]
    for i in range(len(name_list)):
        cell_data.append(
            html.tr([
                html.th(name_list[i], width="100px"),
                html.th(uid_list[i], width="250px"),
                html.th(password_list[i], width="100px"),
                html.th(text_list[i], width="100px"),
                html.th(depart_list[i], width="180px")
            ])
        )
    prefix.extend([html.table([html.thead(html.tr(cells), html.tr(cell_data))], border="1")])
    prefix.extend([html.h2(f"全量测试通过率: {passRate}")])


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    """
    pytest_html报告添加Description、failinfo、tags表头
    :param cells:
    :return:
    """
    cells.insert(1, html.th('Description'))
    # cells.insert(2, html.th('Test_nodeid'))
    # cells.pop(2)
    cells.insert(6, html.th('failinfo'))
    cells.insert(7, html.th('tags'))


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    """
    将用例描述写入到报告中，收集并检测是否有错误信息影响整体用例运行
    :param report:
    :param cells:
    :return:
    """
    fail_locations = os.environ.get("FAIL_LOCATION", '').split(";")
    fail_reasons = os.environ.get("FAIL_REASON", '').split(";")
    date_string = time.strftime("%y/%m/%d-%H:%M")

    try:
        cells.insert(1, html.td(report.description))
    except:
        # 使用正则表达式从报错信息中提取详细报错
        fail_location = (report.location)[0]
        fail_reason_match = re.search(r"E.*Error.*", report.longreprtext)
        fail_reason_str = fail_reason_match.group(0) if fail_reason_match else ''
        fail_locations.append(fail_location)
        fail_reasons.append(fail_reason_str)

    # 写入文件
    with open("check_results.txt", "w") as f:
        if len(fail_locations) == 0:
            f.write("checkResult=%s" % '<span style="color:green;">本次预检测成功！</span>' + "\n")
            f.write("title=%s" % '成功' + "\n")
            f.write("time=%s" % date_string)
        else:
            fail_locations = [loc for loc in fail_locations if loc]
            fail_reasons = [reason for reason in fail_reasons if reason]
            if len(fail_locations) > 0:
                error_list = []
                for i in range(len(fail_locations)):
                    error_str = "<b>出错位置（%d）：</b>%s<br><b>出错原因：</b>%s<hr>" % (i + 1, fail_locations[i], fail_reasons[i])
                    error_list.append(error_str)
                error_string = "".join(error_list)
                f.write("checkResult=%s" % error_string + "\n")
                f.write("title=%s" % '失败' + "\n")
            else:
                f.write("checkResult=%s" % '<span style="color:green;">本次预检测成功！</span>' + "\n")
                f.write("title=%s" % '成功' + "\n")
            f.write("time=%s" % date_string)
            os.environ["FAIL_LOCATION"] = ';'.join(fail_locations)
            os.environ["FAIL_REASON"] = ';'.join(fail_reasons)


@pytest.mark.optionalhook
def pytest_html_results_table_html(report, data):
    """
    pytest_html报告删除通过用例的测试报告内容用指定内容替换，避免报告中显示多余的内容
    :param report:
    :param data:
    :return:
    """
    if report.passed:
        data =data
        del data[:]
        data.append(html.div('No log output captured.', class_='empty log'))


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    生成pytest_html报告，自定义测试报告内容和格式
    :param item:
    :param call:
    :return:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield # 暂停函数执行
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    report.description = str(item.function.__doc__)
    report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")
    if call.when == 'call' and report.failed == True:
        if 'AssertionError' in str(call.excinfo):
            report.extra = call.excinfo
            report.__setattr__('failinfo', call.excinfo)
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_")+".png"
            # ui自动化添加截图
            '''
            screen_img = _capture_screenshot(file_name)
            if file_name:
                html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:600px;height:300px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % screen_img
                extra.append(pytest_html.extras.html(html))
            '''
        report.extra = extra
        report.description = str(item.function.__doc__)
        report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")

    # 删除忽略后置操作的执行信息和报错信息
    if report.when == "teardown" and report.sections:
        if "teardown" in report.sections[-1][0]:
            report.sections.pop()


@pytest.fixture(autouse=True)
def add_interface_description_to_request_header(request):
    """
    将装饰器应用到接口函数
    :param request:
    :return:
    """
    interface_function = request.node
    if interface_function and hasattr(interface_function, "_obj") and callable(interface_function._obj):
        des = interface_function._obj.__doc__

        if not des:
            interface_description = "未提供用例描述"  # 如果没有描述，默认使用未提供接口描述
        else:
            interface_description = des
        os.environ.update({"nodeid_des": interface_function.nodeid})
        os.environ.update({"case_des": interface_description})
    yield
    os.environ.update({"nodeid_des": ""})
    os.environ.update({"case_des": ""})