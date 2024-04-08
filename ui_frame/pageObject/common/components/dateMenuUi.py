from common.base import Page
from . import datePickerUi


class DateMenu(Page):
    """
    DateMenu日期菜单
    dateMenu_open：打开日期菜单
    dateMenu_click_scroller_btn：点击日期菜单滚动条按钮
    dateMenu_set：设置日期菜单
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.datePickerUi = datePickerUi.DatePickerUi(driver)

    def dateMenu_open(self, parent_xpath=""):
        """
        打开日期菜单
        :param parent_xpath:
        :return:
        """
        self.datePickerUi.datePicker_open_date(parent_xpath)

    def dateMenu_click_scroller_btn(self, btn_name, parent_xpath=""):
        """
        点击日期菜单滚动条按钮
        :param btn_name:
        :param parent_xpath:
        :return:
        """
        loc = f'//div[contains(@class, "scroller")]//button[text()="{btn_name}"]'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        self.find_and_scroll_to_element(ele_loc)
        self.click_element(ele_loc)

    def dateMenu_set(self, time_str, parent_xpath=""):
        """
        设置日期菜单
        :param time_str:
            2023-01：2023年1 月
            2023-Q1：2023年第1季度
            2023-H1：2023年上半年
            2023：2023年全年
        :param parent_xpath:
        :return:
        """
        time_dict = {
            "01": "1 月",
            "02": "2 月",
            "03": "3 月",
            "04": "4 月",
            "05": "5 月",
            "06": "6 月",
            "07": "7 月",
            "08": "8 月",
            "09": "9 月",
            "10": "10 月",
            "11": "11 月",
            "12": "12 月",
            "Q1": "第1季度",
            "Q2": "第2季度",
            "Q3": "第3季度",
            "Q4": "第4季度",
            "H1": "上半年",
            "H2": "下半年"
        }
        target_list = str(time_str).split("-")
        target_year = target_list[0]
        target_date = target_list[1] if len(target_list) > 1 else ""
        target_btn_name = time_dict.get(target_date) if target_date else "全年"
        # 打开日期菜单
        self.dateMenu_open(parent_xpath)
        # 选择年份
        self.datePickerUi.datePicker_set_dates(target_year, parent_xpath, "year", need_open=False, need_close=False)
        # 选择滚动条日期
        self.dateMenu_click_scroller_btn(target_btn_name, parent_xpath)
