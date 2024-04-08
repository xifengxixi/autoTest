import time
from common.base import Page
from . import icon, browseBox, table, button


class Dialog(Page):
    """
    Dialog弹层
    dialog_get_confirm_title：获取确认框标题
    dialog_get_confirm_content：获取确认框内容
    dialog_confirm_btn_click：确认框按扭点击
    dialog_confirm_close：关闭提示框
    dialog_check_confirm：确认框校验操作
    dialog_close_dialog：关闭弹框
    dialog_enlarge_dialog：最大化弹框
    dialog_narrow_dialog：最小化弹框
    dialog_click_dialog_header_loc：点击弹框页头元素
    dialog_click_dialog_footer_loc：点击弹框页脚元素
    dialog_click_dialog_body_loc：点击弹框体元素
    dialog_get_dialog_title：获取弹框标题
    dialog_get_dialog_content：获取弹框内容
    dialog_maximize_dialog：悬停后-最大化
    dialog_reduction_dialog：悬停后-还原
    dialog_new_window_dialog：悬停后-新窗口打开
    dialog_get_message_dialog_content：获取消息层弹框内容
    dialog_get_message_content：获取toast提示信息内容
    dialog_close_message：关闭toast提示信息
    dialog_click_menu_list_item：点击弹框的页签
    dialog_close_wait：在等待时间内如果出现弹窗就关闭
    dialog_get_loc：获取弹框的元素
    dialog_click_loc：点击弹框的元素
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.icon = icon.Icon(driver)
        self.browseBox = browseBox.BrowseBox(driver)
        self.table = table.Table(driver)
        self.button = button.Button(driver)

    def dialog_get_confirm_title(self, parent_xpath=""):
        """获取确认框标题"""
        loc = '//div[@class="ui-confirm-title"]'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        return self.get_element_text(ele_loc)

    def dialog_get_confirm_content(self, parent_xpath=""):
        """获取确认框内容"""
        loc = '//div[contains(@class,"ui-confirm-body")]'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        return self.get_element_text(ele_loc)

    def dialog_check_confirm_content(self, content, parent_xpath=""):
        """校验确认框内容"""
        text = self.dialog_get_confirm_content(parent_xpath)
        assert content in text, f"确认框内容校验失败，期望：{content}，实际：{text}"

    def dialog_confirm_btn_click(self, button, parent_xpath=""):
        """确认框按扭点击"""
        if self.is_element_exist("//*[@class='ui-confirm-footer']"):
            pre = "//*[@class='ui-confirm-footer']"
        elif self.is_element_exist("//*[contains(@class,'ui-dialog-footer')]",wait=0):
            pre = "//*[contains(@class,'ui-dialog-footer')]"
        elif self.is_element_exist("//*[contains(@class,'ui-m-dialog-footer')]",wait=0):
            pre = "//*[contains(@class,'ui-m-dialog-footer')]"
        elif self.is_element_exist("//*[contains(@class,'ui-confirm-footer')]",wait=0):
            pre = "//*[contains(@class,'ui-confirm-footer')]"
        else:
            raise "未找到确认框"
        loc = f"{pre}//button[text()='{button}']|{pre}//div[text()='{button}']"
        ele_loc = parent_xpath + loc if parent_xpath else loc
        self.click_element(ele_loc)

    def dialog_confirm_close(self, parent_xpath=""):
        """关闭提示框"""
        loc = "//*[@class='ui-confirm-header']"
        ele_loc = parent_xpath + loc if parent_xpath else loc
        self.icon.click_close_icon(ele_loc)

    def dialog_check_confirm(self,**kwargs):
        """
        确认框校验操作
        """
        if "标题" in kwargs:
            title = self.dialog_get_confirm_title()
            if title.find(kwargs["标题"])<0:
                assert False, f"确认框标题校验失败，期望：{kwargs['标题']}，实际：{title}"
        if "内容" in kwargs:
            content = self.dialog_get_confirm_content()
            if content.find(kwargs["内容"])<0:
                assert False, f"确认框内容校验失败，期望：{kwargs['内容']}，实际：{content}"
        if "按钮" in kwargs:
            self.dialog_confirm_btn_click(kwargs['按钮'])

    def dialog_close_dialog(self, parent_xpath=""):
        """关闭弹框"""
        loc = '//div[contains(@class, "ui-title-inDialog")]'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        self.icon.click_close_icon(ele_loc)

    def dialog_close_dialogs_new(self,closeAll=False):
        """ 有多个弹框时关闭最外层弹框(closeAll为True时关闭全部弹框) """
        loc = '//div[contains(@class, "ui-title-inDialog")]'
        if self.is_element_exist(loc):
            nums = len(self.find_elements(loc))
            for n in range(nums,0,-1):
                self.icon.click_close_icon(f"({loc})[position()={n}]")
                if closeAll is False:
                    break

    def dialog_enlarge_dialog(self, parent_xpath=""):
        """最大化弹框"""
        loc = '//*[name()="svg" and contains(@class, "Icon-enlarge01")]'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        self.click_element(ele_loc)

    def dialog_narrow_dialog(self, parent_xpath=""):
        """最小化弹框"""
        loc = '//*[name()="svg" and contains(@class, "Icon-narrow01")]'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        self.click_element(ele_loc)

    def dialog_click_dialog_header_loc(self, loc_name, parent_xpath="", position="1", fuzzy=True):
        """点击弹框页头元素"""
        loc = f'(//*[contains(@class,"ui-dialog")]{parent_xpath}//*[contains(@class,"title")]//*[contains(text(),"{loc_name}")])[position()={position}]'
        if not fuzzy:
            loc = f'(//*[contains(@class,"ui-dialog")]{parent_xpath}//*[contains(@class,"title")]//*[text()="{loc_name}"])[position()={position}]'
        self.click_element(loc)

    def dialog_click_dialog_footer_loc(self, loc_name, parent_xpath="", position="1", fuzzy=True):
        """点击弹框页脚元素"""
        loc = f'(//*[contains(@class,"ui-dialog")]{parent_xpath}//*[contains(@class,"footer")]//*[contains(text(),"{loc_name}")])[position()={position}]'
        if not fuzzy:
            loc = f'(//*[contains(@class,"ui-dialog")]{parent_xpath}//*[contains(@class,"footer")]//*[text()="{loc_name}"])[position()={position}]'
        self.click_element_disWait(loc)

    def dialog_click_dialog_body_loc(self, loc_name, parent_xpath="", position="1", fuzzy=True):
        """点击弹框体元素"""
        loc = f'(//*[contains(@class,"ui-dialog")]//*[contains(@class,"body")]{parent_xpath}//*[contains(text(),"{loc_name}")])[position()={position}]'
        if not fuzzy:
            loc = f'(//*[contains(@class,"ui-dialog")]//*[contains(@class,"body")]{parent_xpath}//*[text()="{loc_name}"])[position()={position}]'
        self.click_element(loc)

    def dialog_get_dialog_title(self, index=0, dialog_position=1, parent_xpath="", prefix=False):
        """
        获取弹框标题
        支持获取多级弹框标题，通过index取值，此处index从0开始
        """
        if prefix:
            loc = f'({parent_xpath}//div[contains(@class,"ui-dialog-wrap") and not(contains(@class,"fade"))]//div[contains(@class,"inner-container")])[position()={dialog_position}]//div[@class="ui-title-title-top"]'
        else:
            loc = f'{parent_xpath}//div[@class="ui-title-title-top"]'
        title_list = self.get_elements_text(loc)
        title_list = [x for x in title_list if x != ""]
        return title_list[index] if index else title_list[0]

    def dialog_get_dialog_content(self, level=1, index=None, parent_xpath=""):
        """
        获取弹框内容
        支持获取多级弹框内容，通过level取值，如level=1表示获取一级弹框的内容，弹框内容列表通过index取值
        """
        loc = f'(//div[contains(@class,"ui-dialog")]//div[contains(@class,"body")])[position()="{level}"]'
        content_list = []
        if self.is_element_exist(loc + '//p'):
            loc = loc + '//p'
            ele_loc = parent_xpath + loc if parent_xpath else loc
            eles = self.find_elements(ele_loc)
            for i in range(len(eles)):
                if not self.is_element_exist(f'{ele_loc}[position()="{i+1}"]' + '/*'):
                    content_list.append(eles[i].text)
        elif self.is_element_exist(loc + '/div'):
            loc = loc + '/div'
            ele_loc = parent_xpath + loc if parent_xpath else loc
            eles = self.find_elements(ele_loc)
            for ele in eles:
                content_list.append(ele.text)
        else:
            ele_loc = f'{parent_xpath}{loc}'
            content_list = self.get_elements_text(ele_loc)
        content_list = [x for x in content_list if x != ""]
        return content_list[index] if index else content_list

    def dialog_maximize_dialog(self, parent_xpath=""):
        """悬停后-最大化"""
        loc = '//*[name()="svg" and contains(@class, "Icon-enlarge01")]'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        max_loc = '//span[text()="最大化"]'
        self.move_click(ele_loc, max_loc)

    def dialog_reduction_dialog(self, parent_xpath=""):
        """悬停后-还原"""
        loc = '//*[name()="svg" and contains(@class, "Icon-narrow01")]'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        min_loc = '//span[text()="还原"]'
        self.move_click(ele_loc, min_loc)

    def dialog_new_window_dialog(self, parent_xpath=""):
        """悬停后-新窗口打开"""
        loc = '//*[name()="svg" and (contains(@class, "Icon-enlarge01") or contains(@class, "Icon-narrow01"))]'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        new_window_loc = '//span[text()="新窗口打开"]'
        self.move_click(ele_loc, new_window_loc)

    def dialog_get_message_dialog_content(self, parent_xpath=""):
        """获取消息层弹框内容"""
        loc = '//div[contains(@class,"ui-dialog-body")]/div'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        return self.get_element_text(ele_loc)

    def dialog_get_message_content(self, parent_xpath=""):
        """获取toast提示信息内容"""
        loc = '//div[@class="ui-message-body"]'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        return self.get_element_text(ele_loc)

    def dialog_close_message(self, parent_xpath="", index="1"):
        """关闭toast提示信息"""
        message_single_loc = f'//div[contains(@class, "ui-message-single") and position()="{index}"]'
        self.move_on(message_single_loc)
        loc = f'(//*[@class="ui-message"]//*[name()="svg" and contains(@class, "Icon-solid")])[position()="{index}"]'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        self.click_element(ele_loc)

    def dialog_click_menu_list_item(self, item_name, parent_xpath=""):
        """点击弹框的页签"""
        loc = f'//div[@class="ui-menu-tab-top-container"]//div[@title="{item_name}"]'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        self.click_element(ele_loc)

    def dialog_close_wait(self,max_wait):
        """
        在等待时间内如果出现弹窗就关闭
        :param max_wait:
        :return:
        """
        init_time = time.time()
        delay = 1  # 检测间隔时间
        loc = '//div[contains(@class, "ui-title-inDialog")]'
        while time.time() - init_time < int(max_wait):
            if self.is_element_exist(loc):
                self.dialog_close_dialog()
                break
            time.sleep(delay)


    def dialog_get_loc(self, target, dialog_position=1, position=1, parent_xpath=''):
        """
        获取弹框的元素
        :param target: 点击的目标元素，例：'span/input'
        :param dialog_position: 弹框的位置，如有多个弹框的时候，根据此参数区分
        :param position: 目标元素的位置，如有多个匹配结果的时候，根据此参数区分
        :param parent_xpath:
        :return:
        """
        loc = (f'((//div[contains(@class,"ui-dialog-wrap") and not(contains(@class,"fade"))]'
               f'//div[contains(@class,"inner-container")])[position()={dialog_position}]{parent_xpath}//{target})[position()={position}]')
        return loc

    def dialog_click_loc(self, target, dialog_position=1, position=1, parent_xpath=''):
        """
        点击弹框的元素
        :param target: 点击的目标元素，例：'span/input'
        :param dialog_position: 弹框的位置，如有多个弹框的时候，根据此参数区分
        :param position: 目标元素的位置，如有多个匹配结果的时候，根据此参数区分
        :param parent_xpath:
        :return:
        """
        ele_loc = self.dialog_get_loc(target, dialog_position, position, parent_xpath)
        self.click_element(ele_loc)

    def dialog_table_serch_and_select(self,title,list_select_content,serch_value="",operator_button="",parent_xpath='',isShow=True):
        """
        弹窗页面查询并勾选表格数据（例如批量操作页面）
        :param list_select_content: 勾选数据
        :param serch_value: 查询数据
        :param operator_button: 操作
        :param title: 如果需要校验标题
        :param parent_xpath:
        :param isShow: 是否显示选择框（不显示选择框的场景如：以序号代替，鼠标悬浮在指定行才会显示选择框）True显示 False不显示
        :return:
        """
        # 等待弹窗标题元素激活（校验标题）
        dialog_pre = self.browseBox.get_active_browser_dialog(self.browseBox.get_dialog_by_title(title))
        # 搜索
        if serch_value:
            self.browseBox.browser_dialog_search(serch_value)
        # 勾选
        for content in list_select_content:
            self.table.table_selectByCell_content(content,isShow=isShow,parent_xpath=dialog_pre)
            time.sleep(.5)
        # 操作
        if operator_button:
            self.button.click_button(operator_button,parent_xpath=dialog_pre)

