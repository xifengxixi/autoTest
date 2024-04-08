from common.base import Page


class Checkbox(Page):
    """
    checkbox复选框
    select_checkbox_button：选择复选框控件
    select_checkbox：选择复选框控件(没有check框)
    """

    def select_checkbox_button(self, checkbox_type, parent_xpath="", **kwargs):
        '''
        选择复选框控件
        :param checkbox_type:勾选或者不勾选，值True或者False
        '''
        loc = parent_xpath + f"//input[@type='checkbox']"
        loc_ele = self.find_element(loc)
        loc_p = loc + "/.."
        ele_p = self.find_element(loc_p)
        bool = self.check_elem_attribute(ele_p, "checked")
        if checkbox_type != bool:
            loc_ele.click()

    def select_checkbox(self, checkbox_type, parent_xpath="", **kwargs):
        '''
        选择复选框控件(没有check框)
        :param checkbox_type:勾选或者不勾选，值True或者False
        '''
        loc = parent_xpath + f"//label/span"
        ele_p = self.find_element(loc)
        bool = self.check_elem_attribute(ele_p, "unchecked")
        if checkbox_type == bool:
            ele_p.click()

    def select_checkbox_byName(self, nameList, checkbox_type=True, parent_xpath="", **kwargs):
        '''
        通过名称选择复选框控件
        :param name:复选框名称
        :param checkbox_type:勾选或者不勾选，值True或者False
        '''
        if not isinstance(nameList,list):
            nameList=[nameList]
        for name in nameList:
            loc = parent_xpath + f"//span[text()='{name}']"
            loc_ele = self.find_element(loc)
            loc_p = loc + "/ancestor::label"
            if kwargs.get('preceding', False):
                loc_p = loc + "/preceding-sibling::label"
            ele_p = self.find_element(loc_p)
            bool = self.check_elem_attribute(ele_p, "checked")
            if checkbox_type != bool:
                try:
                    loc_ele.click()
                except:
                    self.click_element_disWait(loc_p)
                if kwargs.get('preceding', False):
                    ele_p.click()

    def select_checkbox_noName(self, checkbox_type=True, parent_xpath="", **kwargs):
        '''
        通过位置选择复选框控件
        :param checkbox_type:勾选或者不勾选，值True或者False
        '''
        checkbox_loc = '//input[@class="ui-checkbox-input"]'
        loc = parent_xpath + checkbox_loc
        loc_ele = self.find_element(loc)
        loc_p = loc + "/ancestor::label"
        ele_p = self.find_element(loc_p)
        bool = self.check_elem_attribute(ele_p, "checked")
        if checkbox_type != bool:
            loc_ele.click()

    def check_data_get(self, parent_xpath="", **kwargs):
        '''
        复选框内容获取
        '''
        checkbox_loc = '//input[@class="ui-checkbox-input"]'
        loc = parent_xpath + checkbox_loc
        loc_ele = self.find_element(loc)
        loc_p = loc + "/ancestor::label"
        ele_p = self.find_element(loc_p)
        bool = self.check_elem_attribute(ele_p, "checked")
        return bool

    def select_checkbox_byName_td(self, nameList, checkbox_type=True, parent_xpath="", need_scroll=True, **kwargs):
        """
        表单通过td名称选择复选框控件
        :param name: 复选框对应的td名称
        :param checkbox_type: 勾选或者不勾选，值True或者False
        :param parent_xpath: 父级元素xpath
        :param need_scroll: 是否需要滚动到元素
        :param kwargs:
        """
        nameList = nameList if isinstance(nameList, list) else [nameList]
        for name in nameList:
            loc = f'{parent_xpath}//*[text()="{name}"]/ancestor::tr//input'
            if need_scroll:
                self.find_and_scroll_to_element(loc)
            loc_p = f'{loc}/ancestor::label'
            ele_p = self.find_element(loc_p)
            bool = self.check_elem_attribute(ele_p, "checked")
            if checkbox_type != bool:
                self.click_element(loc)

    def chectBox_isSelected(self,parent_xpath="", **kwargs):
        '''
        复选框是否勾选状态获取
        :param parent_xpath: 父级元素xpath
        :return True:勾选 False:未勾选
        '''
        checkbox_loc = f'{parent_xpath}//input[@class="ui-checkbox-input"]/ancestor::label'
        ele_p = self.find_element(checkbox_loc)
        return self.check_elem_attribute(ele_p, "checked")