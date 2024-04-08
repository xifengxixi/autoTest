import os
from datetime import datetime


class UiConfig:
    """
    selenium相关
    """
    # 浏览器驱动（不需要修改）
    driver = None
    driver2 = None
    # 元素等待显示等待时长（秒）
    timeout = 15
    # 元素等待显示等待间隔（秒）
    poll_frequency = 0.5
    # 浏览器类型
    browser_type = "chrome"
    # 调试模式
    debug = True
    # 基础url
    base_url = "http://www.testingedu.com.cn:8000"
    # 失败重跑次数
    reruns = "0"
    # 初始化账号
    filename = "account.txt"

    """
    路径相关
    """
    # 根路径
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # 指定Chromedriver下载路径
    driver_path = None
    # 用例路径
    testcase_dir = os.path.join(base_dir,"testCase")
    # 数据路径
    testdata_dir = os.path.join(base_dir,"testData")
    # 测试报告路径
    reports_dir = os.path.join(base_dir, "reports/{}".format(str(datetime.now().strftime('%Y%m%d_%H%M%S'))))
    temp_dir = os.path.join(base_dir, "reports/temps")
    # 失败截图
    screen_dir = os.path.join(base_dir, r"reports/screenshot/")
    # 日志路径
    log_dir = os.path.join(base_dir, r"logs")
    # 是否开启日志
    is_log = True
