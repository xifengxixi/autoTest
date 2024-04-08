from common.base import Page


class Form(Page):

    def form_input(self, lable, data, **kwargs):
        '''form-input框填充'''
        loc = kwargs.get("loc") if kwargs.get(
            "loc") else f"//*[text()='{lable}']/ancestor::div[contains(@class,'ui-formItem')]//input"
        if kwargs.get("form_pre"):
            loc = f"{kwargs.get('form_pre')}{loc}"
        input_eles = self.find_elements(loc)
        if isinstance(data, list):
            data = data
        else:
            data = [data]
        length = len(data) if len(data) < len(input_eles) else len(input_eles)
        for i in range(length):
            self.input_text(input_eles[i], data[i])

    def get_form_data(self, form_xpath, list_lable_name):
        '''
        获取表单数据
        :param form_xpath: 表单总的元素定位
        :param list_lable_name: 要获取的选项名称（待扩充，后续如果不传，考虑获取所有选项）
        :return: form_data,表单选项和选项值组成的字典
        '''
        form_data = {}
        # 判断form类型
        if self.is_element_exist(f"{form_xpath}//*[contains(@class,'ui-formItem-label-col')]"):
            item_sub = "ancestor::div[contains(@class,'ui-formItem-label-col')]/following-sibling::div"
        elif self.is_element_exist(f"{form_xpath}//*[contains(@class,'weapp-form-wrapper')]"):
            item_sub = "ancestor::div[contains(@class,'weapp-form-field')]//*[contains(@class,'weapp-form-widget-content')]"
        elif self.is_element_exist(f"{form_xpath}//*[contains(@class,'ui-layout-col')]"):
            item_sub = "ancestor::div[contains(@class,'ui-layout-col')]/following-sibling::div"
        else:
            raise Exception(f"获取表单失败：{form_xpath}下没找到表单元素！")
        # 遍历选项名称,获取选项值，存入字典
        for lable_name in list_lable_name:
            item_xpath = f"{form_xpath}//*[text()='{lable_name}']/{item_sub}"
            data = self.get_formItem_attribute(item_xpath)
            form_data[lable_name] = data
        return form_data

    def get_formItem_attribute(self, item_xpath):
        '''获取表单字段属性'''
        data=''
        if self.is_element_exist(f"{item_xpath}//input[@type='checkbox']",wait=0.1):
            checkbox_loc = f"{item_xpath}//input[@type='checkbox']/ancestor::label"
            is_check = self.check_elem_attribute(self.find_element(checkbox_loc), "checked")
            data = is_check
        elif self.is_element_exist(f"{item_xpath}//input[@type='radio']",wait=0.1):
            ele = self.find_element(f"{item_xpath}//input[@type='radio'][@checked]//ancestor::label")
            data = ele.get_attribute("title")
        elif self.is_element_exist(f"{item_xpath}//input",wait=0.1):
            input_elems = self.find_elements(f"{item_xpath}//input")
            data = []
            for ele in input_elems:
                data.append(ele.get_attribute("value").strip())
            if len(data) == 1:
                data = data[0]
        elif self.is_element_exist(f"{item_xpath}//textarea",wait=0.1):
            input_elems = self.find_elements(f"{item_xpath}//textarea")
            data = []
            for ele in input_elems:
                data.append(ele.get_attribute("textContent").strip())
            if len(data) == 1:
                data = data[0]
        elif self.is_element_exist(f"{item_xpath}//button",wait=0.1):
            ele = self.find_element(f"{item_xpath}//button")
            data = ele.get_attribute("aria-checked")
        if not isinstance(data, bool) and len(data) < 1:
            data = self.get_element_attribute(item_xpath, "textContent").strip()
        return data

    def get_formItem_many_values(self, form_xpath, dict_check):
        '''
        获取表单数据,支持单个字段获取多值情况
        :param form_xpath: 表单总的元素定位
        :return: dict_check,期望比对字典
        '''
        form_data = {}
        # 判断form类型
        if self.is_element_exist(f"{form_xpath}//*[contains(@class,'ui-formItem-label-col')]"):
            item_sub = "ancestor::div[contains(@class,'ui-formItem-label-col')]/following-sibling::div//div[@class='ui-formItem-wrapper']"
        elif self.is_element_exist(f"{form_xpath}//*[contains(@class,'weapp-form-wrapper')]"):
            item_sub = "ancestor::div[contains(@class,'weapp-form-field')]//*[contains(@class,'weapp-form-widget-content')]"
        elif self.is_element_exist(f"{form_xpath}//*[contains(@class,'ui-layout-col') and contains(@class,'label')]"):
            item_sub = "ancestor::div[contains(@class,'ui-layout-col') and contains(@class,'label')]/following-sibling::div"
        else:
            raise Exception(f"获取表单失败：{form_xpath}下没找到表单元素！")
        # 遍历选项名称,获取选项值，存入字典
        for lable_name,label_value in dict_check.items():
            item_xpaths = []
            if isinstance(label_value,list):  # 字段期望值存在多个
                for item in label_value:
                    position = item.get("position")
                    isContains = item.get("isContains", False)
                    if isContains:
                        xpath = f"({form_xpath}//*[contains(text(),'{lable_name}')]/{item_sub})[{position}]"
                    else:
                        xpath = f"({form_xpath}//*[text()='{lable_name}']/{item_sub})[{position}]"
                    item_xpaths.append(xpath)
            elif isinstance(label_value,dict):
                    isContains = label_value.get("isContains", False)
                    if isContains:
                        xpath = f"({form_xpath}//*[contains(text(),'{lable_name}')]/{item_sub})"
                    else:
                        xpath = f"({form_xpath}//*[text()='{lable_name}']/{item_sub})"
                    item_xpaths.append(xpath)
            else:
                item_xpaths.append(f"{form_xpath}//*[text()='{lable_name}']/{item_sub}")
            datas=[]
            for item_xpath in item_xpaths:
                data = self.get_formItem_attribute(item_xpath)
                datas.append(data)
            update_dict = lambda d, k, v: (d.update({k: v}),d)[1]
            form_data[lable_name] = [update_dict(label, "value", data) for label, data in zip(label_value, datas)] if isinstance(label_value, list) else data
        return form_data

    def check_form_data(self, dict_check, form_xpath):
        '''校验表单数据'''
        list_label = dict_check.keys()
        form_data = self.get_form_data(form_xpath, list_label)
        result, msg = self.is_data_contain(form_data, dict_check)
        assert result, msg

    def check_formItems_many_values(self, dict_check, form_xpath):
        '''校验表单数据,支持单字段多值'''
        form_data = self.get_formItem_many_values(form_xpath, dict_check)
        result, msg = self.is_data_contain(form_data, dict_check)
        assert result, msg

    def form_parent_xpath(self, fieldName, item_type='ui-layout-row', parent_xpath='', time_out=3):
        """
        准备表单parent_xpath
        :param fieldName: 表单列名
        :param item_type: 字段行的class名
        :param parent_xpath:
        :param time_out:
        :return:
        """
        loc = f'{parent_xpath}//*[contains(text(),"{fieldName}")]/ancestor::div[contains(@class,"{item_type}")]'
        if not self.is_element_exist(loc, time_out):
            loc = f'{parent_xpath}//*[contains(@title,"{fieldName}")]/ancestor::div[contains(@class,"{item_type}")]'
        return loc