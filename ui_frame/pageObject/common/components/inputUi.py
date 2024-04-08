from time import sleep
from selenium.webdriver.common.keys import Keys
from ui_frame.utils.log_util import logger
from common.base import Page


class InputUi(Page):
    """
    input文本框输入
    input_text_ui:文本框输入内容
    input_textarea 多文本框输入内容
    input_text_get 文本框内容获取
    input_textarea_get 多文本框内容获取
    """

    def input_text_ui(self, text, needClearText=True, parent_xpath="", **kwargs):
        '''
        文本框输入内容
        :param text:需要输入的数据
        :param needClearText:是否需要清除数据
        '''
        loc = parent_xpath + f"//input[contains(@class,'ui-input')]"
        element = self.find_element(loc)
        self.input_text(element,text,needClearText, **kwargs)

    def input_textarea(self, text, needClearText=True, parent_xpath="", **kwargs):
        '''
        多文本框输入内容
        :param text:需要输入的数据
        :param needClearText:是否需要清除数据
        '''
        loc = parent_xpath + f'//textarea[contains(@class,"ui-textarea")]'
        element = self.find_element(loc)
        self.input_text(element,text, needClearText, **kwargs)

    def input_text_get(self,parent_xpath="", **kwargs):
        '''
        文本框内容获取
        '''
        loc = parent_xpath + f"//input[contains(@class,'ui-input')]"
        if kwargs.get("attribute_name"):
            value = self.get_element_attribute(loc, kwargs['attribute_name'])
        else:
            value = self.get_element_attribute(loc, "textContent")
        return value

    def input_textarea_get(self,parent_xpath="", **kwargs):
        '''
        多文本框内容获取
        '''
        loc = parent_xpath + f'//textarea[contains(@class,"ui-textarea")]'
        value=self.get_element_attribute(loc,"textContent")
        return value

    def input_search_advanced(self,select_value,parent_xpath=""):
        """
        搜索框快捷输入并回车
        :param select_value:
        :param parent_xpath:
        :return:
        """
        search_input = parent_xpath+"//*[contains(@class,'ui-searchAdvanced-input')]//input"
        self.input_and_enter(search_input, select_value)
        self.sleep(1)

    def input_search(self, select_value, xpath, parent_xpath=""):
        """
        搜索框输入并回车
        :param select_value:
        :param xpath:
        :param parent_xpath:
        :return:
        """
        search_input = parent_xpath+xpath
        self.input_and_enter(search_input, select_value)
        self.sleep(1)

    def input_and_click(self, loc, value, enter_loc, needClearText = True):
        '''
        根据loc输入文本信息并点击回车
        :param loc:
        :param value:
        :param needClearText:
        :return:
        '''
        try:
            ele = self.find_element(loc)
            if needClearText:
                self.clear_element(ele)
            ele.send_keys(value)
            self.click_element(enter_loc)  # 点击回车
            self.click_element(enter_loc)  # 点击回车
            logger.info(f"输入文本信息：{value}")
        except Exception as e:
            logger.error(f"输入文本信息失败：{value}:{e}")
            raise Exception(f"输入文本信息失败：{value}！")

    def input_textarea_new(self, text, needClearText=True, parent_xpath="", **kwargs):
        '''
        多文本框输入内容
        :param text:需要输入的数据
        :param needClearText:是否需要清除数据
        '''
        loc = parent_xpath + f'//textarea[contains(@class,"ui-textarea")]'
        ele = self.find_element(loc)
        if needClearText:
            self.clear_element(ele)
        ele.send_keys(text)
        if "single_input" in kwargs:
            ele = self.find_element(loc)
            if ele.text != text:
                self.clear_element(ele)
                for key in text:
                    ele = self.find_element(loc)
                    ele.send_keys(key)
                    self.sleep(0.05)

    def input_clear_text_ui(self, text, needClearText=True, parent_xpath="", **kwargs):
        '''
        清空文本框并输入内容
        :param text:需要输入的数据
        :param needClearText:是否需要清除数据
        '''
        loc = parent_xpath + f"//input"
        if needClearText:
            #先清除已有数据
            self.find_element(loc).click()
            self.find_element(loc).send_keys(Keys.CONTROL, 'a')
            sleep(0.05)
            self.find_element(loc).send_keys(Keys.DELETE)
        #数据填充
        self.input(loc, text)

    def input_text_cls(self, text, needClearText=True, parent_xpath="", **kwargs):
        '''
        清空文本框并输入内容
        :param text:需要输入的数据
        :param needClearText:是否需要清除数据
        '''
        loc = parent_xpath + f"//input"
        if needClearText:
            self.find_element(loc).click()
            self.find_element(loc).send_keys(Keys.CONTROL, 'a')
            sleep(0.05)
        #数据填充
        self.input(loc, text)