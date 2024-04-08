from common.base import Page
from . import table, browseBox, scope, button, dialog, tips, selectUi, icon


class ShareList(Page):
    """
    共享组件:
    share_list_add:添加共享列表数据
    share_list_edit:编辑共享列表数据
    share_list_delete:选择共享对象删除
    share_list_delete_all:删除所有共享列表数据
    share_list_to_top:选择共享对象置顶
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.table = table.Table(driver)
        self.browseBox = browseBox.BrowseBox(driver)
        self.scope = scope.Scope(driver)
        self.button = button.Button(driver)
        self.dialog = dialog.Dialog(driver)
        self.tips = tips.Tips(driver)
        self.selectUi = selectUi.SelectUi(driver)
        self.icon = icon.Icon(driver)

    share_loc = "//*[@class='ui-share']"
    share_dialog_xpath = "//*[contains(@class,'ui-share-dialog')]"

    def share_edit_form(self,dict_input):
        """
        新增修改共享列表数据表单
        :param dict_input: 输入数据,例子:{"对象类型":"人员","对象":["自动化团队管理员","普通成员"]}
        :return:
        """
        # 获取激活窗口
        dialog_xpath = self.browseBox.get_active_browser_dialog(self.share_dialog_xpath)
        # 选择对象类型
        share_type = "人员"
        if dict_input.get("对象类型"):
            share_type = dict_input.get("对象类型")
            self.selectUi.select_button(share_type, dialog_xpath,form_lable="对象类型")
        # 选择对象
        if dict_input.get("对象"):
            self.browseBox.browser_multiple_select_by_type(share_type, dict_input.get("对象"),dialog_xpath,form_lable="对象")
        # 勾选项
        if dict_input.get("勾选项"):
            pass
        if dict_input.get("安全级别"):
            self.scope.scope_text(dict_input.get("安全级别"),dialog_xpath,form_lable="安全级别")
        if dict_input.get("岗位级别"):
            self.selectUi.select_button(dict_input.get("岗位级别"), dialog_xpath,form_lable="岗位级别")
        if dict_input.get("角色级别"):
            self.selectUi.select_button(dict_input.get("角色级别"),dialog_xpath,form_lable="角色级别")
        # 保存并校验成功
        self.button.click_button("保存", dialog_xpath)
        self.tips.check_tips_content("保存成功")

    def share_list_add(self,dict_input,parent_xpath=""):
        """
        添加共享列表数据
        :param dict_input: 输入数据,例子:{"对象类型":"人员","对象":["自动化团队管理员","普通成员"]}
        :param parent_xpath: 共享列表父级定位,默认从//*[@class='ui-share']层级开始往下定位
        :return:
        """
        # 点击添加
        loc = parent_xpath + self.share_loc
        self.icon.icon_click_add_to(loc)
        # 页面输入
        self.share_edit_form(dict_input)

    def share_list_edit(self,select,dict_input,parent_xpath=""):
        """
        编辑共享列表数据
        :param list_select: 选择要编辑的共享对象
        :param dict_input: 输入数据,例子:{"对象类型":"人员","对象":["自动化团队管理员","普通成员"]}
        :param parent_xpath: 共享列表父级定位,默认从//*[@class='ui-share']层级开始往下定位
        :return:
        """
        loc = parent_xpath + self.share_loc
        # 选择对象点击编辑
        self.table.table_row_more_menue_click("编辑",select,parent_loc=loc)
        # 页面输入
        self.share_edit_form(dict_input)

    def share_list_delete(self,list_delete,parent_xpath=""):
        """
        选择共享对象删除
        :param list_delete: 共享对象组成的列表
        :param parent_xpath: 共享列表父级定位,默认从//*[@class='ui-share']层级开始往下定位
        :return:
        """
        loc = parent_xpath + self.share_loc
        # 选择
        self.table.table_row_select(*list_delete,isShow=True,parent_loc=loc)
        # 点击删除
        loc = parent_xpath + self.share_loc
        self.icon.click_batch_delete_icon(loc)
        # 点击确定
        self.dialog.dialog_click_dialog_footer_loc("确定",loc)

    def share_list_delete_all(self,parent_xpath=""):
        """
        删除所有共享列表数据
        :param parent_xpath: 共享列表父级定位,默认从//*[@class='ui-share']层级开始往下定位
        :return:
        """
        loc = parent_xpath + self.share_loc
        # 选择
        self.table.table_row_select_all(parent_loc=loc)
        # 点击删除
        loc = parent_xpath + self.share_loc
        self.icon.click_batch_delete_icon(loc)
        # 点击确定
        self.dialog.dialog_click_dialog_footer_loc("确定",loc)

    def share_list_to_top(self,list_select,parent_xpath=""):
        """
        选择共享对象置顶
        :param list_select: 共享对象组成的列表
        :param parent_xpath: 共享列表父级定位,默认从//*[@class='ui-share']层级开始往下定位
        :return:
        """
        loc = parent_xpath + self.share_loc
        # 选择
        self.table.table_row_select(*list_select,isShow=True,parent_loc=loc)
        # 点击置顶
        self.icon.click_back_to_top_icon(loc)
        # 提示成功
        self.tips.check_tips_content("保存成功")

    def share_list_drag_by_value(self,source_value,target_value,source_type="value",target_type="value",parent_xpath=""):
        """
        共享列表根据拖拽对象所在行拖拽到目标所在行
        :param source_value: 拖拽对象
        :param target_value: 拖拽目标对象
        :param source_type: 拖拽对象类型,value:根据行内某个单元格值定位行;row:根据行号定位行
        :param target_type:拖拽目标对象类型,同上
        :return:
        """
        loc = parent_xpath + self.share_loc
        # 拖拽
        self.table.table_row_drag(source_value,target_value,source_type,target_type,loc)
        # 提示成功
        self.tips.check_tips_content("保存成功")


    def share_list_check(self,list_dict_check,check_type=1, match_type=1):
        """校验共享列表数据"""
        if check_type == 1:
            self.table.check_table_datas(list_dict_check, parent_xpath=self.share_loc, match_type=match_type)
        else:
            self.table.check_table_datas_not_exist(list_dict_check, parent_xpath=self.share_loc)


    def get_share_list_data(self,list_col):
        """获取共享列表数据"""
        list_table_data = self.table.get_table_data(list_col, self.share_loc)
        return list_table_data

    def share_row_operate(self,name,operate,dict_input={},parent_xpath=""):
        """
        共享列行操作
        :return:
        """
        loc = parent_xpath + self.share_loc
        # 行操作
        self.table.table_row_more_menue_click(operate, name, parent_xpath=loc,trigger_loc="")
        if operate == "编辑":
            self.share_edit_form(dict_input)
        elif operate in ["删除"]:
            self.dialog.dialog_confirm_btn_click("确定")


