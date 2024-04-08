from common.base import Page


class Radio(Page):
    """
    radio单选控件
    select_radio_button：radio单选控件选择数
    radio_button_byName：radio控件通过名称选择数据
    radio_click_byName：radio控件通过名称点击
    """

    def select_radio_button(self, radio_type, parent_xpath="", **kwargs):
        '''
        radio单选控件选择数据
        :param radio_type:选择或者不选择，值True或者False
        '''
        loc = parent_xpath + f"//input[@type='radio']/.."
        loc_ele = self.find_element(loc)
        # 是否勾选radio单选控件
        bl = self.check_elem_attribute(loc_ele, "checked")
        if radio_type != bl:
            loc_ele.click()

    def radio_button_byName(self, name, radio_type, parent_xpath="", **kwargs):
        '''
        radio控件通过名称选择数据
        :param name:radio框的名称
        :param radio_type:选择或者不选择，值True或者False
        '''
        loc = parent_xpath + f"//span[text()='{name}']|//div[text()='{name}']"
        loc_ele = self.find_element(loc)
        # 是否勾选radio单选控件
        bl = self.check_elem_attribute(loc_ele, "checked")
        if radio_type != bl:
            loc_ele.click()

    def radio_click_byName(self, name, radio_type=True, parent_xpath='',**kwargs):
        """
        radio控件通过名称点击
        :param name:
        :param radio_type:
        :param parent_xpath:
        :return:
        """
        loc = f'//*[contains(@class,"radio-group")]//*[@title="{name}"]'
        loc = parent_xpath + loc if parent_xpath else loc
        loc_ele = self.find_element(loc)
        bl = self.check_elem_attribute(loc_ele, "checked")
        if radio_type != bl:
            self.click_element(loc)

    def radio_getCheck(self, parent_xpath):
        '''
        radio控件获取当前选中的数据
        '''
        loc = parent_xpath + "//*[contains(@class, 'ui-radio-label-span-checked')]"
        value=self.get_element_attribute(loc,"textContent")
        return value
