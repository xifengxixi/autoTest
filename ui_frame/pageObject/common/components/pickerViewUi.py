from common.base import Page


class PickerViewUi(Page):
    """
    PickerView选择器
    pickerView_set：点选快速选择器
    """

    def pickerView_set(self, time_str, parent_xpath=""):
        """
        点选快速选择器
        :param time_str: 例：02:34(2时34分)
        :param parent_xpath:
        :return:
        """
        time_list = str(time_str).split(":")
        target_hour = int(time_list[0])
        target_minute = int(time_list[1])
        xpaths = [
            f'//div[@class="ui-picker-view-column" and position()="1"]//div[text()="{target_hour}时"]',
            f'//div[@class="ui-picker-view-column" and position()="2"]//div[text()="{target_minute}分"]'
        ]
        for i in range(len(time_list)):
            loc = parent_xpath + xpaths[i] if parent_xpath else xpaths[i]
            ele = self.find_and_scroll_to_element(loc)
            ele.click()