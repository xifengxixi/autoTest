from common.base import Page


class Collapse(Page):
    '''
    collapse_status  判断折叠按钮的折叠状态
    collapse_click 点击折叠按钮
    collapse_open  打开折叠按钮
    collapse_close 折叠折叠按钮
    '''

    def collapse_loc(self,span_name,parent_xpath='',**kwargs):
        '''
        获取折叠路径
        :param span_name: 折叠按钮所在行span名称
        :param parent_xpath: 父级路径
        :return:
        '''
        loc = f"//div[text()='{span_name}']"
        loc = parent_xpath + loc
        return loc

    def collapse_ele(self,span_name,parent_xpath='',isState=False,**kwargs):
        '''获取折叠路径元素'''
        loc=self.collapse_loc(span_name,parent_xpath=parent_xpath)
        new_loc = loc+f'/..' if isState else loc
        return self.find_element(new_loc)

    def collapse_status(self, span_name,parent_xpath='',**kwargs):
        '''
        判断折叠按钮的折叠状态
        :param span_name: lable名称
        :param parent_xpath: 父级路径
        :return: status True：展开状态  False：关闭状态
        '''
        status=False
        ele = self.collapse_ele(span_name, parent_xpath=parent_xpath,isState=True)
        attribute_value=ele.get_attribute("class")
        if "inactive" in attribute_value:
            status=True
        return status

    def collapse_click(self, span_name,parent_xpath='',ele=None,**kwargs):
        '''
        点击折叠按钮
        :param span_name: 折叠按钮所在行span名称
        :param parent_xpath:父级路径
        :param ele: 折叠按钮元素
        '''
        if not ele:
            ele=self.collapse_ele(span_name,parent_xpath)
        ele.click()

    def collapse_open(self, span_name, parent_xpath='',**kwargs):
        '''
        打开折叠按钮
        :param span_name: 折叠按钮所在行span名称
        :param parent_xpath: 父级路径
        '''
        status=self.collapse_status(span_name, parent_xpath)
        if not status:#不是展开状态时打开
            self.collapse_click(span_name, parent_xpath)

    def collapse_close(self, span_name, parent_xpath='',**kwargs):
        '''折叠折叠按钮
        :param span_name: 折叠按钮所在行span名称
        :param parent_xpath: 父级路径
        '''
        status=self.collapse_status(span_name, parent_xpath)
        if status:#是展开状态时关闭
            self.collapse_click(span_name, parent_xpath)
