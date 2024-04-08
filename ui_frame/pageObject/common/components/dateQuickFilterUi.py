from common.base import Page
from . import datePickerUi


class DateQuickFilterUi(Page):
    """
    DateQuickFilter日期快速筛选
    dateQuickFilter_click_btn：点击按钮（日期快速筛选）
    dateQuickFilter_open：打开日期快速筛选
    dateQuickFilter_set_day：选择日/周/双周
    dateQuickFilter_set_date：选择月/年
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.datePickerUi = datePickerUi.DatePickerUi(driver)

    def dateQuickFilter_click_btn(self, btn_type="left", click_times=1, parent_xpath=""):
        """
        点击按钮（日期快速筛选）
        :param btn_type:
            left：左边的按钮
            right：右边的按钮
        :param click_times: 点击次数
        :param parent_xpath:
        :return:
        """
        loc = f'//button[@class="button-{btn_type}"]'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        for i in range(int(click_times)):
            self.click_element(ele_loc)

    def dateQuickFilter_open(self, parent_xpath=""):
        """
        打开日期快速筛选
        :param parent_xpath:
        :return:
        """
        loc = '//div[@class="dateLabel"]'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        self.click_element(ele_loc)

    def dateQuickFilter_set_day(self, day_str, parent_xpath=""):
        """
        选择日/周/双周
        :param day_str: 例："2023-03-20"
        :param parent_xpath:
        :return:
        """
        self.dateQuickFilter_open(parent_xpath)
        self.datePickerUi.datePicker_set_days(day_str, parent_xpath, picker_type="date-quick-filter",\
                                 need_open=False, need_close=False)

    def dateQuickFilter_set_date(self, date_str, parent_xpath="", date_type="month"):
        """
        选择月/年
        :param date_str:
            月："2023-03"
            年："2023"
        :param parent_xpath:
        :param date_type:
            "month"：月
            "year"：年
        :return:
        """
        self.dateQuickFilter_open(parent_xpath)
        self.datePickerUi.datePicker_set_dates(date_str, parent_xpath, date_type, "date-quick-filter",\
                                  need_open=False, need_close=False)