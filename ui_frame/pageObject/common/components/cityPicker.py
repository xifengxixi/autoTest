from common.base import Page


class CityPicker(Page):
    """
    CityPicker城市选择器
    select_cityPicker：CityPicker城市选择器选择数据

    """

    def select_cityPicker(self,listData, parent_xpath="", **kwargs):
        '''
        CityPicker城市选择器选择数据
        :param listData:列表形式的数据，如["河南","驻马店","驿城区"]
        '''
        loc = parent_xpath + f"//span[contains(@class,'ui-cascader-picker ui-cascader-picker-show-search ui-city-picker')]"
        element = self.find_element(loc)
        element.click()
        for i in listData:
            i_loc = parent_xpath + f"//li[text()='{i}']"
            self.click_element(i_loc)

