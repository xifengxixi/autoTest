from common.base import Page


class Title(Page):
    """
    Title标题组件
    title_click_right_button: 点击标题右侧【打开】、【跳转】、【开始运行】按钮
    title_click_tab_by_name: 切换或者悬停标题下方tab选项
    title_hover_and_click_more_option: 悬浮标题下方tab【更多】-点击【更多】中的选项
    """

    def title_click_right_button(self, button_name, parent_xpath=""):
        """
        点击标题右侧【打开】、【跳转】、【开始运行】按钮
        @param button_name: 按钮名称
        @param parent_xpath: 父级定位
        @return:
        """
        loc = parent_xpath + f"//div[contains(@class,'title')]//button[contains(text(),'{button_name}')]"
        self.click_element(loc)

    def title_click_tab_by_name(self, tab_name, parent_xpath="", hover=False):
        """
        切换或者悬停标题下方tab选项
        @param tab_name: tab页名称
        @param parent_xpath:
        @param hover: 是否为悬停操作
        @return:
        """
        loc = parent_xpath + f"//div[contains(@class,'ui-menu-tab-top-container')]//span[contains(text(),'{tab_name}')]"
        if hover:
            # 悬停操作
            self.move_on(loc)
        else:
            # 点击操作
            self.click_element(loc)

    def title_hover_and_click_more_option(self, more_option_name, parent_xpath=""):
        """
        悬浮标题下方tab【更多】-点击【更多】中的选项
        @param more_option_name: 【更多】中选项名称
        @param parent_xpath:
        @return:
        """
        self.title_click_tab_by_name("更多", hover=True)
        self.sleep(0.5)
        loc = parent_xpath + f"//div[@class='ui-scroller ui-menu-scroller']//div[@class='ui-menu-list']//div[@title='{more_option_name}']"
        self.click_element(loc)

    def title_get_text(self, parent_xpath=""):
        """
        获取标题文本信息
        @param parent_xpath:
        @return:
        """
        loc = parent_xpath + "//div[@class='ui-title-title-top']"
        return self.get_element_text(loc)
