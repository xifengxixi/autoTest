from common.base import Page


class Tag(Page):
    '''
    tag_value_list 获取标签内容[]
    tag_isExist 判断标签是否存在
    tag_click 点击标签按钮
    tag_del 删除单个标签按钮
    tag_isDisable 标签按钮是否是禁用状态
    '''

    def tag_loc(self,parent_xpath='', span_name=None,**kwargs):
        '''
        获取标签路径
        :param parent_xpath: 标签内容
        :param span_name: 父级路径
        :return: 返回路径信息
        '''
        loc = "//*[contains(@class,'ui-tag')]"
        loc = parent_xpath + loc
        if span_name:
            loc=loc+f"//*[text()='{span_name}']"
        return loc

    def tag_ele(self,parent_xpath='', span_name=None,**kwargs):
        '''获取标签路径元素
        :param:parent_xpath 父级路径 可传可不传 （在不传span_name时，返回元素列表eles)
        :param:span_name 标签内容，传递后（或结合父级路径）可定位唯一标签  返回元素ele
        父级路径与标签内容都不传 获取到所有标签路径，返回元素列表eles
        '''
        loc=self.tag_loc(parent_xpath,span_name)
        if span_name:
            return self.find_element(loc)
        return self.find_elements(loc)

    def tag_close_ele(self,parent_xpath='',**kwargs):
        '''获取关闭标签路径元素'''
        loc = f"//div[@class='ui-tag-close']"
        loc = parent_xpath + loc
        return self.find_element(loc)

    def tag_value_list(self, parent_xpath='',**kwargs):
        '''
        获取标签内容
        :param parent_xpath: 父级路径
        :return: 返回可见标签的所有内容
        '''
        eles=self.tag_ele(parent_xpath=parent_xpath)
        value_list=[ele.get_attribute("textContent") for ele in eles]
        return value_list

    def tag_isExist(self,tag_name,parent_xpath='',**kwargs):
        '''判断标签是否存在
        :param tag_name目标标签内容
        return ststus True：存在 False：不存在
        '''
        ststus = False
        value_list=self.tag_value_list(parent_xpath=parent_xpath)
        if tag_name in value_list:
           ststus=True
        return ststus

    def tag_click(self,span_name,parent_xpath='',**kwargs):
        '''
        点击标签按钮
        :param span_name: 标签名称
        :param parent_xpath: 父级路径
        '''
        ele=self.tag_ele(parent_xpath,span_name)
        ele.click()

    def tag_del(self, span_name, parent_xpath='',**kwargs):
        '''
        删除单个标签按钮
        :param span_name: 标签名称
        :param parent_xpath: 父级路径
        '''
        close_ele=self.tag_close_ele(parent_xpath=parent_xpath)
        loc = self.tag_loc(parent_xpath, span_name)
        self.move_on(loc)
        close_ele.click()

    def tag_isDisable(self, span_name, parent_xpath='',**kwargs):
        '''
        标签按钮是否是禁用状态
        :param span_name: 标签名称
        :param parent_xpath: 父级路径
        :return: status True:标签是禁用状态 False:标签是正常状态
        '''
        loc = self.tag_loc(parent_xpath, span_name)
        loc=loc+f'/..'
        ele=self.find_element(loc)
        status=self.check_elem_attribute(ele,"disable")
        return status


