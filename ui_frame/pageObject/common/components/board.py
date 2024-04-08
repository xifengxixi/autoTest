from common.base import Page
from selenium.webdriver.common.keys import Keys
from . import icon, button


class Board(Page):
    """看板操作
        board_get_cards_num:获取全部的看板卡片数量
        board_edit_card_name:编辑指定看板卡片名称
        board_get_card_task_count:（项目看板）获取看板的未完成及总任务数量
        board_click_cardConent_by_itemTitle:看板卡片，根据内容标题点击查看详情
        board_add_taskCard:（项目看板）新增任务看板卡片
        board_drag_card:看板拖拽卡片交换顺序（未分组不可交换）
        board_drag_card_item:拖拽卡片里面的任务/事项/其他
        board_save_task:（项目看板）安排任务
        board_get_more_option:获取看板卡片更多操作
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.button = button.Button(driver)
        self.icon = icon.Icon(driver)

    def __get_board_cards_loc(self):
        """获取看板卡片定位"""
        return "//div[@data-id and contains(@class,'ui-board-list')]"

    def __board_get_card_loc(self,card_name,parent_xpath=""):
        """
        定位到具体某个看板卡片
        :param card_name: 卡片名称
        """
        return parent_xpath + self.__get_board_cards_loc() + f"//*[text()='{card_name}']/ancestor::div[contains(@class,'ui-board-drag-handle')]"

    def board_get_cards_num(self,parent_xpath=""):
        """
        获取全部的看板卡片数量
        """
        loc = parent_xpath + self.__get_board_cards_loc()
        return len(self.find_elements(loc))

    def board_edit_card_name(self,card_name,new_card_name,parent_xpath=""):
        """
        编辑指定看板卡片名称（未分组不可编辑）
        :param card_name: 卡片名称
        :param new_card_name: 新卡片名称
        """
        if card_name != "未分组":
            loc = self.__board_get_card_loc(card_name,parent_xpath).split("/ancestor::")[0] #定位到卡片标题
            self.double_click_element(self.find_element(loc)) #双击标题
            loc = parent_xpath + self.__get_board_cards_loc() + f"//input[@value='{card_name}']"
            ele = self.find_element(loc)
            self.input_text(ele,new_card_name)
            ele.send_keys(Keys.ENTER)

    def board_get_card_task_count(self,card_name,parent_xpath=""):
        """
        （项目看板）获取看板的未完成及总任务数量
        :param card_name: 看板名称
        """
        loc = self.__board_get_card_loc(card_name,parent_xpath) + "//*[@class='weapp-project-taskboard-title-count']"
        if self.is_element_exist(loc):
            count = self.get_element_text(loc)
            return int(count[1:-1].split("/")[0]),int(count[1:-1].split("/")[1])
        else:
            return None

    def board_click_cardConent_by_itemTitle(self,card_name,item_title,parent_xpath=""):
        """
        看板卡片，根据内容标题点击查看详情
        :param card_name: 看板卡片名称
        :param item_title: 卡片中内容标题
        """
        loc = self.__board_get_card_loc(card_name,parent_xpath) + f"//*[text()='{item_title}']"
        self.click_element(loc)

    def board_add_taskCard(self,card_name,parent_xpath=""):
        """
        （项目看板）新增任务看板卡片
        :param card_name: 卡片名称
        """
        self.button.click_button("+ 新建任务分组")
        loc = parent_xpath + "//input[@placeholder='分组名称（回车键保存）']"
        ele = self.find_element(loc)
        self.input_text(ele, card_name)
        ele.send_keys(Keys.ENTER)

    def board_drag_card(self,ele_name,target_name,parent_xpath=""):
        """
        看板拖拽卡片交换顺序（未分组不可交换）
        :param ele_name: 需要拖拽的卡片名
        :param target_name: 拖拽释放的卡片名
        """
        ele = self.__board_get_card_loc(ele_name, parent_xpath).split("/ancestor::")[0]  # 定位到卡片标题
        target = self.__board_get_card_loc(target_name, parent_xpath).split("/ancestor::")[0]  # 定位到卡片标题
        self.drag_by_pyautogui(self.find_element(ele),self.find_element(target)) #+"/../.."

    def board_drag_card_item(self,card_name1,content1,card_name2,content2,parent_xpath=""):
        """
        拖拽卡片里面的任务/事项/其他
        :param card_name1:卡片1名称、content1:卡片1需要拖拽的内容
        :param card_name2:卡片2名称、content2:卡片2需要拖拽的内容
        卡片1与卡片2可以为同一个
        """
        loc1 = self.__board_get_card_loc(card_name1, parent_xpath) + f"//*[text()='{content1}']"
        loc2 = self.__board_get_card_loc(card_name2, parent_xpath) + f"//*[text()='{content2}']"
        self.drag_by_pyautogui(self.find_element(loc1),self.find_element(loc2))

    def board_save_task(self,card_name,task_name,parent_loc=""):
        """
        （项目看板）安排任务
        :param card_name: 看板名称
        :param task_name: 任务名称
        """
        loc1 = self.__board_get_card_loc(card_name,parent_loc) + "//span[text()='安排任务']"
        self.click_element(loc1)
        loc = self.__board_get_card_loc(card_name,parent_loc) + "//textarea"
        ele = self.find_element(loc)
        self.input_text(ele,task_name)
        self.button.click_button("确定",parent_loc=self.__board_get_card_loc(card_name,parent_loc))

    def board_get_more_option(self,card_name,parent_loc=""):
        """
        获取看板更多操作
        :param card_name: 看板卡片名称
        """
        parent_xpath = self.__board_get_card_loc(card_name,parent_loc)
        if self.is_element_exist(parent_xpath + "//*[contains(@class,'Icon-operation02')]"):
            self.icon.click_icon_by_class("Icon-operation02", parent_xpath)
        elif self.is_element_exist(parent_xpath + "//*[contains(@class,'Icon-more')]"):
            self.icon.icon_more_option(parent_xpath=parent_xpath)