from common.base import Page


class Steps(Page):
    """
    Steps步骤条组件
    steps_click_step: 点击步骤条上一步/下一步
    steps_click_by_index: 点击步骤条中第某个图标，index为图标索引位置
    """

    def steps_click_step(self, step_name="下一步", parent_xpath=""):
        """
        点击步骤条上一步/下一步
        """
        loc = parent_xpath + f"//button[contains(@class,'ui-btn')][contains(text(),'{step_name}')]"
        self.click_element(loc)

    def steps_click_by_index(self, index=0, parent_xpath=""):
        """
        点击步骤条中第某个图标
        """
        loc = parent_xpath + "//*[@class='ui-steps ui-steps-horizontal']//span[@class='ui-steps-icon']"
        eles = self.find_elements(loc)
        if len(eles) > index:
            # 执行js点击
            self.click_by_js(eles[index])
        else:
            raise Exception(f"当前定位中有{len(eles)}个元素，传入的索引位置为{index}")
