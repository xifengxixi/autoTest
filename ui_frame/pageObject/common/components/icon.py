from common.base import Page


class Icon(Page):
    """
    图标操作
    常见基础图标，如高级搜索、增加、关闭、清除、展开、关注、点赞
    """

    def click_search_icon(self, parent_xpath=""):
        """
        点击放大镜图标(用于点击打开组件,用于搜索内容的放大镜图标请移步click_icon_search_icon)
        """
        loc = parent_xpath + "//span[contains(@class,'associative-search-icon')]"
        self.move_click(loc, loc)

    def click_close_icon(self,parent_xpath=""):
        """
        点击页面右上角的X
        """
        loc = parent_xpath + "//div[contains(@class,'ui-dialog-closeIcon')]"
        try:
            self.click_element(loc)
        except:
            l = parent_xpath + "//*[name()='svg' and contains(@class, 'Icon-error')]/.."
            self.click_element_retry(l)

    def click_icon_by_class(self,icon_class,parent_xpath=""):
        """
        根据class获取图标
        :param icon_class: svg标签中可用于标签身份识别的class
        """
        loc = parent_xpath + f"//*[contains(@class,'{icon_class}')]"
        self.click_element(loc)

    def click_cancel_icon(self,parent_xpath=""):
        """
        点击取消图标-实心（清除内容）
        """
        loc = parent_xpath + "//*[contains(@class,'Icon-cancel')]"
        self.move_click(loc, loc)

    def icon_wait_loading_disappear(self,parent_xpath=""):
        """
        等待加载按钮消失
        """
        loc = parent_xpath + "//*[contains(@class,'Icon-Loading')]"
        self.wait_elem_disappear(loc)

    def icon_click_enlarge(self,parent_xpath=""):
        """
        点击(弹层)右上角展开图标
        """
        loc = parent_xpath + "//*[contains(@class,'Icon-enlarge')]"
        self.click_element(loc)
    def icon_click_narrow(self,parent_xpath=""):
        """
        点击(弹层)右上角缩小图标
        """
        loc = parent_xpath + "//*[contains(@class,'Icon-narrow')]"
        self.click_element(loc)
    def icon_click_advanced_search(self,parent_xpath=""):
        """
        点击高级搜索图标
        """
        loc = parent_xpath + "//*[contains(@class,'Icon-Advanced-search')]"
        self.click_element(loc)

    def icon_click_add_to(self,parent_xpath=""):
        """
        点击+图标(新增)
        """
        loc = parent_xpath + "//*[name()='svg' and contains(@class,'Icon-add-to')]"
        self.click_element(loc)

    def icon_move_add_to(self,parent_xpath=""):
        """
        点击+图标(新增)
        """
        loc = parent_xpath + "//*[name()='svg' and contains(@class,'Icon-add-to')]"
        self.move_on(loc)

    def icon_click_edit_o(self,parent_xpath=""):
        """
        点击编辑图标
        """
        loc = parent_xpath + "//*[name()='svg' and contains(@class,'Icon-edit-o')]"
        self.click_element(loc)


    def icon_click_follow(self,is_atted=False,parent_xpath=""):
        """
        点击关注图标(关注+取消关注)
        :param is_atted: False(默认)-关注操作;True-取消关注操作
        """
        loc = parent_xpath + "//*[contains(@class,'Icon-Collection')]"
        if is_atted:
            loc = parent_xpath + "//*[contains(@class,'Icon-score-o')]"
        self.move_click(parent_xpath,loc)

    def icon_check_is_followed(self,parent_xpath=""):
        """
        判断是否已关注——已关注返回True; 未关注返回False; 无法确定返回None
        无法确定的原因：找不到关注(或取消关注)图标,请检查parent_xpath是否正确
        """
        loc = parent_xpath + "//*[contains(@class,'Icon-score-o')]"
        if self.is_element_exist(loc):
            return True
        elif self.is_element_exist(parent_xpath + "//*[contains(@class,'Icon-Collection')]"):
            return False
        else:
            return None

    def icon_click_globalSearch(self):
        """
        点击全局搜索图标
        """
        loc = "//div[@class='e10header-quick-search-button']//span"
        self.click_element(loc)

    def icon_click_quickly_option(self,option):
        """
        导航栏点击快捷操作图标
        :param option: A-快速新建 | B-服务中心 | C-待办/关注/标签，传入A或B或C 也可以直接传入title名称，如：服务中心
        """
        if option in ["A", "B", "C"]:
            items = {"A": "快捷菜单", "B": "服务中心", "C": "待办/关注/标签"}
            loc = f"//div[@title='{items[option]}' and @class='e10header-quick-toolbar-item']"
        else:
            loc = f"//div[@title='{option}' and @class='e10header-quick-toolbar-item']"
        self.move_on(loc)

    def icon_click_refresh(self,left_refresh=False,parent_xpath=""):
        """
        点击刷新图标
        :param left_refresh: True:刷新方向为逆时针；False:刷新方向为顺时针(默认)
        """
        loc = parent_xpath + "//span//*[contains(@class,'Icon-right-refresh')]"
        if left_refresh:
            loc = parent_xpath + "//span//*[contains(@class,'Icon-Left-refresh')]"
        self.move_click(loc,loc)

    def icon_click_addition(self,parent_xpath=""):
        """
        点击批量添加操作图标
        """
        loc = parent_xpath + "//*[contains(@class,'Icon-Batch-addition')]"
        self.click_element(loc)

    def icon_click_fabulous(self,cancel_fab=False,parent_xpath=""):
        """
        点赞及取消点赞
        :param cancel_fab: True-取消点赞;False(默认)-点赞
        """
        loc = parent_xpath + "//*[contains(@class,'Icon-satisfied-o')]"
        if cancel_fab:
            loc = parent_xpath + "//*[contains(@class,'Icon-satisfied')]"
        self.move_click(loc,loc)

    def icon_check_is_fabuloused(self,parent_xpath=""):
        """
        判断是否已点赞——已点赞返回True; 未点赞返回False; 无法确定返回None
        无法确定的原因：找不到点赞(或取消点赞)图标,请检查parent_xpath是否正确
        """
        loc = parent_xpath + "//*[contains(@class,'Icon-satisfied')]"
        if self.is_element_exist(loc):
            if self.is_element_exist(parent_xpath + "//*[contains(@class,'Icon-satisfied-o')]"):
                return False
            else:
                return True
        else:
            return None

    def icon_click_right_arrow(self,parent_xpath=""):
        """
        点击右键/双右键图标（下一页、移至最后一页、点击展开功能等）
        """
        loc = parent_xpath + "//*[contains(@class,'Icon-Right-arrow')]"
        self.click_element(loc)

    def icon_click_left_arrow(self,parent_xpath=""):
        """
        点击左键/双左键图标（上一页、移至第一页等功能）
        """
        loc = parent_xpath + "//*[contains(@class,'Icon-left-arrow')]"
        self.click_element(loc)

    def icon_click_down_arrow(self,parent_xpath=""):
        """
        点击下键/双下键图标（例如展开/收缩等功能）
        """
        loc = parent_xpath + "//*[contains(@class,'Icon-Down-arrow')]"
        self.click_element(loc)

    def icon_click_up_arrow(self,parent_xpath=""):
        """
        点击上键/双上建图标（例如收起图标）
        """
        loc = parent_xpath + "//*[contains(@class,'Icon-up-arrow')]"
        self.click_element(loc)

    def icon_click_error_icon(self,parent_xpath=""):
        """
        点击×图标,有外圈时图标是空心（如关闭弹层,清空）
        """
        icon_class = "Icon-error"
        self.click_icon_by_class(icon_class, parent_xpath)

    def icon_hover_help_intro(self,parent_xpath=""):
        """
        hover提示图标
        """
        icon_class = "Icon-help02"
        self.click_icon_by_class(icon_class, parent_xpath)

    def icon_click_reduce_icon(self,parent_xpath=""):
        """
        点击最小化窗口图标
        """
        icon_class = "Icon-reduce"
        self.click_icon_by_class(icon_class, parent_xpath)
    def icon_more_option(self,hover=False,parent_xpath=""):
        """
        点击...或竖三点图标（如更多操作）
        :param hover: 是否仅hover
        """
        icon_class = "Icon-more"
        if hover:
            self.move_on(parent_xpath + "//*[name()='svg' and contains(@class,'{}')]".format(icon_class))
        else:
            self.click_icon_by_class(icon_class, parent_xpath)

    def icon_click_search_option(self,parent_xpath=""):
        """
        点击放大镜图标（用于搜索功能）
        """
        icon_class = 'Icon-search'
        self.click_icon_by_class(icon_class, parent_xpath)
    def icon_click_upload(self,parent_xpath=""):
        """
        点击上传图标
        """
        icon_class = "Icon-upload"
        self.click_icon_by_class(icon_class, parent_xpath)

    def icon_click_schedule(self,parent_xpath=""):
        """
        点击日程图标
        """
        icon_class = "Icon-schedule-o"
        self.click_icon_by_class(icon_class, parent_xpath)

    def icon_click_setting(self,parent_xpath=""):
        """
        点击设置图标
        """
        icon_class = "Icon-set-up-o"
        self.click_icon_by_class(icon_class, parent_xpath)

    def icon_click_Multilingual(self,parent_xpath=""):
        """
        点击多语言设置图标
        """
        icon_class = "Icon-Multilingual-o"
        self.click_icon_by_class(icon_class, parent_xpath)

    def get_move_icon_loc(self, parent_xpath=""):
        """
        获取拖拽图标元素
        :param parent_xpath:
        :return:
        """
        return parent_xpath + f"//*[contains(@class,'Icon-move')]/.."

    def icon_drag_move_icon(self, target, parent_xpath=""):
        """
        拖拽图标
        """
        # self.ele_dragRell(self.get_move_icon_loc(parent_xpath), target)
        ele = self.find_element(self.get_move_icon_loc(parent_xpath))
        target = self.find_element(target)
        self.drag_by_pyautogui(ele,target,x_offset=10,y_offset=10)

    def icon_hover_batch_operation(self,parent_xpath=""):
        """
        hover批量操作图标
        """
        loc = parent_xpath + "//*[contains(@class,'Icon-Batch-operation-o')]/.."
        self.move_on(loc)

    def icon_click_Batch_delete(self,parent_xpath=""):
        """
        点击批量删除图标
        """
        icon_class = "Icon-Batch-delete"
        self.click_icon_by_class(icon_class,parent_xpath)

    def icon_click_delete(self,parent_xpath=""):
        """
        点击删除图标
        """
        loc = parent_xpath + "//*[contains(@class,'Icon-delete')]"
        self.click_element(loc)

    def icon_click_clock(self,parent_xpath=""):
        """
        点击时钟图标
        """
        loc = parent_xpath + "//*[contains(@class,'Icon-time')]"
        self.click_element(loc)

    def icon_click_aite(self,parent_xpath=""):
        """
        点击@图标
        """
        loc = parent_xpath + "//*[contains(@class,'Icon-@My-new-feedback-o')]"
        self.click_element(loc)

    # def icon_click_not_disturb(self,parent_xpath=""):
    #     """
    #     点击免打扰图标
    #     """
    #     loc = parent_xpath + "//*[contains(@class,'Icon-Don't-disturb-o')]"
    #     self.click_element(loc)

    def icon_click_personnel(self,parent_xpath=""):
        """
        点击单人图标
        """
        loc = parent_xpath + "//*[contains(@class,'Icon-personnel')]"
        self.click_element(loc)

    def icon_click_home(self,parent_xpath=""):
        """
        点击home图标
        """
        loc = parent_xpath + "//*[contains(@class,'Icon-gateway-o')]"
        self.click_element(loc)

    def icon_click_groupChat(self,parent_xpath=""):
        """
        点击群聊/群组图标
        """
        loc = parent_xpath + "//*[contains(@class,'Icon-group3-o')]"
        self.click_element(loc)

    def icon_click_initialization(self,parent_xpath=""):
        """
        点击初始化图标
        """
        loc = parent_xpath + "//*[name()='svg' and contains(@class,'Icon-linitialization')]"
        self.click_element(loc)

    def icon_click_logIcon(self,parent_xpath=""):
        """
        点击日志图标
        """
        loc = parent_xpath + "//*[name()='svg' and contains(@class,'Icon-Operation-log-o')]"
        self.click_element(loc)

    def icon_click_toolIcon(self,parent_xpath=""):
        """
        点击工具图标
        """
        loc = parent_xpath + "//*[name()='svg' and contains(@class,'icon-tool')]"
        self.click_element(loc)

    def icon_click_disabled(self,parent_xpath=""):
        """
        点击停用图标
        """
        loc = parent_xpath + "//*[contains(@class,'Icon-Display-disabled')]"
        self.click_element(loc)

    def icon_click_no_disabled(self,parent_xpath=""):
        """
        点击取消停用图标
        """
        loc = parent_xpath + "//*[contains(@class,'Icon-No-display-disabled')]"
        self.click_element(loc)

    def icon_move_down_arrow(self, parent_xpath=""):
        """
        移动鼠标到下键/双下键图标（例如展开/收缩等功能）
        """
        loc = parent_xpath + "//*[contains(@class,'Icon-Down-arrow')]"
        self.move_on(loc)

    def get_icon_loc_byClass(self, class_name, parent_xpath=""):
        """
        根据class获取icon的loc
        :param class_name: 如Icon-Multilingual-多语言图标
        """
        # Author: zhaoyading
        # Create Date: 2024-02-27
        loc = parent_xpath + f"//*[name()='svg' and contains(@class,'{class_name}')]/.."
        return loc

    def click_back_to_top_icon(self,parent_xpath=""):
        """
        点击取消停用图标
        """
        loc = parent_xpath + "//*[contains(@class,'Icon-Back-to-top')]"
        self.click_element(loc)

    def icon_hover_tag_read(self,parent_xpath=""):
        """
        hover批量操作图标
        """
        loc = parent_xpath + "//*[contains(@class,'Icon-Message-tag-read-o')]/.."
        self.move_on(loc)

    def icon_click_filter(self, parent_xpath=""):
        """
        点击放大镜图标，表单字段管理-字段选择
        """
        loc = parent_xpath + "//*[contains(@class,'Icon-filter')]"
        self.click_element(loc)