from common.base import Page


class CalendarUi(Page):
    """
    Calendar日历
    calendar_click_day_mode：点击日历 日模式 内容
    calendar_get_day_mode_text：获取日历 日模式 文本
    calendar_click_month_mode：点击日历 月模式/双周模式 内容
    calendar_get_month_mode_text：获取日历 月模式/双周模式 文本
    """

    def calendar_click_day_mode(self, time_str, parent_xpath=""):
        """
        点击日历 日模式 内容
        :param time_str:
            "全天"：点击全天对应的内容
            "02:30"：点击02:30对应的内容
        :param parent_xpath:
        :return:
        """
        if time_str == "全天":
            loc = f'//div[@id="calendar-container"]//div[contains(@class, "timeGridDay")]' \
                  f'//tr[contains(@class, "fc-scrollgrid-section-body") and not(contains(@class, "liquid"))]//td[contains(@class, "fc-day-today")]'
        else:
            loc = f'//div[@id="calendar-container"]//div[contains(@class, "timeGridDay")]' \
                  f'//tr[contains(@class, "fc-scrollgrid-section-body") and contains(@class, "liquid")]//td[contains(@data-time, "{time_str}") and position()="2"]'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        self.find_and_scroll_to_element(ele_loc)
        self.click_element(ele_loc)

    def calendar_get_day_mode_text(self, time_str, parent_xpath=""):
        """
        获取日历 日模式 文本
        :param time_str:
            "02:30"：获取02:30对应的文本
        :param parent_xpath:
        :return:
        """
        loc = f'//div[@id="calendar-container"]//div[contains(@class, "timeGridDay")]' \
              f'//tr[contains(@class, "fc-scrollgrid-section-body") and contains(@class, "liquid")]//div[contains(@class, "event-time") and contains(text(), "{time_str}")]' \
              f'/preceding-sibling::div'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        events_list = self.get_elements_text(ele_loc)
        events_list = [x for x in events_list if x != ""]
        return events_list

    def calendar_click_week_mode(self):
        pass

    def calendar_get_week_mode_text(self):
        pass

    def calendar_click_month_mode(self, day_str, parent_xpath=""):
        """
        点击日历 月模式/双周模式 内容
        点击当月内容，非当月内容需先选择到该月再点击
        :param day_str:
            "01"：1号
        :param parent_xpath:
        :return:
        """
        day_str = int(day_str)
        loc = f'//div[@id="calendar-container"]//div[contains(@class, "dayGridMonth")]' \
              f'//td[contains(@class, "fc-daygrid-day") and not(contains(@class, "other"))]//*[@class="fc-daygrid-day-number" and text()="{day_str}"]'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        self.find_and_scroll_to_element(ele_loc)
        self.click_element(ele_loc)

    def calendar_get_month_mode_text(self, day_str, parent_xpath=""):
        """
        获取日历 月模式/双周模式 文本
        获取当月内容，非当月内容需先选择到该月再获取
        :param day_str:
            "01"：1号
        :param parent_xpath:
        :return:
        """
        day_str = int(day_str)
        loc = f'//div[@id="calendar-container"]//div[contains(@class, "dayGridMonth")]' \
              f'//td[contains(@class, "fc-daygrid-day") and not(contains(@class, "other"))]//*[@class="fc-daygrid-day-number" and text()="{day_str}"]' \
              f'/../following-sibling::div//div[contains(@class,"fc-daygrid-event-harness") and not(contains(@style, "hidden"))]//div[contains(@class,"fc-event-title")]'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        events_list = self.get_elements_text(ele_loc)
        events_list = [x for x in events_list if x != ""]
        return events_list