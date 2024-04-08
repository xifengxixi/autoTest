from common.base import Page


class Trigger(Page):
    """
    Trigger触发器
    trigger_click_btn：点击触发器下的按钮
    trigger_get_content：获取触发器内容
    trigger_click：点击触发器文本
    """

    def trigger_click_btn(self, btn_name, click_times=1, index=1, parent_xpath=""):
        """
        点击触发器下的按钮
        :param btn_name: 按钮名称
        :param click_times: 点击次数
        :param index: 触发器层级，默认为一级触发器
        :param parent_xpath:
        :return:
        """
        loc = f'(//div[contains(@class, "ui-trigger-popupInner") and not(contains(@class, "hidden"))])[position()="{index}"]' \
              f'//button[text()="{btn_name}"]'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        for i in range(int(click_times)):
            self.click_element(ele_loc)

    def trigger_get_content(self, index=1, parent_xpath=""):
        """
        获取触发器内容，支持获取多级触发器内容
        :param index: 触发器层级，默认为一级触发器
        :param parent_xpath:
        :return:
        """
        loc = f'(//div[contains(@class, "ui-trigger-popupInner") and not(contains(@class, "hidden"))])[position()="{index}"]' \
              f'//div[contains(@class, "content")]/div'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        content_list = self.get_elements_text(ele_loc)
        return content_list

    def trigger_click(self, text, index=1, parent_xpath=""):
        """
        点击触发器文本
        :param text: 触发器内容
        :param index: 触发器层级，默认为一级触发器
        :param parent_xpath:
        :return:
        """
        loc = f'(//div[contains(@class, "ui-trigger-popupInner") and not(contains(@class, "hidden"))])[position()="{index}"]' \
              f'//*[text()="{text}"]'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        self.click_element(ele_loc)