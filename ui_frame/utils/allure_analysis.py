import os
import json
import datetime
import arrow
import re


abspath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class allureAna():
    """
    allure报告分析，数据提取
    """

    def __init__(self, report_path):
        self.report_path = report_path
        self.attachments_path = os.path.join(self.report_path, r'data\attachments')
        self.testcases_path = os.path.join(self.report_path, r'data\test-cases')
        self.data_path = os.path.join(self.report_path, r'data')

    def get_caseFiles(self):
        """
        获取test-cases目录下的所有文件
        """
        path = self.testcases_path
        files = os.listdir(path)
        return files

    def read_caseFile(self, file):
        """
        读取test-cases目录下单个json文件的内容
        :param file:
        :return:
        """
        file_path = os.path.join(self.testcases_path, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            case = f.read()
        return case

    def read_suits_file(self):
        """
        读取data目录下suites.json文件的内容
        :return:
        """
        file_path = os.path.join(self.data_path, "suites.json")
        with open(file_path, 'r', encoding='utf-8') as f:
            suits = f.read()
        return suits

    def get_caseInfo(self, case):
        """
        获取用例信息
        :param case:
        :return:
        """
        case = json.loads(case)
        caseInfo_dict = {}
        # 用例uid
        caseInfo_dict['uid'] = case.get('uid')
        # 用例名称
        caseInfo_dict['name'] = case.get('name')
        # 用例路径
        caseInfo_dict['fullName'] = case.get('fullName')
        # 耗时/开始时间/结束时间
        caseInfo_dict['duration'] = case.get('time').get('duration')
        caseInfo_dict['start'] = case.get('time').get('start')
        caseInfo_dict['stop'] = case.get('time').get('stop')
        # 用例描述
        caseInfo_dict['description'] = case.get('description')
        # 用例状态
        caseInfo_dict['status'] = case.get('status')
        # 用例状态信息
        caseInfo_dict['statusMessage'] = case.get('statusMessage')
        # 用例异常信息
        caseInfo_dict['statusTrace'] = case.get('statusTrace')
        # 用例前置
        caseInfo_dict['beforeStages'] = case.get('beforeStages')
        # 测试步骤（用例步骤/失败截图/日志/stdout/stderr）
        testStage_dict = self.get_testStage(case, need_content=True)
        caseInfo_dict.update(testStage_dict)
        # 用例后置
        caseInfo_dict['afterStages'] = case.get('afterStages')
        # allure路径
        allurePath_list,allure_dir = self.get_allurePath(case)
        caseInfo_dict['allurePath'] = allurePath_list
        # 参数
        caseInfo_dict['parameters'] = case.get('parameters')
        caseInfo_dict['suit_class'] = allure_dir.get('subSuite')
        # 类别/优先级
        extra_dict = self.get_extra(case)
        caseInfo_dict.update(extra_dict)
        return caseInfo_dict

    def get_all_caseInfo(self, write_file=False):
        """
        获取所有用例信息
        :param write_file:
        :return:
        """
        all_caseInfo = []
        files = self.get_caseFiles()
        for file in files:
            case = self.read_caseFile(file)
            caseInfo = self.get_caseInfo(case)
            all_caseInfo.append(caseInfo)
        if write_file:
            with open('all_caseInfo.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(all_caseInfo, indent=4, ensure_ascii=False))
        return all_caseInfo

    def get_testStage(self, case, need_content=True):
        """
        获取测试步骤
        :param case:
        :param need_content:
        :return:
        """
        testStage_dict = {}
        # 用例步骤
        testStage_dict['steps'] = case.get('testStage').get('steps')
        attachments = case.get('testStage').get('attachments')
        for i in attachments:
            if i.get('source'):
                if i.get('type') == 'image/png':
                    # 失败截图
                    testStage_dict['screenshot'] = os.path.join(self.attachments_path, i.get('source'))
                elif i.get('name') == 'log' and i.get('source'):
                    # log
                    log_path = os.path.join(self.attachments_path, i.get('source'))
                    testStage_dict['log'] = log_path
                    if need_content:
                        testStage_dict['log_content'] = self.read_txt(log_path)
                elif i.get('name') == 'stdout':
                    # stdout
                    stdout_path = os.path.join(self.attachments_path, i.get('source'))
                    testStage_dict['stdout'] = stdout_path
                    if need_content:
                        testStage_dict['stdout_content'] = self.read_txt(stdout_path)
                elif i.get('name') == 'stderr':
                    # stderr
                    stderr_path = os.path.join(self.attachments_path, i.get('source'))
                    testStage_dict['stderr'] = stderr_path
                    if need_content:
                        testStage_dict['stderr_content'] = self.read_txt(stderr_path)
        return testStage_dict

    def read_txt(self, path):
        """
        读取txt文件内容
        :param path:
        :return:
        """
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content

    def get_allurePath(self, case):
        """
        获取allure路径
        :param case:
        :return:
        """
        labels = case.get('labels')
        epic, feature, story = None, None, None
        allure_dir = {}
        for i in labels:
            if i.get('name') == 'epic':
                epic = i.get('value')
            elif i.get('name') == 'feature':
                feature = i.get('value')
            elif i.get('name') == 'story':
                story = i.get('value')
            elif i.get('name') == 'subSuite':
                allure_dir["subSuite"] = i.get('value')
        allure_path = [epic, feature, story]
        return allure_path,allure_dir

    def get_extra(self, case):
        """
        获取extra
        :param case:
        :return:
        """
        extra_dict = {}
        categories = case.get('extra').get('categories')
        extra_dict['categories'] = categories[0].get('name') if categories else None
        extra_dict['severity'] = case.get('extra').get('severity')
        return extra_dict


def deal_result(data):
    list_case = []
    packages = json.loads(data)
    result_map = {"passed": "成功", "skipped": "跳过"}
    for package in packages['children']:
        for item in package['children']:
            for suit in item['children']:
                for case in suit["children"]:
                    start_time = datetime.datetime.fromtimestamp(case['time']['start']/1000).strftime('%Y-%m-%d %H:%M:%S')  #
                    list_case.append({
                        "suit_class": suit['name'],
                        "case_name": case['name'],
                        "uid": case['uid'],
                        "parentUid": case['parentUid'],
                        "result": result_map.get(case['status'],"失败"),
                        "start_time": start_time,
                        "running_time": case['time']['duration'] / 1000
                    })
    return list_case

def get_allure_path():
    try:
        all_path = os.environ['PATH']
        list_path = all_path.split(";")
        for path in list_path:
            if path.find("allure") > -1:
                return os.path.join(path,"allure.bat")
    except:
        pass
    return r"allure.bat"

def filter_date_dir(dir_name,date_save=3):
    """判断文件日期是否在保存时间外"""
    time_save = arrow.now().shift(days=-date_save).format("YYYYMMDDHHmmss")
    match = re.search(r"\d{14}", dir_name)
    if match:
        file_date = match.group()
        if file_date < time_save:
            return True
    return False

if __name__ == '__main__':
    data = allureAna(r'D:\Downloads\temps\temps\report').read_suits_file()

