from common.base import Page


class Empty(Page):
    '''
    empty_title_isExist 判断空状态时标题是否存在
    empty_description_isExist 判断获取空状态时描述元素是否存在
    '''

    def empty_title_loc(self,parent_xpath='',**kwargs):
        '''获取空状态标题路径'''
        loc = f"//div[contains(@class,'ui-empty-title')]"
        loc = parent_xpath + loc
        return loc

    def empty_description_loc(self,parent_xpath='',**kwargs):
        '''获取空状态描述路径'''
        loc = f"//div[contains(@class,'ui-empty-description')]"
        loc = parent_xpath + loc
        return loc

    def empty_title_ele(self,parent_xpath='',**kwargs):
        '''获取空状态标题元素'''
        loc=self.empty_title_loc(parent_xpath)
        return self.find_element(loc)

    def empty_description_ele(self,parent_xpath='',**kwargs):
        '''获取空状态描述元素'''
        loc=self.empty_description_loc(parent_xpath)
        return self.find_element(loc)

    def empty_title_isExist(self, empty_title,parent_xpath='',**kwargs):
        '''
        判断空状态时标题是否存在
        :param empty_title: 页面空状态时，文字标题
        :param parent_xpath: 父级路径
        :return: 空状态标题是否存在 True 描述存在 False 描述不存在
        '''
        ele = self.empty_title_ele(parent_xpath)
        status = self.check_elem_attribute(ele,empty_title, attribute_name="textContent")
        return status

    def empty_description_isExist(self,empty_description, parent_xpath='',**kwargs):
        '''
        判断获取空状态时描述元素是否存在
        :param empty_description: 页面空状态时，文字描述
        :param parent_xpath: 父级路径
        :return: 空状态描述是否存在 True 描述存在 False 描述不存在
        '''
        ele = self.empty_description_ele(parent_xpath)
        status = self.check_elem_attribute(ele,empty_description, attribute_name="textContent")
        return status




