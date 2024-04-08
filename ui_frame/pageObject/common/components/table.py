from time import sleep
from common.base import Page
from . import icon


class Table(Page):
    '''
    table_current_td_click 点击单元格
    table_row_select_all_status 所有行（全选框）选择状态
    table_row_select_all 选择所有行（全选框）
    table_row_select_single_status 当前行选择状态
    table_row_select 选择当前行（或多行）
    table_row_more_menue_click 点击当前行更多菜单
    table_data_assert_line 对table数据进行验证 按列进行验证
    table_data_assert_row 对table数据进行验证,获取所有数据，按行校验
    table_empty_text 获取表格空数据时显示提示
    table_loading_more_click 点击加载更多（在设置次数内点击加载更多，直到加载更多消失或到达设置次数）
    table_isLoadingStatus 判断Table是都正在加载数据
    table_lion_value 获取所有列名
    table_select_row 按照指定行选取数据
    table_selectByCell_content 选择框选择：按照单元格内容以及列名选择
    table_row_drag 根据拖拽对象所在行拖拽到目标所在行
    table_contentByCoordinate 指定单元格，根据其坐标返回列以及对应的单元格数据
    check_table_datas 校验表格数据
    '''

    def __init__(self, driver):
        super().__init__(driver)
        self.icon = icon.Icon(driver)

    #table td Xpath
    table_td_loc=f'//td[contains(@class,"ui-tabl")]'
    # 列路径
    th_loc = f'//th'
    # 行路径
    tr_loc = f'//tbody/tr'

    # ------ table 指定行指定列 -------#
    def table_current_td_loc(self,title_value,parent_xpath='',**kwargs):
        '''
        获取单元格路径
        :param title_value: 单元格title名称（一般来说是单元格内容）
        :param parent_xpath: 父级路径
        :return: 单元格路径
        '''
        table_current_td_loc = self.table_td_loc + f'//*[contains(@title,"{title_value}")]'
        table_current_td_loc = parent_xpath + table_current_td_loc
        return table_current_td_loc

    def table_current_td_ele(self,title_value,parent_xpath='',**kwargs):
        '''
        获取单元格元素
        :param title_value: 单元格title名称（一般来说是单元格内容）
        :param parent_xpath: 父级路径
        :return: 单元格元素
        '''
        loc=self.table_current_td_loc(title_value,parent_xpath)
        ele=self.find_element(loc)
        return ele

    def table_current_td_click(self,title_value,parent_xpath='',**kwargs):
        '''
        点击单元格
        :param title_value: 单元格title名称（一般来说是单元格内容）
        :param parent_xpath: 父级路径
        '''
        ele=self.table_current_td_ele(title_value,parent_xpath)
        ele.click()

    # ------ table 选择所有 -------#
    def table_row_select_all_loc(self,parent_xpath='',**kwargs):
        '''
        获取选中所有选择框（全选框）路径
        :param parent_xpath: 父级路径
        '''
        loc = f'//th//span[contains(@class,"ui-checkbox-left")]'
        loc = parent_xpath + loc
        return loc

    def table_row_select_all_ele(self,parent_xpath='',**kwargs):
        '''
        选择所有行（全选框）元素
        :param parent_xpath: 父级路径
        '''
        loc = self.table_row_select_all_loc(parent_xpath)
        ele = self.find_element(loc)
        return ele

    def table_row_select_all_status(self,parent_xpath='',**kwargs):
        '''
        所有行（全选框）选择状态
        :param parent_xpath: 父级路径
        :return: status True:选择所有框被选中 False:选择所有框没有被选中
        '''
        ele=self.table_row_select_all_ele(parent_xpath)
        status = self.check_elem_attribute(ele, "checked")
        return status,ele

    def table_row_select_all(self,isSelect=True,parent_xpath='',**kwargs):
        '''选择所有行（全选框）
        :param isSelect选择所有行  :True 表示需要选中所有行（默认选中）   False 表示取消选中所有行
        '''
        res=self.table_row_select_all_status(parent_xpath)
        status=res[0]
        ele=res[1]
        if isSelect !=status:
           ele.click()

    # ------ table 当前行 -------#
    def table_current_row_loc(self, title_value, parent_xpath='',**kwargs):
        '''
        获取当前行路径
        :param title_value: 单元格title名称（一般是单元格内容）
        :param parent_xpath: 父级路径
        :return:
        '''
        table_current_td_loc = self.table_current_td_loc(title_value)
        table_current_row_loc = table_current_td_loc + f'/ancestor::tr'
        table_current_row_loc = parent_xpath + table_current_row_loc
        return table_current_row_loc

    def table_row_loc_by_row_num(self, row_num, parent_xpath='',**kwargs):
        '''
        根据行号获取行元素定位
        :param row_num: 第几行,1代表第一行,以此类推;-1代表倒数第一行
        :param parent_xpath: 父级路径
        :return:
        '''
        table_row_loc = parent_xpath + self.tr_loc
        row_count = self.get_element_count(table_row_loc)
        if row_count == 0:
            raise ValueError(f"页面行数为0!")
        if abs(row_num) > row_count:
            raise ValueError(f"选择的行号{row_num}大于页面行数{row_count}")
        if row_num < 0:  # 负索引需要行号倒置
            row_num = row_count + 1 + row_num
        return table_row_loc + f'[{row_num}]'

    def table_current_row_all_data(self, title_value, parent_xpath='',**kwargs):
        '''
        获取当前行所有内容信息
        :param title_value: 单元格title名称（一般是单元格内容）
        :param parent_xpath: 父级路径
        :return:
        '''
        table_current_row_loc = self.table_current_row_loc(title_value, parent_xpath)
        new_loc = table_current_row_loc + f'//span[@title]'
        eles = self.find_elements(new_loc)
        title_value_list = [ele.get_attribute("textContent") for ele in eles]
        return title_value_list

    def table_row_select_single_status(self,title_value,parent_xpath='',**kwargs):
        '''
        当前行选择状态
        :param title_value: 单元格title名称（一般是单元格内容）
        :param parent_xpath: 父级路径
        :return: status True:当前行选择框被选中 False:当前行选择框没有被选中
        '''
        table_current_row_loc = self.table_current_row_loc(title_value, parent_xpath)
        loc=table_current_row_loc + f'//input'
        new_loc = loc+ f'/..'
        ele=self.find_element(new_loc)
        status = self.check_elem_attribute(ele, "checked")
        return status,loc,table_current_row_loc

    def table_row_isselect_status(self,title_value,parent_xpath='',**kwargs):
        '''
        当前行是否可以选择
        :param title_value: 单元格title名称（一般是单元格内容）
        :param parent_xpath: 父级路径
        :return: status True:当前行选择框禁用不可以选中 False:当前行选择框可以被选择
        '''
        table_current_row_loc = self.table_current_row_loc(title_value, parent_xpath)
        loc=table_current_row_loc + f'//input'
        new_loc = loc+ f'/..'
        ele=self.find_element(new_loc)
        status = self.check_elem_attribute(ele, "disabled")
        return status,loc,table_current_row_loc

    def table_row_select(self,title_List,isSelect=True,isShow=False,parent_xpath='',**kwargs):
        '''
        选择当前行（或多行）
        :param title_List: 单元格title名称（一般是单元格内容）[]
        :param isSelect: 选择当前行  :True 表示当前行需要选中（默认选中）   False 表示取消选中当前行
        :param isShow: 是否显示选择框（不显示选择框的场景如：以序号代替，鼠标悬浮在指定行才会显示选择框）True不显示 False显示
        :param parent_xpath: 父级路径
        :return:
        '''
        for title in title_List:
            res=self.table_row_select_single_status(title,parent_xpath)
            status = res[0]
            loc = res[1]
            table_current_row_loc=res[2]
            if isSelect != status:
                if isShow:
                    self.move_on(table_current_row_loc)
                self.click_element(loc)

    #------ table 更多菜单 -------#
    def table_row_more_menue_loc(self,title_value,parent_xpath='',**kwargs):
        '''
        获取当前行更多菜单路径
        :param title_value: 单元格title名称（一般是单元格内容）
        :param parent_xpath: 父级路径
        :return:
        '''
        table_current_row_loc = self.table_current_row_loc(title_value)
        table_current_more_loc = table_current_row_loc + f'//span[contains(@class,"ui-icon")]'
        table_current_more_loc = parent_xpath + table_current_more_loc
        return table_current_more_loc

    def table_row_more_menue_click(self,menue_name,title_value,parent_xpath='',**kwargs):
        '''
        点击当前行更多菜单
        :param menue_name: 菜单名称
        :param title_value: 单元格title名称（一般是单元格内容）
        :param parent_xpath: 父级路径
        :return:
        '''
        table_current_more_loc=self.table_row_more_menue_loc(title_value,parent_xpath)
        loc=f"//span[text()='{menue_name}']"
        if kwargs.get('trigger_loc'):
            loc = kwargs.get('trigger_loc') + loc
        self.move_on(table_current_more_loc)
        #更多三个点的路径
        loc2 = table_current_more_loc + f"//*[contains(@class,'Icon-more02')]"
        # self.click_icon_by_class("Icon-more02", table_current_more_loc)
        self.move_on(loc2)
        self.sleep(1)
        self.click_element_retry(loc)

    def get_table_row_more_menu(self,title_value,parent_xpath=''):
        '''
        获取当前行更多菜单
        :param title_value: 单元格title名称（一般是单元格内容）
        :param parent_xpath: 父级路径
        :return:
        '''
        table_current_more_loc=self.table_row_more_menue_loc(title_value,parent_xpath)
        self.move_on(table_current_more_loc)
        #更多三个点的路径
        loc2 = table_current_more_loc + f"//*[contains(@class,'Icon-more02')]"
        self.move_on(loc2)
        table_row_more_menu = self.get_elements_text('//div[@class="ui-trigger-popupInner"]//span[@class="ui-menu-list-item-content "]')
        return table_row_more_menu

    # ------ table 数据验证 -------#
    def table_data_assert_line(self,data,exdata,parent_xpath='',**kwargs):
        '''
        对table数据进行验证 按列进行验证
        :param data: data={
            "姓名": ["张天逸", "彭浩秋"],"联系方式": ["15199398787", "16179993456"],"部门": ["泛微-北方大区", "设计师"],
            "上级": ["王紫博", "张华"],"多行文本": ["设计师", "设计师"],"入职时间": ["2021-06-23", "2021-08-21"],
        }检验的数据：key:列名  value：对应的列值
        :param exdata: 期望校验的数据 例如：exdata=data['姓名']
        :param parent_xpath: 父级路径
        '''
        # 指定行路径
        locs = [self.table_current_row_loc(title, parent_xpath) for title in exdata]
        #获取列path
        for k,v in data.items():
            th_loc=parent_xpath+f'//th[text()="{k}"]'
            path=int(self.get_element_attribute(th_loc,'path'))
            exvalue=[self.get_element_attribute(loc+f'/td[{path + 1}]',"textContent") for loc in locs]
            assert v==exvalue,f'指定{k}列，预期值{v}不等于实际值{exvalue},'

    def table_data_assert_row(self,data,parent_xpath='',isAssert=True,**kwargs):
        '''
        对table数据进行验证,获取所有数据，按行校验
        :param data: data=[{"姓名":"张天逸","联系方式":"15199398787","部门":"泛微-北方大区","上级":"王紫博","多行文本":"设计师","入职时间":"2021-06-23"},
              {"姓名": "彭浩秋","联系方式": "16179993456","部门": "设计师","上级": "张华","多行文本": "设计师","入职时间": "2021-08-21"}
              ]
              按照表格传入预期验证的数据，key:列名  value：指定行对应的列值
        :param parent_xpath: 父级路径
        :return:
        '''
        tr_loc=parent_xpath+self.tr_loc#行路径
        th_loc=parent_xpath+self.th_loc#列路径
        tr_ele=self.find_elements(tr_loc)
        path_data={k:(int(self.get_element_attribute(th_loc+f'[text()="{k}"or @title="{k}"]', 'path')))+1 for k,v in data[0].items()}
        tr_locs=[tr_loc+f'[{tr_ele.index(i) + 1}]' for i in tr_ele]
        res_data=[{k:(self.get_element_attribute(loc+f'/td[contains(@class,"ui-tabl")][{v}]//span','textContent')).strip() for k,v in path_data.items()} for loc in tr_locs]
        error_data=[f'表格数据验证：预期数据{i}不在实际列表中{res_data}' for i in data if i not in res_data]
        if isAssert:
            assert error_data==[],f'表格数据显示错误：{error_data}'
        return error_data

    def get_thead_texts(self,parent_xpath=""):
        """
        获取表头列表
        :param parent_xpath:
        :return:
        """
        head_th_loc = "//thead//tr//th"
        th_loc = parent_xpath + head_th_loc  # 表头路径
        list_head_col = self.get_elements_attribute(th_loc, "textContent")
        list_head_col = [i.strip() for i in list_head_col]
        return list_head_col

    def get_col_index(self,col_name,list_head_col):
        """
        获取表格列序号
        :param col_name: 列名
        :param list_head_col: 表头文字列表，可从get_thead_texts获取
        :return:
        """
        # 获取表格列序号
        assert col_name in list_head_col,f"列名找不到{col_name},页面获取数据：{list_head_col}"
        return list_head_col.index(col_name)+1 # 元素的第几个是从1开始的，需要列表下标+1


    def get_table_data(self,list_col,parent_xpath=''):
        """
        获取表格数据
        :param list_col: 指定列名
        :param parent_xpath:
        :return:
        """
        # 获取表格列名
        head_th_loc = "//thead//tr//th"
        th_loc = parent_xpath + head_th_loc  # 表头路径
        list_head_col = self.get_elements_attribute(th_loc,"textContent")
        list_head_col = [i.strip() for i in list_head_col]
        list_check = [i for i in list_col if i not in list_head_col]
        if list_check:
            raise ValueError(f"列名找不到{list_check},页面获取数据：{list_head_col}")
        dict_col = {list_head_col.index(col)+1:col for col in list_col}
        # 获取行数据
        table_row_loc = parent_xpath + self.tr_loc
        if not self.is_element_exist(table_row_loc):
            return []
        row_count = self.get_element_count(table_row_loc)
        if row_count<1:
            return []
        list_data = []
        for row in range(1,row_count+1):
            row_data = {"row":row}
            for col_index,col in dict_col.items():
                td_loc = parent_xpath+f"//tbody//tr[{row}]//td[{col_index}]"
                data = None
                if self.is_element_exist(f"{td_loc}//input[@type='text']"):
                    input_elems = self.find_elements(f"{td_loc}//input")
                    data = []
                    for ele in input_elems:
                        data.append(ele.get_attribute("value").strip())
                    if len(data) == 1:
                        data = data[0]
                elif self.is_element_exist(f"{td_loc}//input[@type='checkbox']"):
                    checkbox_loc = f"{td_loc}//input[@type='checkbox']/ancestor::label"
                    is_check = self.check_elem_attribute(self.find_element(checkbox_loc), "checked")
                    data = is_check
                if data is None: # 如果没有数据，尝试获取textContent
                    data = self.get_element_attribute(td_loc, "textContent").strip()
                row_data[col] = data
            list_data.append(row_data)
        return list_data

    def check_table_datas(self, list_dict_check,parent_xpath='',match_type=2):
        """
        校验表格数据
        :param list_dict_check: 校验数据列表，每个字典代表一行数据,列名对应列值，第一个列表的key作为获取表格数据的表头，必须最全面否则可能失败
                                例[{"姓名":"张天逸","联系方式":"15199398787","部门":"泛微-北方大区"}]
        :param parent_xpath:
        :return:
        """
        list_col = list_dict_check[0].keys()
        list_table_data = self.get_table_data(list_col,parent_xpath)
        if match_type == 1:
            error_msg = "校验相同的列表长度不一致：输入值：{}，长度{}；校验值：{}，长度{}".format(list_table_data,len(list_table_data),
                                                                                    list_dict_check,len(list_dict_check))
            assert len(list_table_data) == len(list_dict_check), error_msg
        result, msg = self.is_data_contain(list_table_data, list_dict_check)
        assert result, f"数据校验失败：{msg}，期望值{list_dict_check}，实际值{list_table_data}"

    def check_table_datas_not_exist(self, list_dict_check, parent_xpath=''):
        """
        校验表格数据不存在
        :param list_dict_check: 校验数据列表，每个字典代表一行数据,列名对应列值，第一个列表的key作为获取表格数据的表头，必须最全面否则可能失败
                                例[{"姓名":"张天逸","联系方式":"15199398787","部门":"泛微-北方大区"}]
        :param parent_xpath:
        :return:
        """
        list_col = list_dict_check[0].keys()
        list_table_data = self.get_table_data(list_col,parent_xpath)
        all_result = True
        all_msg = f"表格获取数据{list_table_data},"
        for dict_check in list_dict_check:
            result, msg = self.is_data_contain(list_table_data, [dict_check])
            if result:
                all_result = False
                all_msg += f"校验数据{dict_check}不存在失败"
        assert all_result, all_msg

    def serch_table_data(self, dict_serch,list_col, parent_xpath=''):
        """
        根据给定的数据获取表格数据
        例如{"姓名":"张天逸"}获取整行{"row":1,"姓名":"张天逸","联系方式":"15199398787","部门":"泛微-北方大区"}
        可以通过这个获取到行号row
        :param dict_serch:匹配数据
        :param list_col:要查询的列名
        :param parent_xpath:
        :return:
        """
        list_table_data = self.get_table_data(list_col,parent_xpath)
        for row_data in list_table_data:
            result, data = self.is_data_contain(row_data, dict_serch)
            if result:
                return data
        assert False, f"表格数据不包含查找数据{dict_serch}!表格获取数据为：{list_table_data}"



    # ------ table 空数据 -------#
    def table_empty_loc(self,parent_xpath='',**kwargs):
        '''
        获取表格空数据状态路径
        :param parent_xpath: 父级路径
        :return:
        '''
        table_empty_loc = f'//div[@class="ui-table-grid-empty"]'
        table_empty_loc = parent_xpath + table_empty_loc
        return table_empty_loc

    def table_empty_text(self,parent_xpath='',**kwargs):
        '''
        获取表格空数据时显示提示
        :param parent_xpath: 父级路径
        :return:
        '''
        table_empty_loc = self.table_empty_loc(parent_xpath)
        value=self.get_element_attribute(table_empty_loc,"textContent")
        return value

    def table_empty_isEmpty(self,parent_xpath='',**kwargs):
        '''
        判断表格是否为空表格
        :param parent_xpath: 父级路径
        :return:True 是空表格  False 不是空表格
        '''
        table_loc =f'//div[contains(@class,"ui-spin-nested-loading")]//div[contains(@class,"ui-table-grid")]'
        table_loc = parent_xpath + table_loc
        status=False
        eles=self.find_elements(table_loc)
        for ele in eles:
            value = ele.get_attribute("class")
            if 'ui-table-grid-empty' in value:
                status = True
                break
        return status


    # ------ table 点击加载更多按钮 -------#
    def table_loading_more_loc(self,parent_xpath='',**kwargs):
        '''
        获取加载更多按钮路径
        :param parent_xpath: 父级路径
        :return:
        '''
        table_loading_more_loc = f'//div[contains(@class,"ui-table-grid-tfoot-more")]'
        table_loading_more_loc = parent_xpath + table_loading_more_loc
        return table_loading_more_loc

    def table_loading_more_click(self,hits=5,parent_xpath='',**kwargs):
        '''
        点击加载更多（在设置次数内点击加载更多，直到加载更多消失或到达设置次数）
        :param hits 点击次数
        :param parent_xpath: 父级路径
        :return:
        '''
        table_current_td_loc = self.table_loading_more_loc(parent_xpath)
        num=1
        while num<=hits:
            loading_value=self.get_element_attribute(table_current_td_loc,"textContent")
            if loading_value=="加载更多":
                self.click_element(table_current_td_loc)
                num = num + 1
                sleep(1)
            else:
                break

    # ------ table 加载状态 -------#
    def table_loadingStatus_loc(self,parent_xpath='',**kwargs):
        '''
        获取正在加载路径
        :param parent_xpath: 父级路径
        :return:
        '''
        table_loadingStatus_loc = f'//div[contains(@class,"loading-bottom")]'
        table_loadingStatus_loc = parent_xpath + table_loadingStatus_loc
        return table_loadingStatus_loc

    def table_isLoadingStatus(self,parent_xpath='',**kwargs):
        '''
        判断Table是都正在加载数据
        :param parent_xpath: 父级路径
        :return: ststus 加载状态存在状态 True正在加载中  False 数据不在加载中
        '''
        loc=self.table_loadingStatus_loc(parent_xpath)
        ststus=self.is_element_exist(loc)
        return ststus

    # ------ table 列名 -------#
    def table_lion_value(self, parent_xpath='',**kwargs):
        '''
        获取所有列名
        :param parent_xpath: 父级路径
        :return: [列名1，列名2]
        '''
        th_loc=parent_xpath+self.th_loc
        eles=self.find_elements(th_loc)
        lion_value = [ele.get_attribute("textContent")for ele in eles]
        return lion_value

    # ------ table 按照行列坐标对数据进行操作 -------#

    def select(self,ele,loc,isSelect,isShow,**kwargs):
        status = self.check_elem_attribute(ele, "checked")
        if isSelect != status:
            if isShow:
                self.move_on(loc)
            ele.click()

    def table_cells_value(self, parent_xpath='',**kwargs):
        '''
        获取所有单元格的内容及行列坐标
        :param parent_xpath: 父坐标
        :return: cells_coordinate:所有单元格的内容及行列坐标
                [{'列名':'单元格内容','coordinate'(#坐标): [行坐标, 纵坐标]}]
        '''
        th_loc=parent_xpath+self.th_loc #列路径
        tr_loc = parent_xpath + self.tr_loc  # 行路径
        try:
            tr_ele = self.find_elements(tr_loc)
        except:
            raise Exception(f"table获取数据失败！")
        eles=self.find_elements(th_loc)
        def attribute_value(ele,attribute="textContent"):
            value=ele.get_attribute(attribute)
            value = value.strip() if isinstance(value,str) else value
            value=(int(value))+1 if attribute=="rowindex" or attribute=="path" else value
            return value
        #列以及列坐标 {'序号': 1, '姓名': 2}
        pathData_dict={attribute_value(ele):attribute_value(ele,"path") for ele in eles}
        #所有td路径 以及坐标[行，列]
        trs_tds_locs=[{tr_loc + f'[{(int(ele.get_attribute("rowindex"))) + 1}]//td[contains(@class,"ui-tabl")][{lion_coor}]//span':[(tr_ele.index(ele))+1,lion_coor]} for ele in tr_ele for k,lion_coor in pathData_dict.items()]
        #获取所有单元格内容以及坐标[行，列][{'张天逸': [1, 2]}]
        td_values=[{attribute_value(self.find_element(loc)):coordinate} for res in trs_tds_locs for loc,coordinate in res.items()]
        #按照单元格内容列名以及坐标[{'列名':'单元格内容','coordinate'(#坐标): [行坐标, 纵坐标]}]
        cells_coordinate=[{lion_name:row_value,"coordinate":coordinate} for lion_name,lion_coor in pathData_dict.items() for cell in  td_values for row_value,coordinate in cell.items() if coordinate[1]==lion_coor]
        return cells_coordinate


    def table_select_row(self,rowNum,isContain=True,isSelect=True,isShow=False,parent_xpath='',**kwargs):
        '''
        按照指定行选取数据（例如：1、选中第二行 2、选择前三行 3、选择最后5行 4、选择倒数第二行  ）
        :param rowNum: 选择行数 3前三行，第三行 ,-3倒数第三行，最后三行
        :param isContain: 是否包含前面的行数 例如：rowNum=2 isContain=True：选择第一行第二行 isContain=False：选择第二行
        :param isSelect: 是否选中 True 需要选中 False 取消选中
        :param isShow: 是否显示选择框（不显示选择框的场景如：以序号代替，鼠标悬浮在指定行才会显示选择框）True显示 False不显示
        :param parent_xpath:父级路径
        '''
        tr_loc=parent_xpath+self.tr_loc
        contain=f'position()' if isContain else ''
        if isContain:
            contain = f'position()'
            if rowNum>0:
                contain = contain + f'<={rowNum}'
            else:
                contain = contain + f'> last(){rowNum}'
        else:
            if rowNum>0:
                contain = contain + f'{rowNum}'
            elif rowNum==-1:
                contain = contain + f'last()'
            else:
                contain = contain + f'last(){rowNum}'
        loc=tr_loc+f'[{contain}]//td//input/..'
        eles=self.find_elements(loc)
        for  ele in eles:
            self.select(ele,loc,isSelect,isShow)

    def table_selectByCell_content(self,cellContent,columnName=None,isSelect=True,isShow=False,parent_xpath='',**kwargs):
        '''
        选择框选择：按照单元格内容以及列名选择
        :param cellContent: 单元格名称
        :param columnName: 列名
        :param isSelect: 是否选中 True 需要选中 False 取消选中
        :param isShow: 是否显示选择框（不显示选择框的场景如：以序号代替，鼠标悬浮在指定行才会显示选择框）True显示 False不显示
        :param parent_xpath: 父级路径
        :return:
        '''
        #获取所有单元格内容及坐标
        tr_loc=parent_xpath+self.tr_loc
        cells_value=self.table_cells_value(parent_xpath)
        cell_list1=[res for res in cells_value for k,v in res.items() if cellContent==v]
        if columnName:
            cell_list1=[res for res in cell_list1 for k,v in res.items() if columnName==k]
        locs=[tr_loc+f'[{v[0]}]//td//input/ancestor::td' for res in cell_list1 for k,v in res.items() if k=="coordinate" ]
        for loc in locs:
            ele=self.find_element(loc)
            try:
                self.select(ele,loc,isSelect,isShow)
            except Exception as e:
                raise Exception(f"勾选表格复选框【{loc}】失败{e}")

    def table_contentByCoordinate(self,cells,cells_coordinate,**kwargs):
        '''
        指定单元格，根据其坐标返回列以及对应的单元格数据
        :param cells: 方法table_cells_value 返回的数据
        :param cells_coordinate: 方法table_cells_value 返回的数据的其中一项数据
        :return: [{'名称': ''}, {'列名': '内容'}]
        '''
        cells_coordinate = [i for i in cells if i.get('coordinate')[0] == cells_coordinate.get('coordinate')[0]]
        new_cells = [{k: v} for i in cells_coordinate for k, v in i.items() if k != "" and k != "coordinate"]
        return new_cells

    # ------ table 拖拽 -------#
    def table_row_drag(self,source_value,target_value,source_type="value",target_type="value",parent_xpath='',**kwargs):
        """
        根据拖拽对象所在行拖拽到目标所在行
        :param source_value: 拖拽对象
        :param target_value: 拖拽目标对象
        :param source_type: 拖拽对象类型,value:根据行内某个单元格值定位行;
                            row:根据行号定位行,此时source_value为第几行,1代表第一行,-1代表倒数第一行
        :param target_type:拖拽目标对象类型,同上
        :param parent_xpath:
        :param kwargs:
        :return:
        """
        if source_type == "value":
            table_source_row_loc = self.table_current_row_loc(source_value, parent_xpath)
        elif source_type == "row":
            table_source_row_loc = self.table_row_loc_by_row_num(source_value,parent_xpath)
        else:
            raise ValueError(f"拖拽行table_row_drag方法source_type参数({source_type})错误!")
        if target_type == "value":
            table_target_row_loc = self.table_current_row_loc(target_value, parent_xpath)
        elif target_type == "row":
            table_target_row_loc = self.table_row_loc_by_row_num(target_value,parent_xpath)
        else:
            raise ValueError(f"拖拽行table_row_drag方法target_type参数({target_type})错误!")
        self.icon.icon_drag_move_icon(self.icon.get_move_icon_loc(table_target_row_loc),table_source_row_loc)