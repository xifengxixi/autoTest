import allure
import pytest
import os, sys
sys.path.append(os.getcwd())
from time import strftime
from ui_frame.config import UiConfig
from pageObject.module.funcPage import ModuleFuncPage
from api_frame.apiObject.module.moduleApi import Module_API


base_url = UiConfig.base_url

@pytest.fixture(scope="class", autouse=True)
def class_fixture(browser, class_login):
    global driver, funcPage
    driver = browser
    funcPage = ModuleFuncPage(driver)


@allure.epic("xx项目")
@allure.feature("xx模块-xx功能")
class TestModule:

    def setup_class(self):
        # 页面
        self.funcPage = funcPage
        # 接口
        self.moduleApi = Module_API()
        # 其它
        self.driver = driver
        self.base_url = self.funcPage.base_url

    def setup_method(self):
        '''每个用例开始前'''
        self.now = strftime("%Y%m%d%H%M%S")

    def teardown_method(self):
        '''每个用例结束之后执行'''
        self.funcPage.keep_a_window()

    @allure.story('打开首页-进入商品详情')
    def test_module_AAA_case(self):
        """
        打开首页-进入商品详情
        :return:
        """

        # 1. 打开手机数码页面
        self.funcPage.load_url(self.funcPage.page_url.get('手机数码'))

        # 2. 进入商品详情页
        self.funcPage.view_product_detail('nvc')

        # 3. 测试模块业务
        self.funcPage.module_business_func()

        # 4. 新开一个窗口，打开首页
        self.funcPage.new_window_load_url(self.funcPage.page_url.get('首页'))
