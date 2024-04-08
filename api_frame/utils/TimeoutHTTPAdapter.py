import os
import time
import inspect
from requests.models import Response
from api_frame.config import ApiConfig
from ui_frame.config import UiConfig
from urllib.parse import quote
from requests.adapters import HTTPAdapter
from requests.exceptions import ReadTimeout
from api_frame.utils.log_util import logger


old_path = os.getcwd()
try:
    if old_path.find("ui_frame") > -1:
        is_https = UiConfig.base_url.find("https") > -1
    else:
        is_https = ApiConfig.is_https
    is_log = ApiConfig.is_log
except:
    time.sleep(1)
    if old_path.find("ui_frame") > -1:
        is_https = UiConfig.base_url.find("https") > -1
    else:
        is_https = ApiConfig.is_https
    is_log = ApiConfig.is_log


def get_caller_function_info():
    # 获取调用者的栈帧信息
    caller_frame = inspect.stack()[1]

    # 获取调用者的上级函数名称
    caller_function_name = caller_frame.function

    # 获取上级函数的源代码
    caller_source_lines, _ = inspect.getsourcelines(caller_frame.frame.f_globals[caller_function_name])

    # 获取上级函数的描述，通常在函数定义的下一行添加注释
    caller_description = None
    for line in caller_source_lines:
        if line.strip().startswith('#'):
            caller_description = line.strip('#').strip()
            break

    return caller_function_name, caller_description


class TimeoutHTTPAdapter(HTTPAdapter):

    def __init__(self, *args, **kwargs):
        self.timeout = int(kwargs.pop("timeout", ApiConfig.timeout))
        self.is_traceId = ApiConfig.is_traceId              # 是否记录traceId
        if is_log:
            self.is_headers = ApiConfig.is_headers          # 是否记录request.header
            self.is_body = ApiConfig.is_body                # 是否记录request.body
            self.is_response = ApiConfig.is_response        # 是否记录response
            self.is_stack = ApiConfig.is_stack
            self.logger = logger
        super().__init__(*args, pool_connections=20, pool_maxsize=20, pool_block=True, **kwargs)

    def send(self, request, **kwargs):
        doc = os.environ.get('api_doc')
        doc = doc.split("\n")[0] if doc else ""
        case_des = os.environ.get("case_des", "").strip()
        nodeid_des = os.environ.get("nodeid_des", "")

        kwargs.setdefault('verify', False)
        kwargs.setdefault('timeout', self.timeout)

        if not is_https:
            request.url = request.url.replace("https://", "http://")

        request.headers['X-Case-Description'] = quote(case_des)
        request.headers['X-Interface-Description'] = quote(doc)
        request.headers['x-access-NodeId'] = nodeid_des
        request.headers['t'] = 1
        # 如果接口超时，则自定义返回内容，告诉大家这个接口超时了
        request_duration = 0
        try:
            start_time = time.time()
            response = super().send(request, **kwargs)
            end_time = time.time()
            # 如果响应码不为5xx，4xx，则记录接口响应时间
            if response.status_code < 500:
                request_duration = round(end_time - start_time, 2)
        except ReadTimeout:
            response = Response()
            response.status_code = 500
            response.reason = {"message": f"报错原因:接口:{request.url},响应超过:{str(self.timeout)}秒"}

        # 去掉文件上传接口的body信息
        if request.url.endswith("/upload") and response.status_code != 200:
            request.body = ""
            response_data = "上传附件失败，具体原因不确定, 发生问题客户端时间：" + time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            response_data = response.text

        try:
            trace_id = response.headers["traceId"]
        except:
            # 某些接口没有traceId， 或者接口超时接口拿不到traceId
            trace_id = ""

        info = ('\n--url:{0};\n--request.headers:{1};\n--request.body:{2};\n--response.headers:{3};\n--response.body:{4};'
                '\n--traceId:{5};\n接口响应时间:{6}秒\n').format(
            request.url,
            request.headers,
            request.body or '',
            response.headers,
            response_data or response.reason,
            trace_id,
            request_duration
        )

        exc_info = '\n--[接口异常信息开始]--{}\n--[接口异常信息结束]--\n'.format(info)

        if response.status_code == 200:
            if is_log:
                request_headers = '\n--request.headers:{};'.format(request.headers) if self.is_headers else ''
                request_body = '\n--request.body:{};'.format(request.body) if self.is_body else ''
                response_headers = '\n--response.headers:{};'.format(response.headers) if self.is_response else ''
                response_body = '\n--response.body:{};'.format(response_data) if self.is_response else ''
                normal_info = '\n--url:{};{}{}{}{}\n'.format(request.url, request_headers, request_body,
                                                           response_headers, response_body)
            else:
                normal_info = None
            response_text = response.text
            if response_text:
                try:
                    res = response.json()
                    if self.is_traceId:
                        if isinstance(res, dict):
                            if 'code' in res.keys() and res['code'] != 200:
                                print(exc_info)
                            else:
                                print(f'--通过接口：--url:{request.url}; traceId：{trace_id}; 响应时间：{request_duration}秒')
                        else:
                            print(f'--通过接口：--url:{request.url}; traceId：{trace_id}; 响应时间：{request_duration}秒')
                    if is_log:
                        self.logger.info(normal_info)
                except ValueError:
                    if is_log:
                        self.logger.info(normal_info)
            elif is_log:
                self.logger.info(normal_info)
        else:
            if response.status_code == 302:
                return response
            print(exc_info)
        # os.environ.clear()
        return response