import autoit
import os
from common.base import Page
from ui_frame.config import UiConfig
from ui_frame.utils.log_util import logger


class Upload(Page):
    """
    Upload上传组件。文件存放在testdatas下，图片或视频文件存放在testdatas/image下
    upload_file: 上传文件：点击【上传文件】按钮上传
    upload_image: 上传图片：点击上传图片【+】号
    upload_file_by_drag 上传附件：点击【云状】图标
    upload_hover_and_click: hover已上传文件，点击选项
    upload_get_uploaded_file_name: 获取已上传文件的名称
    upload_file_by_loc: 点击指定元素上传文件
    """

    def __upload_system(self, filename, type="attr",test_dir=None):
        self.sleep(1)
        # autoit开始操作，焦点到文件名选择框
        if UiConfig.browser_type == "firefox":
            title = "文件上传"
        else:
            title = "打开"
        self.sleep(1)
        autoit.control_focus(title, "Edit1")
        self.sleep(1)
        if test_dir==None:
            # 当前目录
            test_dir = os.getcwd()
            test_dir = os.path.dirname(test_dir.split("autoTest")[0] + "autoTest\\ui_frame\\testData\\")
        if type == "attr":
            path = os.path.join(test_dir, filename)
        elif type == "pic" or type == 'video':
            path = os.path.join(test_dir + "\\image", filename)
        # 选择一个文件
        autoit.control_set_text(title, "Edit1", path)
        # 点击打开按钮
        self.sleep(2)
        autoit.control_click(title, "Button1")
        for i in range(4):
            if self.is_upload_windows_exist():
                autoit.send("!{F4}")
                self.sleep(.5)
                if i == 3:
                    logger.error(f"文件上传失败！！！！！！！！请检查文件路径{path}")
                    raise Exception(f"文件上传失败！！！！！！！！请检查文件路径{path}")
        self.sleep(3)

    def is_upload_windows_exist(self):
        """
        判断上传文件窗口是否存在
        @return:
        """
        if UiConfig.browser_type == "firefox":
            title = "文件上传"
        else:
            title = "打开"
        return autoit.win_exists(title)

    def upload_file(self, filename, type="attr", parent_xpath="", only_parentXpath=False):
        """
        上传文件：点击【上传文件】按钮上传
        @param type:
        @param filename: 文件名称
        @param parent_xpath:
        @return:
        """
        loc = parent_xpath + "//button[contains(@class,'ui-upload-select-drag-btn')]"
        if only_parentXpath:
            loc = parent_xpath
        self.click_element(loc)
        self.sleep(0.5)
        self.__upload_system(filename, type)

    def upload_image(self, filename, parent_xpath="",only_parentXpath=False):
        """
        上传图片：点击上传图片【+】号
        @param filename: 文件名称
        @param parent_xpath:
        @return:
        """
        loc = parent_xpath + "//div[@class='ui-upload-select-box ui-upload-image-select-box']"
        if only_parentXpath:
            loc = parent_xpath
        self.click_element(loc)
        self.sleep(0.5)
        self.__upload_system(filename, "pic")

    def upload_file_by_drag(self, filename, type="attr", parent_xpath=""):
        """
        上传附件：点击【云状】图标
        @param filename: 文件名称
        @param parent_xpath:
        @return:
        """
        loc = parent_xpath + "//*[name()='svg' and contains(@class, 'ui-icon-lg ui-icon-svg Icon-upload01')]"
        # loc = parent_xpath + "//span[@class='ui-icon ui-icon-wrapper ui-upload-select-drag-area-icon' and ]"
        self.click_element(loc)
        self.sleep(0.5)
        self.__upload_system(filename, type)

    def upload_hover_and_click(self, filename, option_name, more_option_name="", parent_xpath=""):
        """
        hover已上传文件，点击选项
        @param filename: 已上传文件名称
        @param option_name: hover上的选项名称
        @param more_option_name: 更多中的选项名称
        @param parent_xpath:
        @return:
        """
        loc = parent_xpath + f"//div[@class='ui-list-body ui-list-body-noBorder']//a[@title='{filename}']"
        target_loc = f"//div[@class='ui-trigger-popupInner ui-upload-listT-item-tigger-popup']//span[text()='{option_name}']"
        self.move_on(loc)
        if not option_name == "更多":
            self.click_element(target_loc)
        else:
            if more_option_name:
                # hover 更多选项
                self.move_on(target_loc)
                self.sleep(0.5)
                # 点击更改中的选项
                loc = f"//div[@class='ui-trigger-popupInner ui-upload-listT-item-tigger-popup']//li//span[text()='{more_option_name}']"
                self.click_element(loc)
            else:
                raise Exception("请输入更多按钮中的选项名称")

    def upload_get_uploaded_file_name(self) -> list:
        """
        获取已上传文件的名称
        @return:
        """
        loc = "//div[contains(@class,'ui-upload-list')]//a"
        text = []
        eles = self.find_elements(loc)
        for e in eles:
            text.append(e.get_attribute("title"))
        return text

    def ecode_upload_file(self, filename,type="attr", test_dir=None):
        """
        ecode导入文件：点击【点击上传】按钮
        @param filename: 文件名称
        @param parent_xpath:
        @return:
        """
        loc=f'//button[contains(@class,"ui-upload")]'
        self.find_element(loc).click()
        # self.click_button_to_span('点击上传')
        self.sleep(0.5)
        self.__upload_system(filename, type=type,test_dir=test_dir)

    def upload_file_by_cloudAndText(self, filename, type="attr", parent_xpath=""):
        """
        上传附件：点击【云状带文字】图标
        @param filename: 文件名称
        @param parent_xpath:
        @return:
        """
        loc = parent_xpath + "//span[@class='ui-icon ui-icon-wrapper uplaod-icon']"
        self.click_element(loc)
        self.sleep(0.5)
        self.__upload_system(filename, type)

    def upload_file_by_loc(self, loc, filename, type="attr", test_dir=None, parent_xpath=''):
        """
        点击指定元素上传文件
        :param loc:
        :param filename:
        :param type:
        :param test_dir:
        :param parent_xpath:
        :return:
        """
        self.click_element(f'{parent_xpath}{loc}')
        self.sleep(0.5)
        self.__upload_system(filename, type, test_dir)