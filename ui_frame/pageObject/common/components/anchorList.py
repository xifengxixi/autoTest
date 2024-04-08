from common.base import Page


class AnchorList(Page):
    """
    AnchorList锚点列表组件
    anchorList_click_by_name: 通过锚点名称或锚点索引点击锚点
    anchorList_search_by_name： 搜索锚点
    anchorList_clear_input_value： 清除锚点搜索框内容
    """

    def __get_anchorList_loc(self, anchor_name, parent_xpath=""):
        loc = parent_xpath + f"//span[contains(@class,'ui-anchor-list-link-title')][contains(text(),'{anchor_name}')]"
        return loc

    def anchorList_click_by_name(self, anchor_name, parent_xpath=""):
        """
        通过锚点名称或锚点索引点击锚点
        @param anchor_name: 锚点名称
        @param parent_xpath:
        @return:
        """
        # 通过锚点名称点击
        self.click_element(self.__get_anchorList_loc(anchor_name, parent_xpath))

    def anchorList_search_by_name(self, search_value, parent_xpath=""):
        """
        搜索锚点
        @param search_value: 搜索值
        @param parent_xpath:
        @return:
        """
        loc = parent_xpath + "//div[@class='ui-anchor-list-header']//input[contains(@class, 'ui-input')]"
        self.input(loc, search_value)

    def anchorList_clear_input_value(self, parent_xpath=""):
        """
        清除锚点搜索框内容
        @param parent_xpath:
        @return:
        """
        # 搜索框 x 按钮
        loc = parent_xpath + "//span[@class='ui-input-clear']"
        if self.is_element_exist(loc):
            # 输入框有值时，通过 x 按钮清除
            self.click_element(loc)
        else:
            # 通过输入空字符进行清除
            self.anchorList_search_by_name("", parent_xpath)
