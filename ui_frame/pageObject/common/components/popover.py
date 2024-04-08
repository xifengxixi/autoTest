from common.base import Page


class Popover(Page):
    """
    Popover气泡卡片
    popover_get_popover_text：获取气泡卡片内容
    popover_check_popover_text：气泡卡片校验操作
    popover_click_popover：点击气泡卡片内容
    popover_click_icon：点击气泡卡片图标
    popover_input_text：气泡卡片输入文本
    """

    def popover_get_popover_text(self, parent_xpath=""):
        """
        获取气泡卡片内容
        :param parent_xpath:
        :return:
        """
        loc = '//div[contains(@class, "ui-trigger-popupInner") and not(contains(@class, "hidden"))]//div[contains(@class, "ui-popover-content")]'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        return self.get_element_text(ele_loc)

    def popover_check_popover_text(self, expect_value, parent_xpath=""):
        """
        气泡卡片校验操作
        :param expect_value: 气泡卡片内容期望值
        :param parent_xpath:
        :return:
        """
        actual_value = self.popover_get_popover_text(parent_xpath=parent_xpath)
        if str(actual_value).find(str(expect_value)) < 0:
            assert False, f"输入框气泡卡片校验失败，期望：{expect_value}，实际：{actual_value}"

    def popover_click_popover(self, popover_text, parent_xpath=""):
        """
        点击气泡卡片内容（如有Close，可点击关闭气泡卡片）
        :param popover_text:
        :return:
        """
        loc = '//div[contains(@class, "ui-trigger-popupInner") and not(contains(@class, "hidden"))]'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        if self.is_element_exist(ele_loc):
            text_loc = f'//*[text()="{popover_text}"]'
            text_loc = ele_loc + text_loc
            self.click_element(text_loc)
        else:
            raise Exception("没有找到气泡卡片")

    def popover_click_icon(self, icon_class, parent_xpath=""):
        """
        点击气泡卡片图标
        :param icon_class:
        :param parent_xpath:
        :return:
        """
        loc = f'{parent_xpath}//div[contains(@class, "ui-trigger-popupInner") and not(contains(@class, "hidden"))]'
        icon_loc = f'{loc}//div[contains(@class, "content")]//*[name()="svg" and contains(@class, "{icon_class}")]'
        self.click_element(icon_loc)

    def popover_input_text(self, text, position=1, needClearText=True, parent_xpath=''):
        """
        气泡卡片输入文本
        :param text:
        :param needClearText:
        :param parent_xpath:
        :return:
        """
        loc = (f'(//div[contains(@class, "ui-trigger-popupInner") and not(contains(@class, "hidden"))]'
               f'//div[contains(@class, "ui-popover-content")]{parent_xpath}//input)[position()={position}]')
        ele = self.find_element(loc)
        self.input_text(ele, text, needClearText)

    def popover_click_loc(self, loc, parent_xpath='', position=1):
        """
        气泡卡片点击元素
        :param loc:
        :param parent_xpath:
        :param position:
        :return:
        """
        loc = (f'(//div[contains(@class, "ui-trigger-popupInner") and not(contains(@class, "hidden"))]'
               f'{parent_xpath}{loc})[position()={position}]')
        self.click_element(loc)