from common.base import Page


class Menu(Page):
    """
    菜单操作
    menu_click_menu_item:点击菜单分页
    menu_get_item_name:获取菜单名称（含自定义附加项），例如根据"未处理"获取"未处理(11)"
    menu_get_more_items:hover菜单展开更多
    menu_click_manager_menu_item:后台管理中心——左侧，根据名称点击服务
    menu_click_select_item:下拉菜单点击选项
    menu_click_subMenu_item:多级菜单选项点击
    menu_click_element:页面隐藏三个点下拉框元素点击
    """

    def __menu_get_menu_item_loc(self,menu_name,parent_xpath="",fuzzy=False):
        """ 根据菜单名获取菜单选项 """
        loc = f"//*[contains(@class,'ui-menu-list-item')]//*[text()='{menu_name}']"
        if fuzzy:
            loc = f"//*[contains(@class,'ui-menu-list-item')]//*[contains(text(),'{menu_name}')]"
        return parent_xpath + loc

    def menu_click_menu_item(self,menu_name,parent_xpath="",fuzzy=False):
        """
        点击菜单分页：例如左侧菜单、选择人员菜单分页等
        备注：
        """
        loc = self.__menu_get_menu_item_loc(menu_name, parent_xpath, fuzzy=fuzzy)
        self.click_element(loc)

    def menu_get_item_name(self,menu_name,parent_xpath=""):
        """
        获取菜单名称（含自定义附加项），例如根据"未处理"获取"未处理(11)"
        :param menu_name: 菜单名
        """
        return self.get_element_text(parent_xpath + f"//span[contains(text(),'{menu_name}')]")
    def menu_get_more_items(self,parent_xpath=""):
        """
        hover菜单展开更多
        """
        loc = parent_xpath + "//*[@class='ui-menu-overflow-more']//*[text()='更多']"
        self.move_on(loc)

    def menu_click_manager_menu_item(self,menu_name):
        """
        后台管理中心——左侧，根据名称点击服务
        """
        loc = f"//*[@class='weapp-manager-nav-menus-list-item ']//*[text()='{menu_name}']"
        self.click_element(loc)

    def menu_click_select_item(self,selected_name,menu_name,parent_xpath=""):
        """
        下拉菜单点击选项
        :param selected_name:下拉菜单已选择的选项
        :param menu_name: 下拉菜单需要点击的选项
        """
        loc = parent_xpath + f"//div[contains(@class,'ui-menu-select')]//*[text()='{selected_name}']"
        target = parent_xpath + f"//div[contains(@class,'ui-menu-select-cover-content') or contains(@class,'ui-menu-select-trigger')]//*[text()='{menu_name}']"
        self.move_click(loc,target)

    def menu_click_subMenu_item(self,menu_name,parent_xpath=""):
        """
        多级菜单选项点击(从一级菜单开始,至少输入2项),输入一项请移步 menu_click_menu_item()或输入“流程统计-”
        :param menu_name: 多级菜单选项,格式要求如:流程统计-流程量分析-流程量分析 1.至少输入2项（输入一项时输入”菜单1-“） 2.以-分割 3.从一级菜单开始输入
        """
        lst = menu_name.split("-")
        pre_loc = "/ancestor::*[contains(@class,'ui-menu-list-item')]"
        ## 一级菜单确认关闭
        first_item_loc = self.__menu_get_menu_item_loc(lst[0],parent_xpath) + pre_loc +"//*[contains(@class,'level-0')]/../following-sibling::span//*[contains(@class,'Icon-Right-arrow')]"
        if self.is_element_exist(first_item_loc):
            self.click_element(first_item_loc)
        ## 点击菜单1-菜单2-菜单3...
        for i in range(len(lst)):
            i_loc = self.__menu_get_menu_item_loc(lst[i],parent_xpath) + pre_loc +f"//*[contains(@class,'level-{i}')]"
            if self.is_element_exist(i_loc):
                if i != len(lst)-1:
                    next_i_loc = self.__menu_get_menu_item_loc(lst[i+1],parent_xpath) + pre_loc +f"//*[contains(@class,'level-{i}+1')]"
                    if not self.is_element_exist(next_i_loc):
                        self.click_element(i_loc)
                else :
                    self.click_element(i_loc)

    def menu_list_more(self,*menus,parent_xpath=""):
        # 移动到更多上
        loc = parent_xpath + "//*[contains(@class,'Icon-more')]"
        self.move_on(loc)
        # 移动点击菜单
        for menu in menus:
            menu_loc = f"//*[contains(@class,'ui-menu-list-item') and text()='{menu}']"
            self.move_click(menu_loc,menu_loc)
            self.sleep(.5)

    def menu_list_get_item_name(self, parent_xpath=""):
        """
        获取列表菜单名称
        :param
        """
        loc = parent_xpath + "//*[contains(@class,'ui-menu-list-item')]//*[text()]"
        eles = self.find_elements(loc)
        menu_list = []
        for ele in eles:
            menu_list.append(ele.text)
        return menu_list

    def menu_click_cover_item(self,menu_name,parent_xpath=""):
        """
        悬浮卡片菜单点击
        :param menu_name: 下拉菜单需要点击的选项
        """
        pre_loc = parent_xpath + "//*[contains(@class,'ui-menu-select-cover-container') and contains(@class,'ui-menu-select-cover-container-active')]"
        loc = pre_loc + f"//*[text()='{menu_name}']"
        self.click_element(loc)
