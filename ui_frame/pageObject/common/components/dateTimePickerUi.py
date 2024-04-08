from common.base import Page
from . import datePickerUi, timePickerUi


class DateTimePickerUi(Page):
    """
    DateTimePicker日期时间选择器
    __dateTimePicker_loc：拼接日期时间选择器下的路径
    dateTimePicker_open：打开日期时间选择器
    dateTimePicker_click_text：点击日期时间选择器文本
    dateTimePicker_input：输入日期和时间点
    dateTimePicker_input_range：输入时间和时间范围
    dateTimePicker_clear：清除日期时间
    dateTimePicker_set：选择日期时间
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.datePickerUi = datePickerUi.DatePickerUi(driver)
        self.timePickerUi = timePickerUi.TimePickerUi(driver)

    def __dateTimePicker_loc(self, loc, parent_xpath=""):
        """
        拼接日期时间选择器下的路径
        :param loc:
        :param parent_xpath:
        :return:
        """
        loc = f'//div[@class="ui-trigger-popupInner"]{loc}'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        return ele_loc
    def dateTimePicker_open(self, parent_xpath="", picker_type="date-time-picker", input_index="1"):
        """
        打开日期时间选择器
        :param parent_xpath:
        :param picker_type:
        :param input_index:
        :return:
        """
        self.datePickerUi.datePicker_open_date(parent_xpath, picker_type, input_index)

    def dateTimePicker_click_text(self, text, parent_xpath=""):
        """
        点击日期时间选择器文本
        :param text:
        :param parent_xpath:
        :return:
        """
        self.datePickerUi.datePicker_click_text(text, parent_xpath)

    def dateTimePicker_input(self, dateTime_str, parent_xpath="", text="确定"):
        """
        输入日期和时间点
        :param dateTime_str:
            "2023-03-20 16:00"
            "2023-03-20 16:00:01"
        :param parent_xpath:
        :param text:
        :return:
        """
        start_str = str(dateTime_str).split(" ")[0]
        end_str = str(dateTime_str).split(" ")[1]
        self.dateTimePicker_open(parent_xpath)
        start_loc = '(' + self.__dateTimePicker_loc('//input)[position()="1"]')
        end_loc = '(' + self.__dateTimePicker_loc('//input)[position()="2"]')
        self.input_and_enter(start_loc, start_str)
        self.input_and_enter(end_loc, end_str)
        self.datePickerUi.datePicker_click_text(text)

    def dateTimePicker_input_range(self, start_str, end_str, parent_xpath="", text="确定"):
        """
        输入时间和时间范围
        :param start_str:
            "2022-02-22 10:10"
            "2022-02-22 10:10:10"
        :param end_str:
            "2023-03-23 10:10"
            "2023-03-23 10:10:10"
        :param parent_xpath:
        :param text:
        :return:
        """
        start_date = str(start_str).split(" ")[0]
        start_time = str(start_str).split(" ")[1]
        end_date = str(end_str).split(" ")[0]
        end_time = str(end_str).split(" ")[1]
        self.dateTimePicker_open(parent_xpath)
        start_date_loc = '(' + self.__dateTimePicker_loc('//input)[position()="1"]')
        end_date_loc = '(' + self.__dateTimePicker_loc('//input)[position()="3"]')
        start_time_loc = '(' + self.__dateTimePicker_loc('//input)[position()="2"]')
        end_time_loc = '(' + self.__dateTimePicker_loc('//input)[position()="4"]')
        self.input_and_enter(start_date_loc, start_date)
        self.input_and_enter(start_time_loc, start_time)
        self.input_and_enter(end_date_loc, end_date)
        self.input_and_enter(end_time_loc, end_time)
        self.datePickerUi.datePicker_click_text(text)

    def dateTimePicker_clear(self, parent_xpath=""):
        """
        清除日期时间
        :param parent_xpath:
        :return:
        """
        self.datePickerUi.datePicker_clear_date(parent_xpath, "date-time-picker")

    def dateTimePicker_set(self, dateTime_list,  parent_xpath="", text="确定"):
        """
        选择日期时间
        :param dateTime_list:
            "2022-02-22 10:11"
            "2022-02-22 10:11:33"
            ["2022-02-22 10:11", "2023-03-23 11:22"]
            ["2022-02-22 10:11:33", "2023-03-23 11:22:44"]
        :param parent_xpath:
        :param text:
        :return:
        """
        dateTime_list = dateTime_list if isinstance(dateTime_list, list) else [dateTime_list]
        new_list = " ".join(dateTime_list).split(" ")
        day_list = new_list[0::2]
        time_list = new_list[1::2]
        self.dateTimePicker_open(parent_xpath)
        self.datePickerUi.datePicker_set_days(day_list, parent_xpath, text, "date-time-picker", False, False)
        time_loc = '//div[contains(@class, "ui-trigger-popupInner") and not(contains(@class, "hidden"))]' \
                   '//div[contains(@class, "ui-time-picker")]'
        if len(time_list) == 1:
            self.timePickerUi.timePicker_set_time_detail(time_list[0], time_loc, True)
        else:
            self.timePickerUi.timePicker_set_time_detail(time_list[0], time_loc, True, "1")
            self.timePickerUi.timePicker_set_time_detail(time_list[1], time_loc, True, "2")
        self.dateTimePicker_click_text(text)
