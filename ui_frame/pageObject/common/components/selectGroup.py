from common.base import Page


class SelectGroup(Page):
    """
    平铺筛选:
    select_group_single:选择一组筛选条件
    unselect_group_single:取消选择一组筛选条件
    get_group_single_status:获取一组筛选条件状态
    check_group_single_status:校验平铺筛选勾选状态
    """

    def get_group_single_ele(self,content,parent_xpath="",**kwargs):
        """
        获取单个筛选条件元素
        :param content: 筛选条件文字
        :param parent_xpath:
        :param kwargs:
        :return:
        """
        loc = parent_xpath + f"//*[contains(@class,'ui-select-group-new-single-content')]//*[text()='{content}']"
        return self.find_element(loc)

    def check_group_single_content_active(self,ele):
        """判断单个筛选条件勾选状态"""
        return self.check_elem_attribute(ele,"ui-select-group-new-single-content-active")

    def select_group_single(self,list_content,parent_xpath="",**kwargs):
        """
        选择一组筛选条件
        :param list_content: 筛选条件文字列表
        :param parent_xpath:
        :param kwargs:
        :return:
        """
        for content in list_content:
            ele = self.get_group_single_ele(content,parent_xpath)
            if not self.check_group_single_content_active(ele):
                self.click_ele(ele)

    def unselect_group_single(self,list_content,parent_xpath="",**kwargs):
        """
        取消选择一组筛选条件
        :param list_content:
        :param parent_xpath:
        :param kwargs:
        :return:
        """
        for content in list_content:
            ele = self.get_group_single_ele(content,parent_xpath)
            if self.check_group_single_content_active(ele):
                self.click_ele(ele)

    def get_group_single_status(self,list_content,parent_xpath="",**kwargs):
        """
        获取一组筛选条件状态
        :param list_content:
        :param parent_xpath:
        :param kwargs:
        :return:字典类型数据,key为筛选条件,value为状态(True or False)
        """
        dict_status = {}
        for content in list_content:
            ele = self.get_group_single_ele(content,parent_xpath)
            dict_status[content] = self.check_group_single_content_active(ele)
        return dict_status

    def check_group_single_status(self,dict_check,parent_xpath="",**kwargs):
        """
        校验平铺筛选勾选状态
        :param dict_check: 校验数据字典,key为筛选条件,value为状态(True or False)
        :param parent_xpath:
        :param kwargs:
        :return:
        """
        dict_data = self.get_group_single_status(dict_check.keys(),parent_xpath)
        result,msg = self.is_data_contain(dict_data,dict_check)
        assert result, f"平铺筛选勾选状态校验失败：{msg}"