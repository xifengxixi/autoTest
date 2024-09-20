import os
import time
import json
import urllib
import inspect
import panda as pd
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

        # 判断接口是否为openapi的接口，如果是则拦截并调用esb接口
        abs_path = os.path.abspath(__file__)
        info_path = os.path.join(abs_path.split('接口自动化测试')[0], r"接口自动化测试\test_data\openapi_interface_info.xlsx")
        df = pd.read_excel(info_path)
        openapi_info_list = df.to_dict(orient='records')
        openapi_url_list = [i['url'] for i in openapi_info_list]
        payload = {
            "resourceId": 1034472783597436932,
            "interfaceId": "",
            "requestUrl": {},
            "requestParams": {},
            "requestBody": {},
            "requestHeader": {}
        }
        no_token_list = ['/oauth2/authorize', '/oauth2/access_token']
        part_url = request.path_url.split("?")[0]
        if part_url in openapi_url_list:
            request_body = request.body
            request_url = request.url
            if isinstance(request_body, bytes):
                request_body = request_body.decode('utf-8')
            if part_url in no_token_list or "access_token" in request_url or "access_token" in request_body:
                try:
                    requestBody = json.loads(request_body)
                    payload['requestBody'].update(requestBody)
                except:
                    decoded_query = self.convert_url_str_to_dict(request_body)
                    requestParams = decoded_query
                    payload['requestParams'].update(requestParams)
                if len(request_url.split("?")) > 1:
                    requestParams = self.convert_url_str_to_dict(request_url.split("?")[1])
                    payload['requestParams'].update(requestParams)
                # 替换 payload 的 interfaceId
                interfaceId = [i["interfaceId"] for i in openapi_info_list if request.path_url.split("?")[0] == i["url"]][0]
                payload.update(interfaceId=interfaceId)
                # 替换 请求的body
                request.body = json.dumps(payload)
                # 替换 请求的method
                request.method = "POST"
                # 替换 请求的url
                baseUrl = request.url.split(request.path_url)[0].replace('api', 'weapp')
                request.url = baseUrl + "/api/bs/esb/setting/test/autoTest/1024828696408260622"
                # request.url = baseUrl + f"/api/bs/esb/setting/test/autoTest/{os.environ.get('userid')}"
                # 请求的header中添加ETEAMSID
                request.headers['ETEAMSID'] = os.environ.get("ETEAMSID_admin")
                request.headers['Content-Type'] = "application/json"
                request.headers['Content-Length'] = str(len(request.body))

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

    def convert_url_str_to_dict(self, query_str):
        """
        将 url字符串转换为字典
        :param query_str:
        :return:
        """
        # 解析查询字符串
        parsed_query = urllib.parse.parse_qs(query_str)

        # 将所有字段的值进行解码
        decoded_query = {}
        for key, value in parsed_query.items():
            # 由于 parse_qs 结果的值是列表，所以取第一个元素
            decoded_value = value[0]
            try:
                # 尝试将其解析为 JSON 对象
                decoded_value = json.loads(urllib.parse.unquote(decoded_value))
            except (json.JSONDecodeError, TypeError):
                # 如果解析失败，就保持原值
                decoded_value = urllib.parse.unquote(decoded_value)
            decoded_query[key] = decoded_value

        return decoded_query