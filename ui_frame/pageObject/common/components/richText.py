from common.base import Page


class RichText(Page):
    """
    RichText富文本组件
    richText_input_value: 输入文本内容
    richText_get_value: 获取文本内容
    """

    def richText_input_value(self, value, iframe_xpath):
        """
        富文本：输入文本内容
        @param value: 输入内容
        @param iframe_xpath: iframe xpath定位
        @return:
        """
        ele = self.find_element(iframe_xpath)
        self.switch_frame(ele)
        iframe_loc = "//p"
        self.input(iframe_loc, value)
        self.switch_default_content()

    def richText_get_value(self, iframe_xpath):
        """
        富文本：获取文本内容
        @param iframe_xpath: iframe xpath定位
        @return:
        """
        ele = self.find_element(iframe_xpath)
        self.switch_frame(ele)
        iframe_loc = "//p"
        text = self.get_element_text(iframe_loc)
        self.switch_default_content()
        return text
