import time
from common.base import Page


class Tips(Page):

    def get_tipInfo(self):
        '''获取提示信息内容'''
        if self.is_element_exist('//div[@class="ui-message-content"]'):
            eles = self.find_elements(('//div[@class="ui-message-body"]'))
            tipInfo = []
            for ele in eles:
                tipInfo.append(ele.get_attribute('textContent'))
            return tipInfo
        else:
            return None

    def check_tips_content(self, tip_content, time_out=3,check_type=1):
        '''
        在time_out时间内，是否出现相应的提示信息
        check_type：精确匹配:1;模糊匹配:2
        '''
        init_time = time.time()
        while time.time() - init_time < int(time_out):
            text = self.get_tipInfo()
            if text:
                if tip_content in text:  #精确匹配
                    return True, ""
                elif check_type == 2:  #模糊匹配
                    for i in text:
                        if i.find(tip_content)>-1:
                            return True, ""
                else:
                    assert False, f"检测到其他提示信息，内容为{text}"
            time.sleep(0.2)
        assert False, "未检测到提示信息"

    def close_all_tips(self):
        '''关闭所有提示信息'''
        loc = '//*[contains(@class,"ui-message")]//*[name()="svg" and contains(@class, "Icon-solid")]'
        if self.is_element_exist(loc):
            elems = self.find_elements(loc)
            for elem in elems:
                elem.click()
                self.sleep(.5)

    def get_tipInfo_h5(self):
        '''获取提示信息内容'''
        if self.is_element_exist('//div[@class="ui-m-toast-content"]'):
            eles = self.find_elements(('//div[@class="ui-m-toast-body"]'))
            tipInfo = []
            for ele in eles:
                tipInfo.append(ele.get_attribute('textContent'))
            return tipInfo
        else:
            return None

    def check_tips_content_h5(self, tip_content, time_out=3, check_type=1):
        '''
        在time_out时间内，是否出现相应的提示信息
        check_type：精确匹配:1;模糊匹配:2
        '''
        init_time = time.time()
        while time.time() - init_time < int(time_out):
            text = self.get_tipInfo_h5()
            if text:
                if tip_content in text:  #精确匹配
                    return True, ""
                elif check_type == 2:  #模糊匹配
                    for i in text:
                        if i.find(tip_content)>-1:
                            return True, ""
                else:
                    assert False, f"检测到其他提示信息，内容为{text}"
            time.sleep(0.2)
        assert False, "未检测到提示信息"