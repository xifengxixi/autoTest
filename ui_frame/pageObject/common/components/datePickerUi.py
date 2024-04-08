import re
from common.base import Page


class DatePickerUi(Page):
    """
    DatePicker日期选择器
    __datePicker_loc：拼接日期选择器下的路径
    datePicker_open_date：打开日期选择器
    datePicker_get_value：获取日期选择器组件的值
    datePicker_get_date_title：获取当前选择日期标题
    datePicker_input_date：输入日期（输入日期、月份、年份）
    datePicker_input_date_range：输入日期范围（输入日期范围、月份范围、年份范围）
    datePicker_clear_date：清除日期
    datePicker_click_date_picker_text：点击日期选择器文本（分区）
    datePicker_click_text：点击日期选择器文本
    datePicker_set_days：选择多个/单个天数，选择日期范围
    datePicker_set_dates：选择多个/单个date
    """

    def __datePicker_loc(self, loc, parent_xpath=""):
        """
        拼接日期选择器下的路径
        :param loc:
        :param parent_xpath:
        :return:
        """
        loc = f'//div[@class="ui-trigger-popupInner"]{loc}'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        return ele_loc

    def datePicker_open_date(self, parent_xpath="", picker_type="date-picker", input_index="1"):
        """
        打开日期选择器
        :param parent_xpath:
        :param picker_type:
        :param input_index:
        :return:
        """
        xpaths = [
            '//input',
            f'//span[contains(@class,"ui-{picker_type}-wrap")]',
            '//div'
        ]
        flag = True
        for i in range(len(xpaths)):
            if i == 0:
                ele_loc = f'({parent_xpath}{xpaths[i]})[position()="{input_index}"]'
            else:
                ele_loc = parent_xpath + xpaths[i] if parent_xpath else xpaths[i]
            if self.is_element_exist(ele_loc):
                self.click_element(ele_loc)
                flag = False
                break
        if flag:
            raise Exception("打开日期选择器失败")

    def datePicker_get_value(self, parent_xpath="", picker_type="date-picker"):
        """
        获取日期选择器组件的值
        :param parent_xpath:
        :param picker_type:
        :return:
        """
        value_list = []
        loc1 = '//input'
        loc2 = f'//span[contains(@class, "ui-{picker_type}-wrap")]'
        ele_loc1 = parent_xpath + loc1
        ele_loc2 = parent_xpath + loc2
        if self.is_element_exist(ele_loc1):
            eles = self.find_elements(ele_loc1)
            for ele in eles:
                value_list.append(ele.get_attribute("value"))
        elif self.is_element_exist(ele_loc2):
            ele = self.find_element(ele_loc2)
            value_list.append(ele.text)
        else:
            raise Exception("未找到日期选择器组件的值")
        return value_list


    def datePicker_get_date_title(self, parent_xpath="", picker_type="date-picker"):
        """
        获取当前选择日期标题
        :param parent_xpath:
        :param picker_type:
        :return:
        """
        ele_loc = self.__datePicker_loc(f'//div[@class="ui-{picker_type}-titleDateNav-title"]/*', parent_xpath)
        ele_list = self.get_elements_text(ele_loc)
        ele_list = [x for x in ele_list if x != ""]
        return ele_list

    def datePicker_input_date(self, date_str, parent_xpath=""):
        """
        输入日期（输入日期、月份、年份）
        :param date_str:
            日："2023-03-19"
            月："2023-03"
            年："2023"
        :param parent_xpath:
        :return:
        """
        self.datePicker_open_date(parent_xpath)
        loc = f'//div[contains(@class, "ui-date-picker") and contains(@class, "open")]//input'
        self.input_and_enter(loc, date_str)

    def datePicker_input_date_range(self, start_date, end_date, parent_xpath=""):
        """
        输入日期范围（输入日期范围、月份范围、年份范围）
        :param start_date: 2023-03-19、2023-03、2023
        :param end_date: 2024-04-01、2024-04、2024
        :param parent_xpath:
        :return:
        """
        self.datePicker_open_date(parent_xpath)
        start_loc = self.__datePicker_loc('//div[contains(@class, "item") and position()="1"]//input')
        end_loc = self.__datePicker_loc('//div[contains(@class, "item") and position()="2"]//input')
        self.input_and_enter(start_loc, start_date)
        self.input_and_enter(end_loc, end_date)
        self.datePicker_click_date_picker_text("确定")

    def datePicker_clear_date(self, parent_xpath="", picker_type="date-picker"):
        """
        清除日期
        :param parent_xpath:
        :param picker_type:
        :return:
        """
        loc = f'//*[contains(@class, "ui-{picker_type}")]'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        self.move_on(ele_loc)
        cancel_loc = ele_loc + '//*[name()="svg" and contains(@class, "Icon-cancel")]'
        if self.is_element_exist(cancel_loc):
            self.click_element(cancel_loc)

    def datePicker_click_date_picker_text(self, text, area_type="rangeFooter", parent_xpath="", picker_type="date-picker"):
        """
        点击日期选择器文本（分区）
        :param text:
        :param area_type:
            footer：单个日期选择器，弹窗脚
            multiArea：日期范围选择器，弹窗头
            rangeFooter：日期范围选择器，弹窗脚
        :param parent_xpath:
        :param picker_type:
        :return:
        """
        ele_loc = self.__datePicker_loc(f'//div[contains(@class, "ui-{picker_type}") and contains(@class, "{area_type}")]', parent_xpath)
        if area_type == "rangeFooter":
            ele_loc = ele_loc + "//span"
        elif area_type == "multiArea":
            ele_loc = ele_loc + "//button"
        else:
            ele_loc = ele_loc + "//a"
        options = self.find_elements(ele_loc)
        flag = True
        for option in options:
            if text == option.text:
                option.click()
                flag = False
                break
        if flag:
            raise Exception(f"没有找到需要点击的日期选择器文本：{text}")

    def datePicker_click_text(self, text, parent_xpath=""):
        """
        点击日期选择器文本
        :param text:
        :param parent_xpath:
        :return:
        """
        loc = self.__datePicker_loc(f'//*[text()="{text}"]', parent_xpath)
        self.click_element(loc)

    def datePicker_set_days(self, days_list, parent_xpath="", text="确认", picker_type="date-picker",\
        need_open=True, need_close=True,**kwargs):
        """
        选择多个/单个天数，选择日期范围
        注意：当need_close为True时，text需要传值正确
        :param days_list:
            单个天数格式："2023-03-20"
            多个天数格式：["2023-03-20", "2023-03-21"]
            日期范围格式：["2023-03-20", "2024-03-20"]
        :param parent_xpath:
        :param text: 选择器的文本，例：确认
        :param picker_type: 日期选择器类型
        :param need_open:
        :param need_close:
        :return:
        """
        days_list = days_list if isinstance(days_list, list) else [days_list]
        if need_open:
            self.datePicker_open_date(parent_xpath)
        for day in days_list:
            target_list = str(day).split("-")
            target_year = int(target_list[0])
            target_month = int(target_list[1])
            target_day = int(target_list[2])
            left_left_loc = self.__datePicker_loc('//*[name()="svg" and contains(@class, "Icon-left-arrow03")]')
            right_right_loc = self.__datePicker_loc('//*[name()="svg" and contains(@class, "Icon-Right-arrow03")]')
            left_loc = self.__datePicker_loc('//*[name()="svg" and contains(@class, "Icon-left-arrow01")]')
            right_loc = self.__datePicker_loc('//*[name()="svg" and contains(@class, "Icon-Right-arrow01")]')
            while True:
                title_list = self.datePicker_get_date_title(picker_type=picker_type)
                current_year_min = int(re.findall('\d+|\d+', title_list[0])[0])
                current_month_min = int(re.findall('\d+|\d+', title_list[1])[0])
                current_year_max = current_year_min if len(title_list) == 2 else int(
                    re.findall('\d+|\d+', title_list[2])[0])
                current_month_max = current_month_min if len(title_list) == 2 else int(
                    re.findall('\d+|\d+', title_list[3])[0])
                if target_year < current_year_min:
                    self.click_element(left_left_loc)
                elif target_year > current_year_max:
                    self.click_element(right_right_loc)
                elif target_month < current_month_min:
                    self.click_element(left_loc)
                elif target_month > current_month_max:
                    self.click_element(right_loc)
                else:
                    break
            target_day_loc = self.__datePicker_loc(f'//div[@class="cell"]//*[text()="{target_day}"]')
            if len(title_list) > 2:
                if target_month == current_month_min:
                    target_day_loc = '(' + self.__datePicker_loc(f'//div[@class="cell"]//*[text()="{target_day}"]') + ')[position()="1"]'
                elif target_month == current_month_max:
                    target_day_loc = '(' + self.__datePicker_loc(f'//div[@class="cell"]//*[text()="{target_day}"]') + ')[position()="2"]'
            self.click_element(target_day_loc)
        if need_close:
            self.datePicker_click_text(text)

    def datePicker_set_dates(self, date_list, parent_xpath="", date_type="month", picker_type="date-picker",\
                             text="确认", need_open=True, need_close=True):
        """
        选择多个/单个date
        选择单个（月、季度、半年、年）、选择多个（月、季度、半年、年）、选择范围（月份、年份）
        注意：当need_close为True时，text需要传值正确
        :param date_list:
            单个月份："2023-03"
            单个季度："2023-Q1"
            单个半年："2023-H1"
            单个年份："2023"
            多个月份：["2023-03", "2023-04"]
            多个季度：["2023-Q1", "2023-Q2"]
            多个半年：["2023-H1", "2023-H2"]
            多个年份：["2023", "2024"]
            范围月份：["2023-01", "2025-06"]
            范围年份：["2023", "2026"]
        :param parent_xpath:
        :param date_type:
            month：月份
            season：季度
            halfYear：半年
            year：年份
        :param picker_type:
        :param text: 选择器的文本，例：确认
        :param need_open:
        :param need_close:
        :return:
        """
        month_dict = {
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
            "12": "12 月"
        }
        season_dict = {
            "Q1": "第一季度",
            "Q2": "第二季度",
            "Q3": "第三季度",
            "Q4": "第四季度"
        }
        halfYear_dict = {
            "H1": "上半年",
            "H2": "下半年"
        }
        date_list = date_list if isinstance(date_list, list) else [date_list]
        if need_open:
            self.datePicker_open_date(parent_xpath)
        for date in date_list:
            target_list = str(date).split("-")
            target_year = int(target_list[0])
            target_date = target_list[-1]
            left_left_loc = self.__datePicker_loc('//*[name()="svg" and contains(@class, "Icon-left-arrow03")]')
            right_right_loc = self.__datePicker_loc('//*[name()="svg" and contains(@class, "Icon-Right-arrow03")]')
            while True:
                title_list = self.datePicker_get_date_title(picker_type=picker_type)
                current_year_list = re.findall('\d+|\d+', title_list[0])
                current_year_min = int(current_year_list[0])
                current_year_max = int(current_year_list[-1])
                if target_year < current_year_min:
                    self.click_element(left_left_loc)
                elif target_year > current_year_max:
                    self.click_element(right_right_loc)
                else:
                    break
            target_text = target_date if date_type == "year" else eval(f"{date_type}_dict").get(target_date)
            target_loc = self.__datePicker_loc(f'//div[contains(@class, "content")]//*[text()="{target_text}"]')
            self.click_element(target_loc)
        if need_close:
            self.datePicker_click_text(text)