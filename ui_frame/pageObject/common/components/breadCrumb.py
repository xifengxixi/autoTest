from common.base import Page


class BreadCrumb(Page):
    """
    BreadCrumb面包屑组件
    breadCrumb_click_by_name: 点击面包屑
    breadCrumb_get_path: 获取面包屑路径
    """

    def __get_loc(self, bread_name, parent_xpath=""):
        """
        获取面包屑元素定位
        @param bread_name: 面包屑名称
        @param parent_xpath:
        @return:
        """
        loc = parent_xpath + f"//span[@class='ui-bread-crumb-item']"
        if self.is_element_exist(loc + "/a"):
            # 可点击(a标签)的面包屑
            return loc + f"//a[contains(text(),'{bread_name}')]"
        elif self.is_element_exist(loc + "/i"):
            # 斜体名称
            return loc + f"//i[contains(text(),'{bread_name}')]"
        else:
            # 正常名称或图标
            return loc + f"[contains(text(),'{bread_name}')]"

    def breadCrumb_click_by_name(self, bread_name="", parent_xpath=""):
        """
        点击面包屑
        @param bread_name: 面包屑名称。使用索引位置时，不传该参数
        @param parent_xpath: 父级定位
        @return:
        """
        # 通过面包屑名称点击
        self.click_element(self.__get_loc(bread_name, parent_xpath))

    def breadCrumb_get_path(self, parent_xpath=""):
        """
        获取面包屑路径
        @param parent_xpath: 父级定位
        @return:
        """
        # 获取所有面包屑定位，包含图标、斜体、和链接
        locs = parent_xpath + f"//span[@class='ui-bread-crumb-item']"
        path = []
        eles = self.find_elements(locs)
        for i in range(len(eles)):
            # 先判断是否为图标面包屑
            loc = locs + f"[position()={i+1}]"
            if self.is_element_exist(loc + 'i'):
                path.append(self.get_element_text(loc + 'i'))
            elif self.is_element_exist(loc + "/span"):
                if self.is_element_exist(loc + "/span/following-sibling::span"):
                    path.append(self.get_element_text(loc + "/span/following-sibling::span"))
                else:
                    path.append("图标")
            else:
                path.append(self.get_element_text(loc))
        return path
