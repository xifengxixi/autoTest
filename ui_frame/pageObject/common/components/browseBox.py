from common.base import Page
from . import menu, icon, checkbox, selectUi, inputUi


class BrowseBox(Page):
    """
    浏览框,组合浏览框
    browser_btn_up:展开浏览框收起内容
    get_browser_selected_item:获取浏览框已选择内容
    delete_browser_selected_item:删除浏览框已选内容
    browser_search_select:浏览框输入查询后选择
    move_and_browser_search_select:移到浏览框搜索按钮上加载浏览框再查询选择下拉框内容
    is_browser_item_read_only:浏览框选项是否只读
    browser_multiple_select:浏览框多选
    browser_single_select:浏览框单选
    choose_user_single:选择人员-单选
    choose_user_multiple:选择人员-多选
    choose_depart_single:选择部门-单选
    choose_depart_multiple:选择部门-多选
    choose_position_single:选择岗位-单选
    choose_position_multiple选择岗位-多选
    choose_subcompany_single:选择分部-单选
    choose_subcompany_multiple:选择分部-多选
    browser_single_select_by_type:浏览框根据类型进行单选
    browser_multiple_select_by_type:浏览框根据类型进行多选
    browser_types_single_select:组合浏览框-单选
    browser_types_multiple_select:组合浏览框-多选
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.menu = menu.Menu(driver)
        self.icon = icon.Icon(driver)
        self.checkbox = checkbox.Checkbox(driver)
        self.selectUi = selectUi.SelectUi(driver)
        self.inputUi = inputUi.InputUi(driver)

    browser_confirm_sure = "//*[@id='multSure']"

    def browser_btn_up(self,parent_xpath="",**kwargs):
        """
        展开浏览框收起内容
        :param parent_xpath:
        """
        btn_icon = "//div[contains(@class,'Icon-up-arrow03')]"
        btn_xpath = parent_xpath+ "//*[@class='ui-browser-associative-selected-btn']" + btn_icon
        if self.is_element_exist(btn_xpath):
            self.click_element(btn_xpath)

    def get_browser_selected_item(self,parent_xpath="",**kwargs):
        """
        获取浏览框已选择内容
        :param parent_xpath:
        """
        item_loc = parent_xpath + "//*[contains(@class,'ui-list-item-row')]"
        return self.get_elements_text(item_loc)

    def delete_browser_selected_item(self,list_item,parent_xpath="",**kwargs):
        """
        删除浏览框已选内容
        :param list_item:删除的已选内容列表，模糊匹配选项文字
        :param parent_xpath:
        """
        for item in list_item:
            item_loc = parent_xpath + f"//*[contains(text(),'{item}')]/ancestor::*[contains(@class,'ui-list-content')]"
            # 等待元素出现
            self.wait_elem_visible(item_loc, time_out=15)
            self.move_on(item_loc)
            self.icon.click_cancel_icon(item_loc)
            self.sleep(.5)

    def browser_search_select(self,select_value,parent_xpath="",need_serch=True,**kwargs):
        """
        浏览框输入查询后选择（模糊匹配文字）
        :param select_value:选项内容文字
        :param parent_xpath:
        """
        # 输入查询内容
        input_loc = parent_xpath + "//*[contains(@class,'ui-browser-associative-search-input')]//input"
        self.wait_elem_visible(input_loc)
        if need_serch:
            self.input(input_loc,select_value)
        else:
            self.click_element(input_loc)
        self.sleep(.5)
        browser_drop = "//*[@class='ui-scroller']//*[contains(@class,'ui-browser-associative-dropdown-list')]"
        # 等待下拉列表加载
        self.wait_elem_visible(browser_drop, time_out=10)
        # 选择
        select_loc = browser_drop + f"//*[contains(text(),'{select_value}')]"
        self.click_element(select_loc)

    def move_and_browser_search_select(self,list_select_value,parent_xpath="",**kwargs):
        """
        移到浏览框搜索按钮上加载浏览框再查询选择下拉框内容
        :param list_select_value: 选项内容，多个选项组成的列表，单个选项也可不使用列表；多次根据选项输入选择内容
        :param parent_xpath:
        :return:
        """
        if kwargs.get('is_multiple'):
            add_loc = parent_xpath + "//*[contains(@class,'Icon-add-to01')]"
            self.move_on(add_loc)
        move_loc = parent_xpath + "//*[contains(@class,'ui-browser-associative-search-input')]"
        if isinstance(list_select_value,list):
            list_select_value = list_select_value
        else:
            list_select_value = [list_select_value]
        for select_value in list_select_value:
            self.move_on(move_loc)
            self.browser_search_select(select_value,parent_xpath)

    def is_browser_item_read_only(self,parent_xpath="",**kwargs):
        """
        浏览框选项是否只读
        :param parent_xpath
        """
        item_loc = parent_xpath + "//*[contains(@class,'ui-browser-associative-selected-item')]"
        elems = self.find_elements(item_loc)
        if not elems:
            raise Exception("未查找到浏览按钮选项值，无法判断是否只读！")
        for ele in elems:
            if not self.check_elem_attribute(ele,"is-readonly"):
                return False
        return True

    def get_dialog_by_title(self,title):
        """
        根据title获取当前激活的浏览框弹窗元素的xpath
        """
        loc = f"//*[contains(@class,'ui-title')]//*[text()='{title}']/ancestor::*[@class='ui-dialog-portal']"
        return loc

    def get_active_browser_dialog(self,dialog_pre="", **kwargs):
        """
        获取当前激活的浏览框弹窗元素的xpath
        """
        loc = dialog_pre + "//*[contains(@class,'ui-dialog-wrap') and not(contains(@class,'ui-dialog-content-middle-fadeOut'))]"
        if kwargs.get('add_path'):
            loc = f'{loc}//div[contains(@class,"content-main") and not(contains(@class,"hidden"))]'
        self.wait_elem_visible(loc)
        return loc

    def browser_dialog_search(self,select_value,dialog_pre=""):
        """
        浏览框弹窗查询选项
        :param select_value: 查询内容
        :return:
        """

        dialog_xpath = dialog_pre if dialog_pre else self.get_active_browser_dialog()
        search_input = dialog_xpath + "//*[contains(@class,'ui-searchAdvanced-input')]//input"
        self.click_element(search_input)
        self.sleep(0.5)
        enter_loc = dialog_xpath + '//*[name()="svg"][contains(@class, "ui-icon-svg") and contains(@class, "Icon-enter")]'   #input框内回车图标
        if self.is_element_exist(enter_loc):
            self.inputUi.input_and_click(search_input, select_value, enter_loc)
        else:
            self.input_and_enter(search_input, select_value)
        self.sleep(0.5)

    def browser_dialog_list_item_select(self,list_select_value,parent_tab,checkbox_type=True,dialog_pre=""):
        """
        浏览框弹窗勾选选项
        :param list_select_value: 勾选内容文字列表，完全匹配选项内容
        :param parent_tab: 选项父级xpath路径
        :param checkbox_type: 勾选类型，True:勾选，False:取消勾选，默认True
        :return:
        """
        for select_value in list_select_value:
            # 搜索查询
            self.browser_dialog_search(select_value,dialog_pre)
            self.sleep(.5)
            # 选择选项
            loc = parent_tab + f"//*[text()='{select_value}']/ancestor::*[@class='ui-list-content']"
            contains_loc = parent_tab + f"//*[contains(text(),'{select_value}')]/ancestor::*[@class='ui-list-content']"
            loc = loc if self.is_element_exist(loc) else contains_loc
            self.checkbox.select_checkbox_button(checkbox_type,loc)

    def browser_dialog_item_select(self,select_value,parent_tab,dialog_pre=""):
        """
        浏览框弹窗-搜索后点击期望选项
        :param select_value: 点击内容文字，完全匹配选项内容
        :param parent_tab: 选项父级xpath路径
        :return:
        """
        # 搜索查询
        self.browser_dialog_search(select_value,dialog_pre)
        self.sleep(.5)
        # 点击选项
        loc = parent_tab + f"//*[text()='{select_value}']/ancestor::*[@class='ui-list-content']"
        self.click_element(loc)

    def browser_dialog_tab_multiple_item_select(self,tab,list_select_value,parent_div,checkbox_type=True):
        """
        浏览框弹窗有分页下选择复选内容
        :param tab: 分页名称
        :param list_select_value: 勾选内容文字列表，完全匹配选项内容
        :param parent_div: 分页父级xpath路径，一般是弹窗路径
        :param checkbox_type:
        :return:
        """
        # 选择分页
        self.menu.menu_click_menu_item(tab, parent_div)
        parent_tab = parent_div + "//*[contains(@class,'ui-browser-panel-content-box')]/*[not(contains(@class,'is-hidden'))]"
        # 勾选
        self.browser_dialog_list_item_select(list_select_value,parent_tab,checkbox_type,parent_div)

    def browser_dialog_tab_single_item_click(self,tab,select_value,parent_div):
        """
        浏览框弹窗有分页下选择单选内容
        :param tab: 分页名称
        :param select_value: 勾选内容文字，完全匹配选项内容
        :param parent_div: 分页父级xpath路径，一般是弹窗路径
        :return:
        """
        # 选择分页
        self.menu.menu_click_menu_item(tab, parent_div)
        parent_tab = parent_div + "//*[contains(@class,'ui-browser-panel-content-box')]/*[not(contains(@class,'is-hidden'))]"
        # 搜索查询
        self.browser_dialog_search(select_value,parent_div)
        # 选择单选点击选项
        click_loc = parent_tab + f"//*[contains(@class,'ui-list-item-row')]//*[text()='{select_value}']"
        self.click_element(click_loc)

    def browser_dialog_multiple_select(self,list_select_value,checkbox_type=True,confirm=True):
        """
        浏览框弹窗无分页多选
        :param list_select_value: 勾选内容文字列表，完全匹配选项内容
        :param checkbox_type: 勾选类型，True:勾选，False:取消勾选，默认True
        :param confirm: 是否需要点击确定，默认True
        :return:
        """
        dialog_xpath = self.get_active_browser_dialog()
        # 选择列表内容
        self.browser_dialog_list_item_select(list_select_value, dialog_xpath, checkbox_type)
        # 点击确定
        if confirm:
            self.sleep(0.5)
            button_loc = dialog_xpath + self.browser_confirm_sure
            self.click_element(button_loc)

    def browser_dialog_single_select(self,select_value,parent_xpath=""):
        """
        浏览框弹窗无分页单选
        :param select_value:选项内容
        :return:
        """
        dialog_xpath = self.get_active_browser_dialog(parent_xpath)
        # 搜索查询
        self.browser_dialog_search(select_value,parent_xpath)
        # 选择单选点击选项
        click_loc = dialog_xpath + f"//*[contains(@class,'ui-list-item-row-span') and text()='{select_value}']"
        self.click_element(click_loc)

    def browser_multiple_select(self,list_select_value,parent_xpath="",checkbox_type=True,confirm=True,title="",**kwargs):
        """
        浏览框多选
        :param list_select_value: 勾选内容文字列表，完全匹配选项内容
        :param parent_xpath: 浏览框按钮父级xpath
        :param checkbox_type: 勾选类型，True:勾选，False:取消勾选，默认True
        :param confirm:是否需要点击确定，默认True
        :return:
        """
        # 点击浏览框按钮
        self.icon.click_search_icon(parent_xpath)
        self.sleep(1)
        dialog_pre = self.get_dialog_by_title(title) if title else ""
        dialog_xpath1 = self.get_active_browser_dialog(dialog_pre, add_path=kwargs.get('add_path'))
        dialog_xpath = self.get_active_browser_dialog(dialog_pre)
        # 选择列表内容
        self.browser_dialog_list_item_select(list_select_value, dialog_xpath1, checkbox_type)
        # 点击确定
        if confirm:
            button_loc = dialog_xpath + self.browser_confirm_sure
            self.click_element(button_loc)

    def browser_single_select(self,select_value,parent_xpath="",title="",**kwargs):
        """
        浏览框单选
        :param select_value: 勾选内容文字
        :param parent_xpath: 浏览框按钮父级xpath
        :return:
        """
        # 点击浏览框按钮
        self.icon.click_search_icon(parent_xpath)
        self.sleep(1)
        dialog_pre = self.get_dialog_by_title(title) if title else "//*[contains(@class,'is-single')]"
        dialog_xpath = self.get_active_browser_dialog(dialog_pre)
        if kwargs.get('add_path'):
            dialog_xpath = self.get_active_browser_dialog(dialog_pre, add_path=kwargs.get('add_path'))
        # 搜索查询
        self.browser_dialog_search(select_value,dialog_xpath)
        # 选择单选点击选项
        click_loc = dialog_xpath + f"//*[contains(@class,'ui-list-item-row')]//*[text()='{select_value}']"
        self.click_element(click_loc)

    def browser_single_table_select(self,select_value,parent_xpath="",title="",**kwargs):
        """
        浏览框表格类型单选
        :param select_value: 勾选内容文字
        :param parent_xpath: 浏览框按钮父级xpath
        :return:
        """
        # 点击浏览框按钮
        self.icon.click_search_icon(parent_xpath)
        self.sleep(1)
        dialog_pre = self.get_dialog_by_title(title) if title else "//*[contains(@class,'is-single')]"
        dialog_xpath = self.get_active_browser_dialog(dialog_pre)
        # 搜索查询
        self.browser_dialog_search(select_value,dialog_xpath)
        # 选择单选点击选项
        click_loc = dialog_xpath + f"//*[contains(@class,'ui-table-grid-table')]//*[text()='{select_value}']"
        self.click_element(click_loc)

    def choose_user_single(self,select_data,tab_type="所有人",**kwargs):
        """
        选择人员-单选
        :param select_data: 选择的数据
        :param tab_type: 分页名称，默认是所有人分页
        :param kwargs：其他待扩展内容
        :return:
        """
        parent_div = self.get_active_browser_dialog(self.get_dialog_by_title("选择人员"))
        # 根据分页选择人员
        if tab_type in ["所有人"]:
            # 选择分页数据
            self.browser_dialog_tab_single_item_click(tab_type, select_data, parent_div)
        else:
            raise ValueError(f"分页类型{tab_type}暂不支持！")

    def choose_user_multiple(self,select_data,tab_type="所有人",confirm=True,**kwargs):
        """
        选择人员-多选
        :param select_data: 选择的数据
        :param tab_type: 分页名称，默认是列表分页
        :param confirm: 是否点击确定按钮
        :param kwargs：其他待扩展内容
        """
        parent_div = self.get_active_browser_dialog(self.get_dialog_by_title("选择人员"))
        # 根据分页选择人员
        if tab_type in ["所有人"]:
            # 选择分页数据
            self.browser_dialog_tab_multiple_item_select(tab_type, select_data, parent_div)
        else:
            raise ValueError(f"分页类型{tab_type}暂不支持！")
        # 点击确定
        if confirm:
            self.sleep(1)
            button_loc = parent_div+self.browser_confirm_sure
            self.click_element(button_loc)

    def choose_depart_single(self,select_data,tab_type="列表",**kwargs):
        """
        选择部门-单选
        :param select_data: 选择的数据
        :param tab_type: 分页名称，默认是列表分页
        :param kwargs：其他待扩展内容
        :return:
        """
        parent_div = self.get_active_browser_dialog()
        # 根据分页选择部门
        if tab_type in ["列表"]:
            # 选择分页数据
            self.browser_dialog_tab_single_item_click(tab_type, select_data, parent_div)
        else:
            raise ValueError(f"分页类型{tab_type}暂不支持！")

    def choose_depart_multiple(self,select_data,tab_type="列表",confirm=True,**kwargs):
        """
        选择部门-多选
        :param select_data: 选择的数据
        :param tab_type: 分页名称，默认是列表分页
        :param confirm: 是否点击确定按钮
        :param kwargs：其他待扩展内容
        """
        parent_div = self.get_active_browser_dialog("//*[contains(@class,'is-multiple')]")
        # 根据分页选择部门
        if tab_type in ["列表"]:
            # 选择分页数据
            self.browser_dialog_tab_multiple_item_select(tab_type, select_data, parent_div)
        else:
            raise ValueError(f"分页类型{tab_type}暂不支持！")
        # 点击确定
        if confirm:
            self.sleep(.5)
            button_loc = parent_div + self.browser_confirm_sure
            self.click_element(button_loc)

    def choose_group_multiple(self,select_data,tab_type="公共组",confirm=True,**kwargs):
        """
        选择群组-多选
        :param select_data: 选择的数据
        :param tab_type: 分页名称，默认是公共组分页
        :param confirm: 是否点击确定按钮
        :param kwargs：其他待扩展内容
        """
        parent_div = self.get_active_browser_dialog()
        # 根据分页选择群组
        if tab_type in ["公共组"]:
            # 选择分页数据
            self.browser_dialog_tab_multiple_item_select(tab_type, select_data, parent_div)
        else:
            raise ValueError(f"分页类型{tab_type}暂不支持！")
        # 点击确定
        if confirm:
            button_loc = parent_div + self.browser_confirm_sure
            self.click_element(button_loc)

    def choose_position_single(self,select_data,tab_type="按列表",**kwargs):
        """
        选择岗位-单选
        :param select_data: 选择的数据
        :param tab_type: 分页名称
        :param kwargs：其他待扩展内容
        :return:
        """
        parent_div = self.get_active_browser_dialog("//*[contains(@class,'is-single')]")
        # 根据分页选择岗位
        if tab_type in ["按列表"]:
            # 选择分页数据
            self.browser_dialog_tab_single_item_click(tab_type, select_data, parent_div)
        else:
            raise ValueError(f"分页类型{tab_type}暂不支持！")

    def choose_position_multiple(self,select_data,tab_type="按列表",confirm=True,**kwargs):
        """
        选择岗位-多选
        :param select_data: 选择的数据
        :param tab_type: 分页名称
        :param confirm: 是否点击确定按钮
        :param kwargs：其他待扩展内容
        """
        parent_div = self.get_active_browser_dialog()
        # 根据分页选择岗位
        if tab_type in ["按列表"]:
            # 选择分页数据
            self.browser_dialog_tab_multiple_item_select(tab_type, select_data, parent_div)
        else:
            raise ValueError(f"分页类型{tab_type}暂不支持！")
        # 点击确定
        if confirm:
            button_loc = parent_div+self.browser_confirm_sure
            self.click_element(button_loc)

    def choose_subcompany_single(self,select_data,tab_type="列表",**kwargs):
        """
        选择分部-单选
        :param select_data: 选择的数据
        :param tab_type: 分页名称，默认是列表分页
        :param kwargs：其他待扩展内容
        :return:
        """
        parent_div = self.get_active_browser_dialog()
        # 根据分页选择分部
        if tab_type in ["列表"]:
            # 选择分页数据
            self.browser_dialog_tab_single_item_click(tab_type, select_data, parent_div)
        else:
            raise ValueError(f"分页类型{tab_type}暂不支持！")

    def choose_subcompany_multiple(self,select_data,tab_type="列表",confirm=True,**kwargs):
        """
        选择分部-多选
        :param select_data: 选择的数据
        :param tab_type: 分页名称，默认是列表分页
        :param confirm: 是否点击确定按钮
        :param kwargs：其他待扩展内容
        :return:
        """
        parent_div = self.get_active_browser_dialog()
        # 根据分页选择分部
        if tab_type in ["列表"]:
            # 选择分页数据
            self.browser_dialog_tab_multiple_item_select(tab_type, select_data, parent_div)
        else:
            raise ValueError(f"分页类型{tab_type}暂不支持！")
        # 点击确定
        if confirm:
            button_loc = parent_div + self.browser_confirm_sure
            self.click_element(button_loc)

    def browser_single_select_by_type(self,select_type,select_data,parent_xpath="",select_kwargs={},**kwargs):
        """
        浏览框根据类型进行单选
        :param select_type: 浏览框类型，例如人员、部门等
        :param select_data:选择的数据，列表
        :param parent_xpath:浏览框按钮的父级路径，不传就不点击
        :param select_kwargs:其他参数，例如浏览框分页名称等
        :return:None
        """
        # 选择组合浏览框类型
        if select_type == "人员":
            self.icon.click_search_icon(parent_xpath)
            self.sleep(0.5)
            self.choose_user_single(select_data, **select_kwargs)
        elif select_type == "部门":
            self.icon.click_search_icon(parent_xpath)
            self.sleep(0.5)
            self.choose_depart_single(select_data, **select_kwargs)
        elif select_type == "分部":
            self.icon.click_search_icon(parent_xpath)
            self.sleep(0.5)
            self.choose_subcompany_single(select_data, **select_kwargs)
        elif select_type == "岗位":
            self.icon.click_search_icon(parent_xpath)
            self.sleep(0.5)
            self.choose_position_single(select_data, **select_kwargs)
        elif select_type in ["角色"]:
            self.icon.click_search_icon(parent_xpath)
            self.sleep(0.5)
            self.browser_dialog_single_select(select_data)
        elif select_type in ["所有人"]:
            pass
        else:
            raise ValueError(f"类型{select_type}暂不支持！")

    def browser_multiple_select_by_type(self, select_type, list_select_data, parent_xpath="", select_kwargs={},**kwargs):
        """
        浏览框根据类型进行多选
        :param select_type: 浏览框类型，例如人员、部门等
        :param list_select_data:选择的数据，列表
        :param parent_xpath:浏览框按钮的父级路径
        :param select_kwargs:其他参数，例如浏览框分页名称等
        :return:None
        """
        # 选择组合浏览框类型
        if select_type == "人员":
            self.icon.click_search_icon(parent_xpath)
            self.sleep(0.5)
            self.choose_user_multiple(list_select_data, **select_kwargs)
        elif select_type == "部门":
            self.icon.click_search_icon(parent_xpath)
            self.sleep(0.5)
            self.choose_depart_multiple(list_select_data, **select_kwargs)
        elif select_type == "分部":
            self.icon.click_search_icon(parent_xpath)
            self.sleep(0.5)
            self.choose_subcompany_multiple(list_select_data, **select_kwargs)
        elif select_type == "岗位":
            self.icon.click_search_icon(parent_xpath)
            self.sleep(0.5)
            self.choose_position_multiple(list_select_data, **select_kwargs)
        elif select_type in ["角色"]:
            self.icon.click_search_icon(parent_xpath)
            self.sleep(0.5)
            self.browser_dialog_multiple_select(list_select_data, **select_kwargs)
        elif select_type == "群组":
            self.icon.click_search_icon(parent_xpath)
            self.sleep(0.5)
            self.choose_group_multiple(list_select_data, **select_kwargs)
        elif select_type in ["所有人"]:
            pass
        else:
            raise ValueError(f"类型{select_type}暂不支持！")

    def browser_types_single_select(self,select_type,select_data="",parent_xpath="",select_kwargs={}, need_add=True,**kwargs):
        """
        组合浏览框-单选
        :param select_type: 选择类型
        :param select_data: 勾选选项内容
        :param parent_xpath:组合浏览框所在的父级xpath路径
        :param select_kwargs:浏览框操作的其他参数，默认可以不传
        :param need_add:是否需要移动到添加框上
        :param kwargs:后续扩展
        :return:
        """
        # 如果需要移动到添加框上
        if need_add:
            # add_loc = parent_xpath + "//*[contains(@class,'ui-browser-types-associative-inner-add')]"
            add_loc = parent_xpath + "//*[contains(@class,'associative-inner-add')]"
            self.move_on(add_loc)
        # 选择类型
        self.selectUi.select_button(select_type, parent_xpath)
        if select_data:
            self.browser_single_select_by_type(select_type,select_data,parent_xpath,select_kwargs)

    def browser_types_multiple_select(self,list_select_data,parent_xpath="",select_kwargs={}, need_add=True,**kwargs):
        """
        组合浏览框-复选
        :param list_select_data: 多次组合浏览框复选操作，每次操作都需要提供select_type(选择类型)和list_select_value(勾选选项内容列表)
        :param parent_xpath:组合浏览框所在的父级xpath路径
        :param select_kwargs:浏览框操作的其他参数，默认可以不传
        :param need_add:是否需要移动到添加框上
        :param kwargs:后续扩展
        :return:
        """
        for select_data in list_select_data:
            # 如果需要移动到添加框上
            if need_add:
                # add_loc = parent_xpath + "//*[contains(@class,'ui-browser-types-associative-inner-add')]"
                add_loc = parent_xpath + "//*[contains(@class,'associative-inner-add')]"
                self.move_on(add_loc)
            # 选择类型
            select_type = select_data.get("select_type")
            self.selectUi.select_button(select_type, parent_xpath)
            list_select_value = select_data.get("list_select_value")
            if list_select_value:
                self.browser_multiple_select_by_type(select_type,list_select_value,parent_xpath,select_kwargs)

    def browser_single_select_search(self,search_value,parent_xpath="",title="",**kwargs):
        """
        浏览框根据查询条件点击
        :param search_value: 点击内容文字，完全匹配选项内容
        :param parent_xpath: 浏览框按钮父级xpath
        :param title: 浏览框标题
        :return:
        """
        # 点击浏览框按钮
        self.icon.click_search_icon(parent_xpath)
        self.sleep(1)
        dialog_pre = self.get_dialog_by_title(title) if title else ""
        dialog_xpath = self.get_active_browser_dialog(dialog_pre)
        # 点击搜索结果
        self.browser_dialog_item_select(search_value, dialog_xpath)