from common.base import Page


class TimelineUi(Page):
    """
    Timeline时间轴
    timeline_click_left：点击时间轴左侧元素
    timeline_click_content：点击时间轴右侧元素
    timeline_click_middle：点击时间轴中间节点
    timeline_get_text：获取时间轴的文本
    """

    def timeline_click_left(self, left_text, parent_xpath=""):
        """
        点击时间轴左侧元素（通过文本内容点击）
        :param left_text: 时间轴左侧文本
        :param parent_xpath:
        :return:
        """
        loc = '//div[contains(@class, "ui-timeline-item-content-left")]'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        if self.is_element_exist(ele_loc + '/*'):
            ele_loc = ele_loc + '/*'
        eles = self.find_elements(ele_loc)
        flag = True
        for ele in eles:
            if left_text in ele.text:
                self.scroll_into_view(ele)
                ele.click()
                flag = False
                break
        if flag:
            raise Exception("没有找到需要点击的时间轴左侧元素")

    def timeline_click_content(self, content_text, parent_xpath=""):
        """
        点击时间轴右侧元素（通过文本内容点击）
        :param content_text: 时间轴右侧文本
        :param parent_xpath:
        :return:
        """
        loc = '//div[contains(@class, "ui-timeline-item-content")]'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        if self.is_element_exist(ele_loc + '/*'):
            ele_loc = ele_loc + '/*'
        eles = self.find_elements(ele_loc)
        flag = True
        for ele in eles:
            if content_text in ele.text:
                self.scroll_into_view(ele)
                ele.click()
                flag = False
                break
        if flag:
            raise Exception("没有找到需要点击的时间轴右侧元素")

    def timeline_click_middle(self, index, parent_xpath=""):
        """
        点击时间轴中间节点
        :param index: 节点的index
        :param parent_xpath:
        :return:
        """
        loc = '//*[contains(@class, "ui-timeline-item") and not(contains(@class, "hide"))]' \
              '//*[contains(@class, "ui-timeline-item-content-middle")]'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        loc_target = f'({ele_loc}//*[contains(@class, "head")])[position()="{index}"]'
        self.click_element(loc_target)


    def timeline_get_text(self, index, content_type="left", parent_xpath=""):
        """
        获取时间轴的文本
            left: 获取时间轴左侧的文本
            middle: 获取时间轴中间的文本
            content: 获取时间轴右侧的文本
        :param index:
        :param content_type:
        :param parent_xpath: 
        :return: 
        """
        loc = '//*[contains(@class, "ui-timeline-item") and not(contains(@class, "hide"))]'
        ele_loc = parent_xpath + loc if parent_xpath else loc
        xpaths = {
            "left": '//*[@class="ui-timeline-item-content-left"]',
            "middle": '//*[@class="ui-timeline-item-content-middle"]',
            "content": '//*[@class="ui-timeline-item-content"]'
        }
        type_loc = xpaths.get(content_type)
        target_loc = f'({ele_loc}{type_loc})[position()="{index}"]'
        text = self.get_element_text(target_loc)
        return text