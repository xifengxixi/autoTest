from common.base import Page


class Tree(Page):
    """
    Tree树组件
    tree_is_open: tree节点是否展开
    tree_is_checked: tree节点是否被勾选
    tree_open_by_loc: 展开或收起tree节点
    tree_checked_by_loc: 勾选、取消勾选tree节点
    tree_open_by_node_name_list: 根据tree节点名称列表层级展开，或收起最后一个节点
    tree_check_by_node_name_list: 根据tree节点名称列表，勾选、取消勾选节点
    """
    def tree_is_open(self, loc):
        """
        tree节点是否展开
        @param loc:
        @return:
        """
        return False if "off" in self.get_element_attribute(loc, "class") else True

    def tree_is_checked(self, loc):
        """
        tree节点是否被勾选
        @param loc:
        @return:
        """
        # return self.find_element(loc).is_selected()  # 返回状态一直为False
        return True if "checked" in self.get_element_attribute(loc, "class") else False

    def tree_open_by_loc(self, loc, is_open=True):
        """
        展开或收起tree节点
        @param loc: 完整元素定位
        @param is_open: True 展开，False 收起
        @return:
        """
        if is_open and not self.tree_is_open(loc):
            # 展开
            # self.click_element(loc)
            self.click_by_js(self.find_element(loc))
        elif not is_open and self.tree_is_open(loc):
            # 收起
            # self.click_element(loc)
            self.click_by_js(self.find_element(loc))

    def tree_checked_by_loc(self, loc, is_check=True):
        """
        勾选、取消勾选tree节点
        @param loc: 完整元素定位
        @param is_check:
        @return:
        """
        if is_check and not self.tree_is_checked(loc):
            self.click_element(loc)
        elif not is_check and self.tree_is_checked(loc):
            self.click_element(loc)

    def tree_open_by_node_name_list(self, tree_name_list: list, parent_xpath="", is_open=True):
        """
        根据tree节点名称列表层级展开，或收起最后一个节点
        @param tree_name_list: 节点名称列表，从根节点开始传入节点名称，
        @param parent_xpath:
        @param is_open: True：展开，False：收起
        @return:
        """
        if not isinstance(tree_name_list, list) or not tree_name_list:
            raise Exception("请传入tree节点列表")
        # root_loc = parent_xpath + "//ul[@class='ui-tree']"
        root_loc = parent_xpath + "//ul[contains(@class,'ui-tree')]"
        for index, node_name in enumerate(tree_name_list):
            # 根据节点名称组装节点loc
            span_loc = root_loc + f"/li/div//span[text()='{node_name}']"
            if index > 0:
                span_loc = root_loc + f"//ul[@class='ui-tree-child']//li/div//span[text()='{node_name}']"
                root_loc = root_loc + f"//ul[@class='ui-tree-child']//li/div[2]"
            # 判断节点是否存在
            if self.is_element_exist(span_loc, wait=15):
                # 展开或收起节点
                if is_open:
                    # 展开
                    self.tree_open_by_loc(span_loc + "/../..", True)
                else:
                    if not self.tree_is_open(span_loc):
                        # 元素已被收起，且需要收起，不需要再循环判断下级节点
                        break
                    if index == len(tree_name_list):
                        self.tree_open_by_loc(span_loc + "/../..", False)
            else:
                raise Exception(f"节点名称元素定位不存在：{span_loc}")

    def tree_check_by_node_name_list(self, tree_name_list: list, parent_xpath="", is_check=True):
        """
        根据tree节点名称列表，勾选、取消勾选节点
        @param tree_name_list:
        @param parent_xpath:
        @param is_check:
        @return:
        """
        if not isinstance(tree_name_list, list):
            raise Exception("请传入tree节点列表")
        # 根据节点列表，展开tree
        self.tree_open_by_node_name_list(tree_name_list[:-1], parent_xpath, True)
        # 是否勾选最后一个节点
        # root_loc = parent_xpath + "//ul[@class='ui-tree']"
        root_loc = parent_xpath + "//ul[contains(@class,'ui-tree')]"
        last_loc = None
        # 组装最后一个节点的定位
        for index, node_name in enumerate(tree_name_list):
            # 根据节点名称组装节点loc
            span_loc = root_loc + f"/li/div//span[text()='{node_name}']"
            input_loc = span_loc + "/..//input"
            if index > 0:
                span_loc = root_loc + f"//ul[@class='ui-tree-child']//li/div//span[text()='{node_name}']"
                root_loc = root_loc + f"//ul[@class='ui-tree-child']//li/div[2]"
                input_loc = span_loc + "/..//input"
            last_loc = input_loc + "/.."
        self.tree_checked_by_loc(last_loc, is_check)

    def tree_click_by_node_name_list(self, tree_name_list: list, parent_xpath=""):
        """
        根据tree节点名称列表层级展开，或收起最后一个节点
        @param tree_name_list: 节点名称列表，从根节点开始传入节点名称，
        @param parent_xpath:
        @return:
        """
        if not isinstance(tree_name_list, list) or not tree_name_list:
            raise Exception("请传入tree节点列表")
        root_loc = parent_xpath + "//*[contains(@class,'ui-tree')]"
        for index, node_name in enumerate(tree_name_list):
            # 根据节点名称组装节点loc
            span_loc = root_loc + f"/li/div//span[text()='{node_name}']"
            if index > 0:
                span_loc = root_loc + f"//ul[@class='ui-tree-child']//li/div//span[text()='{node_name}']"
                root_loc = root_loc + f"//ul[@class='ui-tree-child']//li/div[2]"
            self.click_element(span_loc)
            self.sleep(.5)

    def tree_node_name_exist(self, node_name, parent_xpath=""):
        """
        节点名称是否存在
        """
        node_loc = parent_xpath + f"//*[contains(@class,'ui-tree')]//li/div//span[text()='{node_name}']"
        return self.is_element_exist(node_loc)