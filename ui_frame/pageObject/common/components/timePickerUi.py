from common.base import Page


class TimePickerUi(Page):
    """
    TimePicker时间选择器
    timePicker_open：打开时间选择器
    timePicker_click_text：点击时间选择器文本
    timePicker_clear_time：清除时间
    timePicker_input_time：输入时间
    timePicker_input_range_time：输入时间区间
    timePicker_set_time：选择时间点
    timePicker_set_range_time：选择时间区间
    timePicker_set_time_detail：选择时间点（分秒详细）
    timePicker_set_range_time_detail：选择时间区间（分秒详细）
    """

    def timePicker_open(self, parent_xpath="", input_index="1"):
        """
        打开时间选择器
        :param parent_xpath:
        :param input_index:
        :return:
        """
        xpaths = [
            f'//input',
            f'//div'
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
            raise Exception("打开时间选择器失败")

    def timePicker_click_text(self, text, parent_xpath=""):
        """
        点击时间选择器文本
        :param text: 例：确定
        :param parent_xpath:
        :return:
        """
        loc = f'//div[contains(@class, "ui-trigger-popupInner") and not(contains(@class, "hidden"))]//*[text()="{text}"]'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        self.click_element(ele_loc)


    def timePicker_clear_time(self, parent_xpath="", picker_type="time-picker"):
        """
        清除时间
        :param parent_xpath: 时间选择器的parent_xpath
        :param picker_type:
        :return:
        """
        loc = f'//div[contains(@class, "ui-{picker_type}")]'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        self.move_on(ele_loc)
        cancel_loc = ele_loc + '//*[name()="svg" and contains(@class, "Icon-cancel")]'
        if self.is_element_exist(cancel_loc):
            self.click_element(cancel_loc)

    def timePicker_input_time(self, time_str, parent_xpath="", text="确定"):
        """
        输入时间
        :param time_str: 格式为：01:59 或 01:59:59（注意英文冒号）
        :param parent_xpath:
        :param text:
        :return:
        """
        self.timePicker_open(parent_xpath)
        loc = '//div[contains(@class, "ui-time-picker") and contains(@class, "open")]//input'
        self.input_and_enter(loc, time_str)
        confirm_loc = f'//div[contains(@class, "ui-trigger-popupInner") and not(contains(@class, "hidden"))]//*[text()="{text}"]'
        if self.is_element_exist(confirm_loc):
            self.click_element(confirm_loc)

    def timePicker_input_range_time(self, start_str, end_str, parent_xpath="", text="确定"):
        """
        输入时间区间
        :param start_str:
        :param end_str:
        :param parent_xpath:
        :param text:
        :return:
        """
        self.timePicker_open(parent_xpath)
        start_loc = f'(//div[contains(@class, "ui-time-picker") and contains(@class, "open")]//input)[position()="1"]'
        end_loc = f'(//div[contains(@class, "ui-time-picker") and contains(@class, "open")]//input)[position()="2"]'
        self.input_and_enter(start_loc, start_str)
        self.timePicker_open(parent_xpath, input_index="2")
        self.input_and_enter(end_loc, end_str)
        confirm_loc = f'//div[contains(@class, "ui-trigger-popupInner") and not(contains(@class, "hidden"))]//*[text()="{text}"]'
        if self.is_element_exist(confirm_loc):
            self.click_element(confirm_loc)

    def timePicker_set_time(self, time_str, parent_xpath="", need_open=True, need_close=True, text="确定"):
        """
        选择时间点
        :param time_str: 格式为：01:59或01：59：59（注意英文冒号）
        :param parent_xpath:
        :param need_open:
        :param need_close:
        :param text:
        :return:
        """
        if need_open:
            self.timePicker_open(parent_xpath)
        time_list = str(time_str).split(":")
        for i in range(len(time_list)):
            loc = f'(//div[contains(@class, "column")])[position()="{i+1}"]//div[contains(@class, "item")]'
            options = self.find_elements(loc)
            for option in options:
                if option.text == str(time_list[i]):
                    self.scroll_into_view(option)
                    option.click()
                    break
        if need_close:
            self.timePicker_click_text(text)

    def timePicker_set_range_time(self, start_str, end_str, parent_xpath="", need_open=True,\
                                  need_close=True, text="确定"):
        """
        选择时间区间
        :param start_str: 格式为：01:59或01:59:59
        :param end_str: 格式为：02:59或02:59:59
        :param parent_xpath:
        :param need_open:
        :param need_close:
        :param text:
        :return:
        """
        if need_open:
            self.timePicker_open(parent_xpath)
        start_list = str(start_str).split(":")
        end_list = str(end_str).split(":")
        time_list = [start_list, end_list]
        for i in range(len(time_list)):
            for j in range(len(start_list)):
                loc = f'(//div[contains(@class, "ui-trigger-popupInner") and not(contains(@class, "hidden"))]//div[contains(@class, "container")])[position()="{i+1}"]' \
                      f'//div[contains(@class, "column") and position()="{j+1}"]//div[contains(@class, "item")]'
                options = self.find_elements(loc)
                for option in options:
                    if option.text == str(time_list[i][j]):
                        self.scroll_into_view(option)
                        option.click()
                        break
        if need_close:
            self.timePicker_click_text(text)

    def timePicker_set_time_detail(self, time_str, parent_xpath="", need_open=True, input_index="1"):
        """
        选择时间点（分秒详细）
        :param time_str:
        :param parent_xpath:
        :param need_open:
        :param input_index:
        :return:
        """
        if need_open:
            self.timePicker_open(parent_xpath, input_index)
        time_list = str(time_str).split(":")
        # 选择小时
        hour_loc = f'//div[contains(@class, "detailContent")]//*[contains(@class, "item")]'
        hour_options = self.find_elements(hour_loc)
        for hour_option in hour_options:
            if hour_option.text == str(time_list[0]):
                self.scroll_into_view(hour_option)
                hour_option.click()
                break
        # 选择分和秒
        for i in range(1, len(time_list)):
            loc = f'//div[contains(@class, "detailContent")]/div[position()="{i+1}"]//*[contains(@class, "cell")]'
            options = self.find_elements(loc)
            for option in options:
                if option.text == str(time_list[i]):
                    self.scroll_into_view(option)
                    option.click()
                    break

    def timePicker_set_range_time_detail(self, star_str, end_str, parent_xpath=""):
        """
        选择时间区间（分秒详细）
        :param star_str:
        :param end_str:
        :param parent_xpath:
        :return:
        """
        self.timePicker_set_time_detail(star_str, parent_xpath, input_index="1")
        self.timePicker_set_time_detail(end_str, parent_xpath, input_index="2")