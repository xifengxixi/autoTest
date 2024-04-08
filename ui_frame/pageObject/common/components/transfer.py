from common.base import Page


class Transfer(Page):
    """
    Transfer穿梭框组件
    transfer_selected_by_name: 通过名称勾选\取消勾选
    transfer_selected_all: 全选\取消全选
    transfer_search_by_name: 搜索穿梭框内容
    transfer_clear_input_value: 清除穿梭框搜索内容
    transfer_is_selected: 是否被勾选
    """

    def __get_transfer_loc(self, transfer_name, parent_xpath=""):
        loc = parent_xpath + f"//div[contains(@class, 'ui-transfer-list-wrap-left')]//div[text()='{transfer_name}']/following-sibling::label"
        if transfer_name == "全选":
            return parent_xpath + "//label[contains(@class, 'ui-transfer-check-all-checkbox')]"
        return loc

    def transfer_is_selected(self, loc):
        """
        是否被勾选
        @param loc:
        @return:
        """
        return True if "checked" in self.get_element_attribute(loc, "class") else False

    def transfer_selected_by_name(self, transfer_name, parent_xpath="", is_check=True):
        """
        穿梭框-通过名称勾选\取消勾选
        @param transfer_name: 选项名称
        @param is_check: 是否勾选，True/False
        @param parent_xpath:
        @return:
        """
        loc = self.__get_transfer_loc(transfer_name, parent_xpath)
        if is_check and not self.transfer_is_selected(loc):
            self.click_element(loc)
        elif not is_check and self.transfer_is_selected(loc):
            self.click_element(loc)

    def transfer_selected_all(self, parent_xpath="", is_check_all=True):
        """
        穿梭框-全选\取消全选
        @param parent_xpath:
        @param is_check_all: 是否全选，True/False
        @return:
        """
        loc = self.__get_transfer_loc("全选", parent_xpath)
        if is_check_all and not self.transfer_is_selected(loc):
            self.click_element(loc)
        elif not is_check_all and self.transfer_is_selected(loc):
            self.click_element(loc)

    def transfer_search_by_name(self, search_value, parent_xpath=""):
        """
        搜索穿梭框内容
        @param search_value: 搜索内容
        @param parent_xpath:
        @return:
        """
        loc = parent_xpath + "//div[contains(@class, 'ui-transfer-list-wrap-left')]//input[contains(@class, 'ui-input')]"
        self.input(loc, search_value)

    def transfer_clear_input_value(self, parent_xpath=""):
        """
        清除穿梭框搜索内容
        @param parent_xpath:
        @return:
        """
        # 搜索框 x 按钮
        loc = parent_xpath + "//div[contains(@class, 'ui-transfer-list-wrap-left')]//span[@class='ui-input-clear']"
        if self.is_element_exist(loc):
            # 输入框有值时，通过 x 按钮清除
            self.click_element(loc)
        else:
            # 通过输入空字符进行清除
            self.transfer_search_by_name("", parent_xpath)
