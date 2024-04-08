import allure
from pageObject.common.components import components


class ModuleBasePage(components):
    """
    模块基础方法
    """

    page_url = {
        "首页": "/home/Index/index.html",
        "手机数码": "/Home/Goods/goodsList/id/31.html",
        "手机分类": "/Home/Goods/goodsList/id/587.html",
        "智能/国产": "/Home/Goods/goodsList/id/588.html",
        "服装服饰": "/Home/Goods/goodsList/id/12.html",
        "电脑配件": "/Home/Goods/goodsList/id/37.html",
        "家具家居": "/Home/Goods/goodsList/id/30.html",
        "电器工具": "/Home/Goods/goodsList/id/52.html",
        "食品生鲜": "/Home/Goods/goodsList/id/55.html",
    }

    @allure.step('xx模块公共方法')
    def module_common_func(self):
        """xx模块公共方法"""
        print('xx模块公共方法')