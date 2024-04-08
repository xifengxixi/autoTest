from common.base import Page
from . import table, button, dialog, icon, menu

class Batchoperator(Page):
    '''
    batchoperator_procedure 批量操作过程（打开批量操作弹窗,或通过快捷搜索选择筛选数据，点击全选，点击批量操作）
    batchoperator_assert 批量操作页面校验
    '''

    def __init__(self, driver):
        super().__init__(driver)
        self.table = table.Table(driver)
        self.button = button.Button(driver)
        self.dialog = dialog.Dialog(driver)
        self.icon = icon.Icon(driver)
        self.menu = menu.Menu(driver)

    def batchoperator_title_assert(self,title_name,parent_xpath='',**kwargs):
        '''
        校验批量操作弹窗标题是否正确
        :param parent_xpath:
        :return:
        '''
        error_list=[]
        title = self.dialog.dialog_get_dialog_title(parent_xpath=parent_xpath)
        if title_name!=title:
            error_list.append(f'批量操作弹框标题与预期不符，预期为{title_name},实际是{title}')
        return error_list

    def batchoperator_quick_search(self, searchName, parent_xpath='',**kwargs):
        '''
        输入检索名称并回车
        :param searchName: 需要检索的内容
        :param parent_xpath: 父级路径
        '''
        #输入框路径
        loc=parent_xpath+f'//div[contains(@class,"searchAdvanced")]//input[contains(@placeholder,"请输入")]'
        self.input_and_enter(loc,searchName)

    def batchoperator_button(self, buttonName, parent_xpath='',**kwargs):
        '''
        点击按钮操作按钮
        :param buttonName:
        :param parent_xpath:
        :return:
        '''
        self.button.click_button(buttonName,parent_xpath)

    def batchoperator_procedure(self,opButtonName,cellContent=None,columnName=None,searchName=None,parent_xpath='',**kwargs):
        '''
        批量操作过程（打开批量操作弹窗,或通过快捷搜索选择筛选数据，点击全选，点击批量操作）
        :param opButtonName: 提交批量操作的按钮名称
        :param searchName: 快捷搜索输入内容
        :param cellContent: 指定行单元格内容（不传数据表示全选）
        :param parent_xpath: 父级路径
        :param kwargs:
        :return:
        '''
        #在打开批量弹窗的基础上
        #通过快捷搜索筛选数据
        if searchName:
            self.batchoperator_quick_search(searchName,parent_xpath)
        if cellContent:
            # 选择指定行
            self.table.table_selectByCell_content(cellContent, columnName, parent_xpath=parent_xpath)
        else:
            #点击全选
            self.table.table_row_select_all(parent_xpath=parent_xpath)
        #点击批量操作按钮
        self.button.click_button(opButtonName,parent_xpath)

    def batchoperator_assert(self,data,title_name,searchName=None,parent_xpath='',isAssert=True,**kwargs):
        '''
        批量操作页面校验：
        1、批量操作弹窗标题校验
        2、批量操作table列名校验
        3、批量操作table列表内容校验
        :param data:data=[{"姓名":"张天逸","联系方式":"15199398787","部门":"泛微-北方大区","上级":"王紫博","多行文本":"设计师","入职时间":"2021-06-23"},
              {"姓名": "彭浩秋","联系方式": "16179993456","部门": "设计师","上级": "张华","多行文本": "设计师","入职时间": "2021-08-21"}
              ]
              按照表格传入预期验证的数据，key:列名  value：指定行对应的列值
        :param title_name: 批量操作弹窗标题
        :param searchName: 批量操作快捷搜索内容
        :param parent_xpath: 父级路径
        :param kwargs:
        :return:
        '''
        #批量操作弹出窗验证
        errorsList1=self.batchoperator_title_assert(title_name,parent_xpath)
        #快捷搜索筛选数据
        if searchName:
            self.batchoperator_quick_search(searchName,parent_xpath)
            self.sleep(1)
        #table内容校验
        errorsList2=self.table.table_data_assert_row(data,parent_xpath,isAssert=False)
        #table列名
        lion_value=self.table.table_lion_value(parent_xpath=parent_xpath)
        lion_value=[i for i in lion_value if i!=""]
        res=[k for i in data for k,v in i.items()]
        if  set(lion_value)!=set(res):
            errorsList2.append(f'列名与实际不符，预期是：{res}，实际是{lion_value}')
        errorsList=errorsList2+errorsList1
        if isAssert:
            assert errorsList==[],f"批量操作表单内容校验失败{errorsList}"
        return errorsList

    def batchoperator_menu_click(self,menuName,parent_xpath=""):
        '''
        点击打开批量操作页面
        :param menuName: 操作菜单名称
        :return:
        '''
        self.icon.click_icon_by_class("Icon-Message-tag-read-o",parent_xpath)
        self.menu.menu_click_menu_item(menuName)
