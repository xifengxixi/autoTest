from selenium.webdriver.common.by import By
from common.base import Page


class SelectUi(Page):
    """
    select下拉框组件
    select_button:下拉框单选选择数据
    select_buttons:下拉框多选选择数据
    """
    singleSelect_loc=f'//div[contains(@class,"ui-select is-single") or contains(@class,"ui-select is-opened is-single")]'
    selectOption_loc=f'//div[contains(@class,"ui-trigger-popupInter-container")]/div[not(contains(@class,"hidden"))]//*[contains(@class,"option")]'

    def select_button(self, data, parent_xpath="", **kwargs):
        '''
        下拉框单选选择数据
        :param data：下拉框的值，如："选项一"
        '''
        #点击下拉框 展示下拉框数据
        if 'sourceElement' in kwargs:
            kwargs["sourceElement"].find_element(*(By.XPATH, parent_xpath + self.singleSelect_loc)).click()
        else:
            loc = '(' + parent_xpath +  self.singleSelect_loc + ')' + f'[position()={kwargs.get("position", 1)}]'
            label_loc = f'{parent_xpath}//*[@class="ui-formItem-label-span"]'    # 存在填充表单,触发help气泡框,无法点击下一个表单字段,所以先移动鼠标悬停到字段label
            if self.is_element_exist(label_loc):
                self.move_on(label_loc)
            self.click_element(loc)
        # 选择值
        loc = self.selectOption_loc
        self.find_and_scroll_to_element(loc + f'//*[text()="{data}"]') # 选项过多时,需要滚动到选项
        self.click_element(loc + f'//*[text()="{data}"]')

    def select_button_by_class(self, data, parent_xpath="", **kwargs):
        '''
        下拉框单选通过class选择数据
        :param data：下拉框class的值，如："xxx"
        '''
        #点击下拉框 展示下拉框数据
        loc = '(' + parent_xpath +  self.singleSelect_loc + ')' + f'[position()={kwargs.get("position", 1)}]'
        self.move_on(loc) # 有时候下拉框会有气泡遮挡，需要先移动到下拉框上
        self.click_element(loc)
        # 选择值
        loc = self.selectOption_loc
        self.click_element(loc + f'//*[contains(@class,"{data}")]')

    def select_button_by_attri(self, data, attri='title', parent_xpath="", fuzzy=True, **kwargs):
        '''
        下拉框单选通过属性选择数据
        :param data: 属性值
        :param attri: 属性名
        :param parent_xpath:
        :param fuzzy: 是否模糊匹配
        :param kwargs:
        :return:
        '''
        #点击下拉框 展示下拉框数据
        loc = '(' + parent_xpath +  self.singleSelect_loc + ')' + f'[position()={kwargs.get("position", 1)}]'
        if self.is_element_exist(loc + '//span'):
            self.click_element(loc + '//span')
        else:
            self.click_element(loc)
        # 选择值
        loc = self.selectOption_loc
        option_loc = loc + f'//*[contains(@{attri},"{data}")]' if fuzzy else loc + f'//*[@{attri}="{data}"]'
        self.click_element(option_loc)

    def select_buttons(self, listData,selectType =True, parent_xpath="", **kwargs):
        '''
        下拉框多选选择数据
        :param  selectType:勾选或者不勾选，True or False
        :param  listData:列表形式，下拉框的值，如:["选项一", "选项二"]
        :return:
        '''
        #点击下拉框 展示下拉框数据
        # self.click_element(parent_xpath + f"(//div[contains(@class,'ui-select-input-wrap')])[7]")
        self.click_element(parent_xpath + f"//div[contains(@class,'ui-select-input-wrap')]")
        loc = "//div[contains(@class,'ui-trigger-popupInter-container')]/div[not(contains(@class, 'hidden'))]"
        #勾选多选选择值
        if selectType:
            for i in listData:
                i_ele = self.find_element(loc + f'//span[text()="{i}"]/ancestor::li')
                #判断是否已经被勾选
                if "is-active" not in i_ele.get_attribute("class"):
                    i_ele.click()
        #取消勾选多选选择值
        if not selectType:
            for j in listData:
                j_ele = self.find_element(loc + f'//span[text()="{j}"]/ancestor::li')
                # 判断是否已经被勾选，被勾选就再次点击取消勾选
                if "is-active"  in j_ele.get_attribute("class"):
                    j_ele.click()
        if kwargs.get('need_close'):
            self.click_element(parent_xpath + f"//div[contains(@class,'ui-select-input-wrap')]")

    def select_getText(self,parent_xpath="", **kwargs):
        '''
        获取单选下拉框的所有内容
        :param parent_xpath: 父级路径
        :param kwargs:
        :return: [value1，value2]
        '''
        # 单选框路径
        loc=parent_xpath+self.singleSelect_loc
        #选项路径
        loc2=self.selectOption_loc+f"//li"
        self.click_element(loc)#打开选择框
        text_list=self.get_elements_text(loc2)
        self.click_element(loc)#关闭选择框
        return text_list

    def select_getSelectText(self, parent_xpath="", **kwargs):
        '''
        获取选择框选择内容
        :param parent_xpath:
        :param kwargs:
        :return:
        '''
        # 单选框路径
        loc=parent_xpath+self.singleSelect_loc+f'//span[contains(@class,"input-selected")]'
        value = self.get_element_attribute(loc, "textContent")
        return value