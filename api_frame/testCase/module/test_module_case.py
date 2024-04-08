import pytest
from time import strftime
from apiObject.module.moduleApi import Module_API


@pytest.mark.module
class Test_module:

    def setup_class(cls):
        """setup_class"""
        cls.Module_API = Module_API()
        cls.get_value = cls.Module_API.get_value
        cls.PHPSESSID = cls.Module_API.get_PHPSESSID()

        print("这是setup_class")

    def setup_method(cls):
        """setup_method"""
        cls.now = strftime("%Y%m%d%H%M%S")
        print("这是setup_method")

    def teardown_method(cls):
        """teardown_method"""
        print("这是teardown_method")

    def teardown_class(cls):
        """teardown_class"""
        print("这是teardown_class")

    def test_module_AAA_mobile_search(self):
        """手机数码搜索"""
        PHPSESSID = self.PHPSESSID

        # # 1. 登录
        # res_login = self.Module_API.login()
        # PHPSESSID = self.get_value(res_login, ['result', 'token'])

        # 2. 获取省份
        res_province = self.Module_API.get_province(PHPSESSID)
        assert res_province['status'] == 1, "获取省份失败"

        # 3. 搜索
        res_search = self.Module_API.searchKey(PHPSESSID, 'vivo')
        assert res_search['status'] == 1, "搜索失败"