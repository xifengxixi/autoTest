from common.base import Page
from . import datePickerUi


class MonthDayPickerUi(Page):
    """
    MonthDayPicker月日选择器
    __monthDayPicker_loc：拼接月日选择器下的路径
    monthDayPicker_open：打开月日选择器
    monthDayPicker_click_text：点击月日选择器文本
    monthDayPicker_set：点选月日选择器
    monthDayPicker_clear：清除月日选择器
    monthDayPicker_get_value：获取月日选择器组件的值
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.datePickerUi = datePickerUi.DatePickerUi(driver)

    def __monthDayPicker_loc(self, loc, parent_xpath=""):
        """
        拼接月日选择器下的路径
        :param loc:
        :param parent_xpath:
        :return:
        """
        loc = f'//div[@class="ui-trigger-popupInner"]{loc}'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        return ele_loc

    def monthDayPicker_open(self, parent_xpath=""):
        """
        打开月日选择器
        :param parent_xpath:
        :return:
        """
        self.datePickerUi.datePicker_open_date(parent_xpath, "month-day-picker")

    def monthDayPicker_click_text(self, text="确定", parent_xpath=""):
        """
        点击月日选择器文本
        :param text:
        :param parent_xpath:
        :return:
        """
        self.datePickerUi.datePicker_click_text(text, parent_xpath)

    def monthDayPicker_set(self, monthDay_str, parent_xpath="", text="确定"):
        """
        点选月日选择器
        :param monthDay_str: 例：03-20(三月二十日)
        :param parent_xpath:
        :param text:
        :return:
        """
        self.monthDayPicker_open(parent_xpath)
        date_list = str(monthDay_str).split("-")
        target_month = int(date_list[0])
        target_day = int(date_list[1])
        xpaths = [
            self.__monthDayPicker_loc(f'//div[contains(@class, "column") and position()="1"]//div[text()="{target_month}月"]'),
            self.__monthDayPicker_loc(f'//div[contains(@class, "column") and position()="2"]//div[text()="{target_day}日"]')
        ]
        for i in range(len(date_list)):
            loc = xpaths[i]
            ele = self.find_and_scroll_to_element(loc)
            ele.click()
        self.monthDayPicker_click_text(text)

    def monthDayPicker_clear(self, parent_xpath=""):
        """
        清除月日选择器
        :param parent_xpath:
        :return:
        """
        self.datePickerUi.datePicker_clear_date(parent_xpath, "month-day-picker")

    def monthDayPicker_get_value(self, parent_xpath=""):
        """
        获取月日选择器组件的值
        :param parent_xpath:
        :return:
        """
        value_list = self.datePickerUi.datePicker_get_value(parent_xpath, "month-day-picker")
        return value_list