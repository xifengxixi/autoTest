import win32con
import win32gui
from selenium.webdriver.common.by import By
from common.base import Page
from . import switch, button


class CommentUi(Page):
    """
    comment评论组件
    commentUi_input：评论
    commentUi_edit：编辑评论
    commentUi_reply：回复评论
    commentUi_delete：删除评论
    commentUi_assignment：评论转任务
    commentUi_consult：评论查阅
    commentUi_log：评论操作日志
    commentUi_input_richtext：富文本形式评论
    commentUi_edit_richtext：富文本形式编辑评论
    commentUi_reply_richtext：富文本形式回复评论
    commentUi_copy_richtext：复制评论
    commentUi_get_commentText：获取某条评论的评论内容
    commentUi_get_commentTextAll:获取所有评论的评论内容
    commentUi_desensitization：脱敏显示设置
    commentUi_changeId：单条评论切换id
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.switch = switch.Switch(driver)
        self.button = button.Button(driver)

    def edit_input_loc(self, parent_xpath="", **kwargs):
        '''获取评论输入框路径'''
        loc = parent_xpath + f"//div[contains(@class,'ui-comment-edit-input')]"
        return loc

    def commentUi_input(self,value, parent_xpath="", **kwargs):
        '''
        评论
        :param  value:评论的内容
        '''
        # 打开评论输入框
        ele_loc_comment = self.edit_input_loc(parent_xpath)
        self.click_element(ele_loc_comment)
        #输入内容
        loc_text = parent_xpath + f"//textarea[contains(@class,'ui-textarea auto-height ui-comment-textarea')]"
        ele_loc_text = self.find_element(loc_text)
        self.input_text(ele_loc_text, value)
        #点击发表
        self.button.click_button("发表", parent_loc=parent_xpath)

    def commentUi_edit(self,value, parent_xpath="", **kwargs):
        '''
        编辑评论
        :param value:评论的内容
        '''
        # 点击“编辑”
        loc_comment = parent_xpath + f'//div[@title="对本条评论的编辑"]'
        self.click_element(loc_comment)
        # 输入内容
        loc_text = parent_xpath + f"//textarea[contains(@class,'ui-textarea auto-height ui-comment-textarea')]"
        ele_loc_text = self.find_element(loc_text)
        self.input_text(ele_loc_text, value)
        # 点击修改
        self.button.click_button("修改", parent_loc=parent_xpath)

    def commentUi_reply(self,value, parent_xpath="", **kwargs):
        '''
        回复评论
        :param  value:评论的内容
        '''
        # 点击“回复”
        loc_comment = parent_xpath + f'//div[@title="对本条评论的回复"]'
        self.click_element(loc_comment)
        # 输入内容
        loc_text = parent_xpath + f"//textarea[contains(@class,'ui-textarea auto-height ui-comment-textarea')]"
        ele_loc_text = self.find_element(loc_text)
        self.input_text(ele_loc_text, value)
        # 点击回复
        self.button.click_button("回复", parent_loc=parent_xpath)

    def commentUi_delete(self, parent_xpath="", **kwargs):
        '''
        删除评论
        '''
        self.click_element(parent_xpath + f'//div[text()="删除"]')
        self.button.click_button("确定", parent_loc=parent_xpath)

    def commentUi_assignment(self, value, parent_xpath="", **kwargs):
        '''
        评论转任务
        :param value：转任务的内容
        '''
        # 点击“转任务”
        self.click_element(parent_xpath + f'//div[@title="转发到我的工作"]')
        # 输入内容
        loc_text = parent_xpath + f"//textarea[contains(@class,'ui-textarea auto-height ui-comment-textarea')]"
        ele_loc_text = self.find_element(loc_text)
        self.input_text(ele_loc_text, value)
        # 点击转发
        self.button.click_button("转发", parent_loc=parent_xpath)

    def commentUi_consult(self, parent_xpath="", **kwargs):
        '''
        评论查阅
        :return: 返回查阅列表的全部数据
        '''
        # 点击“查阅情况”
        loc_consult = parent_xpath + f"//span[text()='查阅情况']"
        self.click_element(loc_consult)
        #获取查阅情况数据
        i_texts = []
        parent_loc = parent_xpath + f'//div[@class="ui-comment-log"]'
        loc_ele = self.find_element(parent_loc)
        hrm_eles = loc_ele.find_elements(By.XPATH, f'.//a')
        for i in hrm_eles:
            i_text = i.text
            i_texts.append(i_text)
        j_texts = []
        status_eles = loc_ele.find_elements(By.XPATH, f'.//span[contains(@class,"ui-comment-log-status")]')
        for j in status_eles:
            j_text = j.text
            j_texts.append(j_text)
        k_texts = []
        time_eles = loc_ele.find_elements(By.XPATH, f'.//div[contains(@class,"ui-comment-log-time ui-comment-ellipsis")]')
        for k in time_eles:
            k_text = k.text
            k_texts.append(k_text)
        list = [[x, y, z] for x, y, z in zip(i_texts, j_texts, k_texts)]
        return list

    def commentUi_log(self, parent_xpath="", **kwargs):
        '''
        评论操作日志
        :return: 返回操作日志的全部数据
        '''
        # 点击“操作日志”
        loc_consult = parent_xpath + f"//span[text()='操作日志']"
        self.click_element(loc_consult)
        #获取操作日志数据
        i_texts = []
        parent_loc = parent_xpath + f'//div[contains(@class,"ui-list-body")]'
        loc_ele = self.find_element(parent_loc)
        hrm_eles = loc_ele.find_elements(By.XPATH, f'.//a[contains(@class,"weapp-elog-cardloglist-content-div-a")]')
        for i in hrm_eles:
            i_text = i.text
            i_texts.append(i_text)
        time_eles = loc_ele.find_elements(By.XPATH, f'.//span[contains(@class,"weapp-elog-cardloglist-content-div-span")]')
        k_texts = []
        for k in time_eles:
            k_text = k.text
            k_texts.append(k_text)
        n = 3
        list_text = [k_texts[i:i + n] for i in range(0, len(k_texts), n)]
        list = [[x, y] for x, y in zip(i_texts, list_text)]
        return list

    def weaUploadSelectByElement(self, element, accpath):
        '''
        comment评论组件上传附件
        :param  element:附件路径
        :return:
        '''
        self.click_element(element)
        dialog = win32gui.FindWindow('#32770', '打开')  # 对话框
        ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None)
        ComboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, 'ComboBox', None)
        Edit = win32gui.FindWindowEx(ComboBox, 0, 'Edit', None)  # 上面三句依次寻找对象，直到找到输入框Edit对象的句柄
        button = win32gui.FindWindowEx(dialog, 0, 'Button', None)  # 确定按钮Button
        win32gui.SendMessage(Edit, win32con.WM_SETTEXT, None, accpath)  # 往输入框输入绝对地址
        win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 按button

    def comment_upload_file(self, path, parent_xpath="", **kwargs):
        '''
        comment评论组件上传附件
        :param path:绝对路径
        :return:
        '''
        loc = parent_xpath + f'//div[contains(@class,"ui-upload-select-input")]'
        self.weaUploadSelectByElement(loc,path)

    def commentUi_input_richtext(self,value, parent_xpath="", **kwargs):
        '''
        富文本形式评论
        :param value:评论的内容
        '''
        #用户评论
        # 打开评论输入框
        ele_loc_comment = parent_xpath + "//div[contains(@class,'ui-comment-edit-input')]"
        self.click_element(ele_loc_comment)
        # 切换iframe
        loc = parent_xpath + '//div[contains(@class,"cke_contents cke_reset")]/iframe'
        ele = self.find_element((By.XPATH, loc))
        self.switch_frame(ele)
        #输入内容
        loc_text = parent_xpath + f"//body[contains(@class,'cke__pc cke_editable cke_editable_themed cke_contents_ltr')]"
        ele_loc_text = self.find_element(loc_text)
        self.input_text(ele_loc_text, value)
        self.driver.switch_to_default_content()
        #点击发表
        self.button.click_button("发表", parent_loc=parent_xpath)

    def commentUi_edit_richtext(self,value, parent_xpath="", **kwargs):
        '''
        富文本形式编辑评论
        :param value:评论的内容
        '''
        # 点击“编辑”
        loc_comment = f'//div[@title="对本条评论的编辑"]'
        self.click_element(loc_comment)
        # 切换iframe
        loc = parent_xpath + '//div[contains(@class,"cke_contents cke_reset")]/iframe'
        ele = self.find_element((By.XPATH, loc))
        self.switch_frame(ele)
        # 输入内容
        loc_text = parent_xpath + f"//body[contains(@class,'cke__pc cke_editable cke_editable_themed cke_contents_ltr')]"
        ele_loc_text = self.find_element(loc_text)
        self.input_text(ele_loc_text, value)
        self.driver.switch_to_default_content()
        # 点击修改
        self.button.click_button("修改", parent_loc=parent_xpath)

    def commentUi_reply_richtext(self,value, parent_xpath="", **kwargs):
        '''
        富文本形式回复评论
        :param value:评论的内容
        '''
        # 点击“回复”
        loc_comment = parent_xpath + f'//div[@title="对本条评论的回复"]'
        self.click_element(loc_comment)
        # 切换iframe
        loc = parent_xpath + '//div[contains(@class,"cke_contents cke_reset")]/iframe'
        ele = self.find_element((By.XPATH, loc))
        self.switch_frame(ele)
        # 输入内容
        loc_text = parent_xpath + f"//body[contains(@class,'cke__pc cke_editable cke_editable_themed cke_contents_ltr')]"
        ele_loc_text = self.find_element(loc_text)
        self.input_text(ele_loc_text, value)
        self.driver.switch_to_default_content()
        # 点击回复
        self.button.click_button("回复", parent_loc=parent_xpath)

    def commentUi_copy_richtext(self, parent_xpath="", **kwargs):
        '''
        复制评论
        '''
        loc = parent_xpath + f'//div[text()="复制"]'
        self.click_element(loc)

    def loc_comment(self, parent_xpath=""):
        '''获取评论显示路径'''
        loc = parent_xpath + f'//div[contains(@class,"ui-rich-text-cke-readonly")]'
        return loc

    def commentUi_get_commentText(self, parent_xpath="", **kwargs):
        '''
        获取某条评论的评论内容
        '''
        text = self.get_element_text(self.loc_comment(parent_xpath))
        return text

    def commentUi_get_commentTextAll(self, parent_xpath="", **kwargs):
        '''
        获取所有评论的评论内容
        '''
        text_list = self.get_elements_text(self.loc_comment(parent_xpath))
        return text_list

    def loc_desensitization(self, parent_xpath="", **kwargs):
        '''获取脱敏显示设置路径'''
        loc = parent_xpath + f'//span[text()="脱敏显示设置"]'
        return loc

    def commentUi_desensitization(self, parent_xpath="", **kwargs):
        '''
        脱敏显示设置
        '''
        #点击脱敏显示设置，展示详情
        self.click_element(self.loc_desensitization(parent_xpath))
        #开启脱敏显示
        self.switch.click_switch_button(True,parent_xpath)
        self.button.click_button("保存", parent_loc=parent_xpath)

    def commentUi_changeId(self, id, parent_xpath="", **kwargs):
        '''
        单条评论切换id
        :param idValue:要切换的评论id值
        '''
        #输入id
        loc = parent_xpath + f'[contains(@class,"ui-input")]'
        self.input_text(loc, id)
        #切换id
        self.button.click_button("切换id", parent_loc=parent_xpath)






