import allure
from .basePage import ModuleBasePage

class ModuleFuncPage(ModuleBasePage):
    """
    模块功能方法
    """

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step('模块方法')
    def module_business_func(self):
        """
        模块方法
        :return:
        """
        # 1. 调用模块公共方法
        self.module_common_func()
        # 2. 模块业务功能
        print('模块业务功能')

    @allure.step('搜索商品')
    def good_search(self, good_name):
        """
        搜索商品
        :param good_name:
        :return:
        """
        self.input_text_cls(good_name, parent_xpath='//div[contains(@class,"ecsc-search")]')

    @allure.step('进入商品详情页')
    def view_product_detail(self, product):
        """
        进入商品详情页
        :param product:
        :return:
        """
        card_loc = f'//*[contains(text(),"{product}")]/ancestor::div[contains(@class,"s_xsall")]/div[contains(@class,"xs_img")]'
        self.click_element(card_loc)