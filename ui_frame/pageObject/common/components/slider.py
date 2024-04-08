from common.base import Page
from . import inputUi


class Slider(Page):
    """
    滑块/进度条操作
    slider_get_handle_value：获取滑块进度条的值
    slider_set_handle_value：将滑块进度条设置指定值
    slider_is_disabled：滑块是否禁用
    slider_is_readOnly：滑块是否只读
    slider_handle_input_value：滑块输入框输入值（滑块进度条相应改变值）
    slider_get_input_value：获取滑块输入框的值
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.inputUi = inputUi.InputUi(driver)

    def __get_slider_handle_loc(self,parent_xpath=""):
        """ 获取滑块句柄定位 """
        return parent_xpath + "//div[@class='ui-slider-handle']"

    def __get_slider_loc(self,parent_xpath=""):
        """ 获取滑块组件定位 """
        return self.__get_slider_handle_loc(parent_xpath) + "/.."

    def __get_slider_spot_loc(self,parent_xpath=""):
        """ 获取滑块节点值定位 """
        return parent_xpath + "//span[contains(@class,'ui-slider-dot')]"

    def slider_get_handle_value(self,parent_xpath=""):
        """
        获取滑块进度条的值
        """
        loc = self.__get_slider_handle_loc(parent_xpath)
        value = self.get_element_attribute(loc,"aria-valuenow")
        return int(value)

    def slider_set_handle_value(self,value,dragable=True,parent_xpath=""):
        """
        将滑块进度条设置指定值
        :param dragable: dragable为True时，为普通滑块，可拖拽到相应值；dragable为flase时，为步长滑块，点击步长节点赋值
        :param value: 0-100（输入int数据）
        """
        if dragable:
            loc = self.__get_slider_handle_loc(parent_xpath)
            ele = self.find_element(loc)
            while value !=  self.slider_get_handle_value():
                drag_value = value - self.slider_get_handle_value()  # 需要拖拽的值
                offsetWidth = self.get_element_attribute(self.__get_slider_loc(), "offsetWidth")
                need_offset = float(drag_value) * float(offsetWidth) / 100  # 需要拖拽的坐标值
                self.drag_by_pyautogui_offset(ele, x_value=need_offset, x_offset=7.5, y_offset=8,duration=1)
        else:
            loc = self.__get_slider_spot_loc(parent_xpath)
            eles =self.find_elements(loc)
            for el in eles:
                if str(value) in el.get_attribute("style"):
                    el.click()

    def slider_is_disabled(self,parent_xpath=""):
        """
        滑块是否禁用
        """
        loc = self.__get_slider_loc(parent_xpath)
        return self.check_elem_attribute(self.find_element(loc),"ui-slider-disabled")

    def slider_is_readOnly(self,parent_xpath=""):
        """
        滑块是否只读
        """
        loc = self.__get_slider_loc(parent_xpath)
        return self.check_elem_attribute(self.find_element(loc),"ui-slider-readOnly")

    def slider_handle_input_value(self,value,parent_xpath=""):
        """
        滑块输入框输入值（滑块进度条相应改变值）
        :param value:输入的值-int型
        """
        loc = self.__get_slider_handle_loc(parent_xpath) + "/ancestor::div[@class='ui-layout-row']"
        self.inputUi.input_text_ui(value,parent_xpath=loc)

    def slider_get_input_value(self,parent_xpath=""):
        """
        获取滑块输入框的值
        """
        loc = self.__get_slider_handle_loc(parent_xpath) + "/ancestor::div[@class='ui-layout-row']//input"
        if self.get_element_attribute(loc,"value"):
            return self.get_element_attribute(loc,"value")
