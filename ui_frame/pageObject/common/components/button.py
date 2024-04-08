from common.base import Page


class Button(Page):
    """
    按钮组件
    click_button:根据按钮名称点击按钮
    """

    def click_button(self, button_name, parent_xpath="",**kwargs):
        """
        根据按钮名称点击按钮
        :param button_name:
        :param parent_xpath:
        :param kwargs:
        :return:
        """
        if kwargs.get("text_contains"):
            loc = parent_xpath + f"//button[contains(text(),'{button_name}')]"
        else:
            loc = parent_xpath + f"//button[text()='{button_name}']"
        self.click_element(loc)

    def click_button_to_span(self, button_name, parent_xpath="", **kwargs):
        """
        根据button名称点击按钮,button下面有span
        :param button_name: 按钮名称 str
        :param parent_xpath:
        :param kwargs:
        :return:
        """
        loc = parent_xpath + f'//button/span[text()="{button_name}"]'
        if kwargs.get("fuzzy"):
            loc = parent_xpath + f"//button//span[contains(text(),'{button_name}')]"
        if kwargs.get("rootLoc"):
            loc = loc + "/ancestor::button"
        self.click_element_disWait(loc)

    def click_button_wait(self, button_name, parent_xpath="", **kwargs):
        """
        根据按钮名称等待按钮可点击点击按钮
        :param button_name:
        :param parent_xpath:
        :param kwargs:
        :return:
        """
        if kwargs.get("text_contains"):
            loc = parent_xpath + f"//button[contains(text(),'{button_name}')]"
        else:
            loc = parent_xpath + f"//button[text()='{button_name}']"
        self.click_element_disWait(loc)

    def click_button_by_title(self, button_name, parent_xpath="",**kwargs):
        """
        根据按钮title名称点击按钮
        :param button_name:
        :param parent_xpath:
        :param kwargs:
        :return:
        """
        if kwargs.get("title_contains"):
            loc = parent_xpath + f"//button[contains(@title,'{button_name}')]"
        else:
            loc = parent_xpath + f"//button[@title='{button_name}']"
        self.click_element(loc)
        self.sleep(0.5)