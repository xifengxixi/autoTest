from common.base import Page


class RightMenu(Page):
    """
    RightMenu右键菜单
    right_menu_click_option: 点击右键菜单选项
    right_menu_click_sub_menu: 点击右键二级菜单：悬停到一级菜单，点击二级菜单
    """

    def __get_option_loc(self, option_name, parent_xpath=""):
        loc = parent_xpath + f"//div[@class='ui-scroller ui-menu-scroller']//span[contains(text(),'{option_name}')]"
        return loc

    def right_menu_click_option(self, option_name, loc, parent_xpath=""):
        """
        点击右键菜单选项
        @param option_name: 选项名称
        @param loc: 右键位置元素定位
        @param parent_xpath: 父级定位
        @return:
        """
        self.context_click(self.find_element(loc))
        self.sleep(0.5)
        self.click_element(self.__get_option_loc(option_name, parent_xpath))

    def right_menu_click_sub_menu(self, option_name, sub_option_name, loc):
        """
        点击右键二级菜单：悬停到一级菜单，点击二级菜单
        @param option_name: 一级菜单名称
        @param sub_option_name: 二级菜单名称
        @param loc: 右键位置元素定位
        @return:
        """
        # 一级菜单定位
        source_loc = self.__get_option_loc(option_name)
        # 二级菜单定位
        target_loc = f"//div[contains(@title, '{sub_option_name}')]"
        self.context_click(self.find_element(loc))
        self.move_click(source_loc, target_loc)

