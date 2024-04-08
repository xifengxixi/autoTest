from common.base import Page


class Switch(Page):
    """
    开关组件:
    get_switch_status:获取开关开启状态
    is_swicth_read_only:开关是否只读
    click_switch_button:点击开关控件
    """

    def get_switch_elem(self,parent_xpath="",**kwargs):
        """
        获取开关元素
        :param parent_xpath:开关父级路径
        """
        button_loc = parent_xpath + "//button[contains(@class,'ui-switch-btn')]"
        return self.find_element(button_loc)

    def get_switch_ele_status(self,ele):
        """
        获取开关元素开启状态
        :param
        """
        return ele.get_attribute("aria-checked")

    def get_switch_status(self,parent_xpath="",**kwargs):
        """
        获取开关开启状态
        :param parent_xpath:开关父级路径
        """
        ele = self.get_switch_elem(parent_xpath)
        return self.get_switch_ele_status(ele)

    def is_swicth_read_only(self,parent_xpath="",**kwargs):
        """
        开关是否只读
        """
        ele = self.get_switch_elem(parent_xpath)
        return self.check_elem_attribute(ele,"ui-switch-btn-readOnly")

    def click_switch_button(self, switch_type=True,parent_xpath="",**kwargs):
        """
        点击开关控件
        :param switch_type: 开启类型,开启:True;关闭:False
        :param parent_xpath:
        :param kwargs:
        :return:
        """
        elem = self.get_switch_elem(parent_xpath)
        status=self.get_switch_ele_status(elem)
        def str_to_bool(str):
            return True if str.lower() == 'true' else False
        if status=="true" or status=="false":
            status=str_to_bool(status)
        elif status=="1" or status=="0":
            status=True if status=="1" else False
        elif status=="":
            status=False
        if status!= switch_type:
            self.click_ele(elem)
