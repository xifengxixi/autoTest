from common.base import Page
from . import button


class Cascader(Page):
    """
    cascader级联选择器组件
    select_cascader：选择数据
    click_reset_cascader：重置级联选择器数据
    get_values_cascader：get_values_cascader
    clear_cascader：清除级联选择器数据
    select_search_cascader：快捷搜索级联选择器
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.button = button.Button(driver)

    def select_cascader(self, listData, parent_xpath="", **kwargs):
        '''
        选择数据
        :param listData:列表形式的数据，如["河南","驻马店","驿城区"]
        '''
        #展开数据
        loc = parent_xpath + f"//span[contains(@class,'ui-cascader-picker')]"
        self.click_element(loc)
        for i in listData:
            i_loc = parent_xpath + f"//li[text()='{i}']"
            self.click_element(i_loc)

    def click_reset_cascader(self, parent_xpath="", **kwargs):
        '''
        重置级联选择器数据
        '''
        self.button.click_button("重置", parent_loc=parent_xpath)

    def get_values_cascader(self, parent_xpath="", **kwargs):
        '''
        获取级联选择器数据
        '''
        loc = parent_xpath + f"//span[contains(@class,'ui-cascader-picker-label')]"
        ele_loc = self.find_element(loc)
        values = self.get_element_text(ele_loc)
        return values

    def clear_cascader(self, parent_xpath="", **kwargs):
        '''
        清除级联选择器数据
        '''
        loc = parent_xpath + f"//span[contains(@class,'ui-icon ui-icon-wrapper ui-cascader-picker-clear')]"
        self.click_element(loc)

    def select_search_cascader(self,value, parent_xpath="", **kwargs):
        '''
        快捷搜索级联选择器
        '''
        #输入搜索数据
        loc = parent_xpath + f"//input[contains(@class,'ui-input ui-cascader-input')]"
        self.input(loc, value)

