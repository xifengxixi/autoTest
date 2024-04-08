from common.base import Page
from . import icon, checkbox, inputUi


class ListOp(Page):
    """列表操作
    list_get_items_num:获取列表选项数量
    list_drag_by_item:拖拽列表中某项元素（直接拖拽）
    list_drag_by_icon:拖拽列表中某项元素（根据图标拖拽）
    list_check_item:选择/取消选择 一个列表选项
    list_check_items:选择/取消选择 多个列表选项
    list_expand_items:点击加载更多列表选项
    list_click_next_page:列表数据点击下一页
    list_click_previous_page:列表数据点击上一页
    list_click_to_first_page:列表数据点击跳至第一页
    list_click_to_last_page:列表数据点击跳至最后一页
    list_click_item_expand:点击选项展开/关闭
    lict_get_more_options:获取列表某一项的更多操作
    list_is_item_exist:判断列表中是否有指定数据
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.icon = icon.Icon(driver)
        self.checkbox = checkbox.Checkbox(driver)
        self.inputUi = inputUi.InputUi(driver)

    def __get_list_items_loc(self,parent_xpath=""):
        """ 获取全部列表元素的loc """
        return parent_xpath + "//*[contains(@class,'ui-list-item')]"

    def __list_get_item_loc(self,item_name,parent_xpath=""):
        """
        获取列表中某项的loc
        :param item_name: 能够定位到这一项元素的文本信息
        """
        return self.__get_list_items_loc(parent_xpath) + f"//*[text()='{item_name}']"

    def list_get_items_num(self,parent_xpath=""):
        """
        获取列表选项数量
        """
        loc = self.__get_list_items_loc(parent_xpath)
        if self.is_element_exist(loc,wait=2,num=0.5):
            return len(self.find_elements(loc))
        else:
            return 0

    def list_click_item(self,item_name,parent_xpath=""):
        """
        点击列表中某项
        :param item_name:
        """
        loc = self.__list_get_item_loc(item_name,parent_xpath)
        self.click_element(loc)

    def list_drag_by_item(self,item_name,target_name,parent_xpath=""):
        """
        拖拽列表中某项元素（直接拖拽）
        :param item_name:需要拖拽的选项
        :param target_name: 拖拽释放处
        """
        ele = self.find_element(self.__list_get_item_loc(item_name,parent_xpath))
        target = self.find_element(self.__list_get_item_loc(target_name,parent_xpath))
        self.drag_by_pyautogui(ele,target,x_offset=10,y_offset=10)

    def list_drag_by_icon(self,item_name,target_name,parent_xpath=""):
        """
        拖拽列表中某项元素（根据图标拖拽）
        :param item_name:需要拖拽的选项
        :param target_name: 拖拽释放处
        """
        loc = self.__list_get_item_loc(item_name,parent_xpath) + "/.."
        target = self.__list_get_item_loc(target_name, parent_xpath)
        self.icon.icon_drag_move_icon(target,loc)

    def list_check_item(self,item_name,checkbox_type=True,parent_xpath=""):
        """
        选择/取消选择 一个列表选项
        :param item_name: 用于选项的辅助定位
        :param checkbox_type: True为勾选；False为取消勾选
        """
        loc = self.__list_get_item_loc(item_name,parent_xpath) + "/ancestor::div[contains(@class,'ui-list-item-check')]"
        if not self.check_elem_attribute(self.find_element(loc),"ui-list-item-disabled"):
            self.move_on(loc)
            self.checkbox.select_checkbox_button(checkbox_type,parent_xpath=loc)
        else:
            pass

    def list_check_items(self,item_names,checkbox_type=True,parent_xpath=""):
        """
        选择/取消选择 多个列表选项
        :param item_names: 列表选项标题，list或tuple
        :param checkbox_type: True为勾选；False为取消勾选
        """
        for item in item_names:
            self.list_check_item(item,checkbox_type,parent_xpath)

    def list_expand_items(self,parent_xpath=""):
        """
        点击加载更多列表选项
        """
        loc = parent_xpath + "//div[@class='ui-list-footer']"
        self.icon.icon_click_down_arrow(parent_xpath=loc)

    def __list_get_pagination_loc(self,parent_xpath=""):
        """ 获取列表底部页码组件loc """
        return parent_xpath + "//div[contains(@class,'ui-list-pagination')]"

    def list_click_next_page(self,parent_xpath=""):
        """
        列表数据点击下一页
        """
        loc = self.__list_get_pagination_loc(parent_xpath)
        self.icon.click_icon_by_class(icon_class="Icon-Right-arrow01",parent_xpath=loc)

    def list_click_previous_page(self,parent_xpath=""):
        """
        列表数据点击上一页
        """
        loc = self.__list_get_pagination_loc(parent_xpath)
        self.icon.click_icon_by_class(icon_class="Icon-left-arrow01",parent_xpath=loc)

    def list_click_to_first_page(self,parent_xpath=""):
        """
        点击跳至第一页
        """
        loc = self.__list_get_pagination_loc(parent_xpath)
        self.icon.click_icon_by_class(icon_class="Icon-left-arrow05",parent_xpath=loc)

    def list_click_to_last_page(self,parent_xpath=""):
        """
        点击跳至最后一页
        """
        loc = self.__list_get_pagination_loc(parent_xpath)
        self.icon.click_icon_by_class(icon_class="Icon-Right-arrow05",parent_xpath=loc)

    def list_click_to_page(self,page,parent_xpath=""):
        """
        点击跳至指定页面(还需要调试)
        :param page:页数-int
        """
        loc = self.__list_get_pagination_loc(parent_xpath) + "//*[@class='ui-pagination-pager-page']"
        self.click_element(loc)
        self.sleep(1)
        self.inputUi.input_text_ui(page,parent_xpath=loc)
        self.click_element(loc+"//*[text()='前往']")

    def list_click_item_expand(self,item_name,flag=True,parent_xpath=""):
        """
        点击选项展开/关闭
        :param flag: True为展开，False为收起
        """
        loc = self.__list_get_item_loc(item_name, parent_xpath) + "/ancestor::div[contains(@class,'ui-list-item')]//i"
        ele = self.find_element(loc)
        if flag:
            if self.check_elem_attribute(ele,"switcher-off"):
                self.click_element(loc)
        else:
            if self.check_elem_attribute(ele, "switcher-ok"):
                self.click_element(loc)

    def lict_get_more_options(self,item_name,parent_xpath=""):
        """
        获取列表某一项的更多操作
        :param item_name: 用于选项的辅助定位
        """
        loc = self.__list_get_item_loc(item_name,parent_xpath) + "/ancestor::div[contains(@class,'ui-list-item')]"
        self.move_on(loc)
        self.icon.icon_more_option(parent_xpath=loc)

    def list_is_item_exist(self,item_name,is_precise=True,parent_xpath=""):
        """
        判断列表是否有指定选项数据,有则返回True,无则返回False
        :param item_name: 需要判断的选项数据
        :param is_precise: 是否精准校验,默认为True,即需保证输入的名称与列表数据相等才可校验通过;设置False时,只要列表中的数据包含有输入的item_name也可校验通过
        """
        loc = self.__list_get_item_loc(item_name,parent_xpath)
        if not is_precise:
            loc = self.__get_list_items_loc() + f"//*[contains(text(),'{item_name}')]"
        if self.is_element_exist(loc,wait=2,num=0.5):
            return True
        else:
            return False