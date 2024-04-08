import os


class ApiConfig:
    """
    运行测试配置
    """
    # 环境信息
    baseurl = "www.testingedu.com.cn:8000"
    # 初始化账号
    filename = "account.txt"
    # 是否https
    is_https = False
    # 超时时间
    timeout = 60
    # 是否打印traceId(所有接口,包括通过和失败的)
    is_traceId = True


    # 日志相关
    is_log = False
    is_stack = False
    is_headers = False
    is_body = False
    is_response = False
    API_FRAME_PATH = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(API_FRAME_PATH, "logs/")