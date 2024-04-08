from common.base import Page


class Scope(Page):
    """
    scope区间框输入组件
    scope_text：区间框输入数据
    scope_text_add：区间框加
    scope_text_reduce：区间框减
    scope_addOrReduce：区间框加减
    """

    def scope_text(self, data, parent_xpath="", **kwargs):
        '''
        区间框输入数据
        :param  data:区间框要输入的数据,单个数字或者是列表
        '''
        loc = parent_xpath + f"//input[contains(@class,'ui-input')]"
        input_eles = self.find_elements(loc)
        if isinstance(data, list):
            data = data
        else:
            data = [data]
        length = len(data) if len(data) < len(input_eles) else len(input_eles)
        for i in range(length):
            self.input_text(input_eles[i], data[i])

    def get_add_elem(self,parent_xpath="", **kwargs):
        """
        获取减号元素
        """
        loc = parent_xpath + '//*[name()="svg" and contains(@class,"ui-icon-xs ui-icon-svg Icon-reduce01")]'
        return self.find_element(loc)

    def get_reduce_elem(self,parent_xpath="", **kwargs):
        """
        获取加号元素
        """
        loc = parent_xpath + '//*[name()="svg" and contains(@class,"ui-icon-xs ui-icon-svg Icon-add-to01")]'
        return self.find_element(loc)

    def scope_text_add(self, parent_xpath="", **kwargs):
        '''
        区间框加
        '''
        loc = parent_xpath + '//*[name()="svg" and contains(@class,"ui-icon-xs ui-icon-svg Icon-add-to01")]'
        self.click_element(loc)

    def scope_text_reduce(self, parent_xpath="", **kwargs):
        '''
        区间框减
        '''
        loc = parent_xpath + '//*[name()="svg" and contains(@class,"ui-icon-xs ui-icon-svg Icon-reduce01")]'
        self.click_element(loc)

    def scope_addOrReduce(self, data, scopeType=True, parent_xpath="", **kwargs):
        '''
        区间框加减
        :param scopeType:加或者减数据，True是加 False是减
        '''
        if scopeType:
            loc = parent_xpath + '//*[name()="svg" and contains(@class,"ui-icon-xs ui-icon-svg Icon-add-to01")]'
        else:
            loc = parent_xpath + '//*[name()="svg" and contains(@class,"ui-icon-xs ui-icon-svg Icon-reduce01")]'
        list(map(lambda x: self.click_element(loc), range(data)))
