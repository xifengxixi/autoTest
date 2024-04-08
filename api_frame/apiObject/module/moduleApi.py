import os
import sys
sys.path.append(os.getcwd())
sys.path.append("..")
from api_frame.apiObject.base.baseApi import BaseApi
from api_frame.utils.get_api_desc import get_doc_info

requests = BaseApi().http_timeout()
@get_doc_info
class Module_API(BaseApi):

    def __init__(self):
        self.base_url = BaseApi().baseurl()

    def login(self, username='13800138006', password='123456', verify_code='aaaa'):
        """
        testingedu登录
        :param username:
        :param password:
        :param verify_code:
        :return:
        """
        url = f'http://{self.base_url}/index.php?m=Home&c=User&a=do_login&t=0.010459923089728207'
        headers = {
            'Content-Type': 'text/html; charset=UTF-8'
        }
        payload = {
            'username': username,
            'password': password,
            'verify_code': verify_code
        }
        response = requests.request("POST", url, headers=headers, params=payload)
        assert response.status_code == 200, f"testingedu登录失败，resp:{response.text}"
        return response.json()

    def get_province(self, PHPSESSID, **kwargs):
        """
        首页-手机数码-获取省份
        :param PHPSESSID:
        :param kwargs:
        :return:
        """
        url = f'http://{self.base_url}/index.php'
        headers = {
            'Content-Type': 'text/html; charset=UTF-8',
            'Cookie': f'PHPSESSID={PHPSESSID}'
        }
        payload = {
            'm': 'Home',
            'c': 'Api',
            'a': 'getProvince'
        }
        payload.update(kwargs)
        response = requests.request("GET", url, headers=headers, params=payload)
        assert response.status_code == 200, f"首页-手机数码-获取省份失败，resp:{response.text}"
        return response.json()

    def searchKey(self, PHPSESSID, key, **kwargs):
        """
        首页-手机数码-搜索
        :param PHPSESSID:
        :param key:
        :param kwargs:
        :return:
        """
        url = f'http://{self.base_url}/Home/Api/searchKey.html'
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Cookie': f'PHPSESSID={PHPSESSID}'
        }
        payload = {
            'key': key
        }
        payload.update(kwargs)
        response = requests.request("POST", url, headers=headers, params=payload)
        assert response.status_code == 200, f"首页-手机数码-搜索失败，resp:{response.text}"
        return response.json()