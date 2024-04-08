from common.base import Page


class Spin(Page):
    """
    加载操作
    spin_get_text：获取加载提示内容
    spin_wait_disappear：等待加载完成
    """

    def spin_get_text(self,parent_xpath=""):
        """ 获取加载提示内容 """
        loc = parent_xpath + "//div[contains(@class, 'ui-spin-text')]"
        if self.is_element_exist(loc, wait=2):
            return self.get_element_text(loc)

    def spin_wait_disappear(self,time_out=3,parent_xpath=""):
        """
        等待加载完成
        :param time_out: 超时时间（单位：秒）
        """
        loc = parent_xpath + "//div[contains(@class,'loading-bottom-layer')]"
        self.wait_elem_disappear(loc,time_out)


