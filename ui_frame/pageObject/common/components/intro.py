from common.base import Page


class Intro(Page):
    """
    Intro引导页组件
    intro_click_by_name: 通过名称点击引导页按钮
    intro_close: 关闭引导页
    """

    def intro_click_by_name(self, name, parent_xpath=""):
        """
        通过名称点击引导页按钮
        @param name:
        @param parent_xpath:
        @return:
        """
        loc = parent_xpath + f"//div[@class='introjs-tooltipbuttons']//a[contains(text(),'{name}')]"
        self.click_element(loc)

    def intro_close(self):
        """关闭引导页"""
        # 引导页
        loc = "//div[contains(@class,'introjs-relativePosition')]"
        if self.is_element_exist(loc):
            # 关闭引导页
            skip_loc = "//a[contains(@class,'introjs-skipbutton')]"
            self.click_element(skip_loc)

    def intro_close_to_A(self):
        """关闭引导页-通过A标签"""
        loc = "//a[contains(@class,'introjs-skipbutton')]"
        if self.is_element_exist(loc):
            self.click_element(loc)
