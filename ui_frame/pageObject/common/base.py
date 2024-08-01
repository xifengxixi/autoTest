import os
import re
import json
import subprocess
import platform
this_platform = platform.platform()
if 'Windows' in this_platform:
    import pyautogui
from time import sleep, time, strftime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from ui_frame.utils.log_util import logger
from ui_frame.config import UiConfig
from api_frame.apiObject.base.baseApi import BaseApi


_TIMEOUT = UiConfig.timeout
_POLL_FREQUENCY = UiConfig.poll_frequency
_SCREEN_DIR = UiConfig.screen_dir
_BROWSER_TYPE = UiConfig.browser_type
_TESTDATA_DIR = UiConfig.testdata_dir
_FILE_NAME = UiConfig.filename


class Page(object):

    def __init__(self, driver):
        self.driver = driver
        self.base_url = UiConfig.base_url.replace('/releaseWeaver', '/release/second')
        self.timeout = _TIMEOUT
        self.BaseApi = BaseApi()

    def get_user_account(self, file_name=_FILE_NAME):
        '''获取人员帐号信息'''
        user_file_path = os.path.join(_TESTDATA_DIR, file_name)
        user_file = open(user_file_path, 'r', encoding="UTF-8")
        users = user_file.readlines()
        name = []
        username = []
        password = []
        remark = []
        teams = []
        for u in users:
            name.append(u.split(',')[0].strip())
            username.append(u.split(',')[1].strip())
            password.append(u.split(',')[2].strip())
            remark.append(u.split(',')[3].strip())
            teams.append(u.split(',')[4].strip())
        return name, username, password, remark, teams

    def login(self, username, password, url=""):
        '''输入用户名密码点击登录'''
        self.load_url(url)
        domain = f'.{self.base_url.split("//")[-1].split(":")[0]}'
        PHPSESSID = self.BaseApi.login_api(username, password)
        self.driver.add_cookie({
            'name': 'PHPSESSID',
            'value': PHPSESSID,
            'domain': domain  # 替换网站域名，确保cookie在正确的域名下生效
        })
        logger.info(f"登录成功：{username}")

    def other_login(self, username, password):
        '''重新登录'''
        _BASE_URL = UiConfig.base_url
        domain = f'.{self.base_url.split("//")[-1].split(":")[0]}'
        url = _BASE_URL.replace('/releaseWeaver', '')
        PHPSESSID = self.BaseApi.login_api(username, password)
        self.driver.add_cookie({
            'name': 'PHPSESSID',
            'value': PHPSESSID,
            'domain': domain  # 替换网站域名，确保cookie在正确的域名下生效
        })
        self.load_url(url)

    def login_env(self, username, password, url=''):
        """
        登录账号并跳转到url，可跨环境
        :param username:
        :param password:
        :param url: 例子：http://www.testingedu.com.cn:8000/index.php
        :return:
        """
        domain = f'.{url.split("//")[-1].split(":")[0]}'
        is_https = True if url.find('https') > -1 else False
        PHPSESSID = self.BaseApi.login_api(username, password, domain=domain, is_https=is_https)
        self.load_url(url)
        self.driver.add_cookie({
            'name': 'PHPSESSID',
            'value': PHPSESSID,
            'domain': domain
        })
        return PHPSESSID

    def load_url(self, url, timeout=0.5):
        '''
        打开url
        :param url:
        :return:
        '''
        if "http" in url:
            url = url
        else:
            url = self.base_url + url
        try:
            self.driver.get(url)
            logger.info(f"打开url：{url}")
            try:
                self.close_alert(timeout)
            except:
                logger.info(f"0.5秒内关闭alert失败")
        except:
            logger.error(f"打开url：{url}失败！")
            raise Exception(f"打开url：{url}失败！")

    def find_element(self, loc):
        '''
        定位单个元素
        :param loc：传tuple可指定定位方式，否则默认xpath
        :param driver：不传默认页面对象，可传指定元素对象
        :return:
        '''
        if isinstance(loc, tuple):
            ele_loc = loc
        else:
            ele_loc = ("xpath", loc)
        try:
            element = WebDriverWait(self.driver, _TIMEOUT, _POLL_FREQUENCY).until(
                EC.presence_of_element_located(ele_loc))
            logger.info(f"定位元素：{loc}元素")
        except:
            logger.error(f"定位元素失败：{loc}元素！")
            raise Exception(f"定位元素失败：{loc}元素！")
        else:
            return element

    def find_element_can_click(self, loc):
        '''
        定位单个元素可被点击
        :param loc：传tuple可指定定位方式，否则默认xpath
        :param driver：不传默认页面对象，可传指定元素对象
        :return:
        '''
        if isinstance(loc, tuple):
            ele_loc = loc
        else:
            ele_loc = ("xpath", loc)
        try:
            element = WebDriverWait(self.driver, _TIMEOUT, _POLL_FREQUENCY).until(
                EC.element_to_be_clickable(ele_loc))
            logger.info(f"定位元素：{loc}元素")
        except Exception as e:
            logger.error(f"定位{loc}可被点击失败：{e}！")
            raise Exception(f"定位{loc}可被点击失败：{e}！")
        else:
            return element

    def find_elements(self, loc):
        '''
        定位多个元素
        :param loc：传tuple可指定定位方式，否则默认xpath
        :param driver：不传默认页面对象，可传指定元素对象
        :return:
        '''
        if isinstance(loc, tuple):
            ele_loc = loc
        else:
            ele_loc = ("xpath", loc)
        try:
            elements = WebDriverWait(self.driver, _TIMEOUT, _POLL_FREQUENCY).until(
                EC.presence_of_all_elements_located(ele_loc))
            logger.info(f"定位元素：[{loc}]元素")
        except:
            logger.error(f"定位元素失败：[{loc}]元素！")
            raise Exception(f"定位元素失败：[{loc}]元素！")
        else:
            return elements

    def get_element_count(self,loc):
        """
        获取元素数量
        :param loc:
        :return:
        """
        return len(self.find_elements(loc))

    def click_element(self, *locs):
        '''
        点击元素/支持多次点击
        :param loc:
        :return:
        '''
        for loc in locs:
            try:
                # ele = self.find_element_can_click(loc)
                ele = self.find_element(loc)
                ele.click()
            except Exception as e:
                raise Exception(f"元素{loc}点击失败：{e}")
            sleep(0.5)

    def click_element_retry(self,loc,times=3):
        '''
        点击元素/支持多次点击，失败后等待1秒后重试
        :param loc:
        :return:
        '''
        for num in range(1,times+1):
            try:
                ele = self.find_element(loc)
                ele.click()
                return True
            except Exception as e:
                logger.error(f"元素{loc}第{num}次尝试点击失败：{e}！")
            sleep(1)
        raise Exception(f"元素{loc}尝试{times}次后仍然点击失败")

    def click_ele(self, *eles):
        '''
        点击元素/支持多次点击
        :param loc:
        :return:
        '''
        for ele in eles:
            try:
                ele.click()
            except Exception as e:
                raise Exception(f"元素点击失败：{e}")
            sleep(0.5)

    def mouse_click(self, loc):
        '''
        鼠标点击
        :param loc:
        :return:
        '''
        try:
            ActionChains(self.driver).click(self.find_element(loc)).perform()
        except Exception as e:
            raise Exception(f"元素{loc}鼠标点击失败：{e}")
        sleep(0.5)

    def double_click_element(self,ele):
        '''
        双击元素
        '''
        ActionChains(self.driver).double_click(ele).perform()
        sleep(0.5)

    def click_text(self, text,parent_xpath="",**kwargs):
        '''
        点击文字
        :param texts:
        :return:
        '''
        loc = parent_xpath + f"//*[text()='{text}']"
        try:
            self.click_element(loc)
        except Exception as e:
            raise Exception(f"点击文字{text}失败：{e}")
        sleep(0.5)

    def is_element_exist(self, loc, wait=1.0, num=0.1):
        '''判断元素是否存在'''
        if isinstance(loc, tuple):
            ele_loc = loc
        else:
            ele_loc = ("xpath", loc)
        try:
            WebDriverWait(self.driver, wait, num).until(EC.presence_of_element_located(ele_loc))
            return True
        except Exception:
            return False

    def screenshot(self, page_name=None):
        '''
        截图
        :param page_name:
        :param loc_name:
        :return:
        '''
        try:
            times = strftime('%Y%m%d-%H%M')
            # 图片名称：函数名_年月日时分秒
            # decode('utf-8').encode('gbk')) 处理生成的文件名称不出现乱码
            file_name = os.path.join(_SCREEN_DIR, f'{page_name}{times}.png')
            # 若截图路径不存在，则创建路径
            if (os.path.exists(_SCREEN_DIR) == False):
                os.makedirs(_SCREEN_DIR)
            self.driver.save_screenshot(file_name)
            logger.info(f'截取网页：文件路径为{file_name}')
        except:
            logger.error('截取网页异常！')

    def input(self, loc, value):
        '''
        根据loc输入文本信息
        :param loc:
        :param value:
        :param driver:
        :return:
        '''
        try:
            el = self.find_element(loc)
            el.send_keys(value)
            logger.info(f"输入文本信息：{value}")
        except:
            logger.error(f"输入文本信息失败：{value}！")
            raise Exception(f"输入文本信息失败：{value}！")

    def input_and_enter(self, loc, value, needClearText = True):
        '''
        根据loc输入文本信息
        :param loc:
        :param value:
        :param needClearText:
        :return:
        '''
        try:
            ele = self.find_element(loc)
            if needClearText:
                self.clear_element(ele)
            ele.send_keys(value, Keys.ENTER)
            logger.info(f"输入文本信息：{value}")
        except Exception as e:
            logger.error(f"输入文本信息失败：{value}:{e}")
            raise Exception(f"输入文本信息失败：{value}！")

    def input_text(self,  ele, value, needClearText = True, **kwargs):
        '''
        根据element输入文本信息
        :param loc:
        :param value:
        :param driver:
        :return:
        '''
        try:
            if needClearText:
                self.clear_element(ele)
            ele.send_keys(value)
            if "single_input" in kwargs:
                if ele.get_attribute('value') != value:
                    self.clear_element(ele)
                    for key in value:
                        ele.send_keys(key)
                        sleep(0.05)
            logger.info(f"输入文本信息：{value}")
        except Exception as e:
            logger.error(f"输入文本信息失败：{e}！")
            raise Exception(f"输入文本信息失败：{e}！")

    def get_element_attribute(self, loc, attribute_name):
        '''
        获取元素属性
        :param page_name:
        :param loc_name:
        :param attribute_name:
        :return:
        '''
        try:
            el = self.find_element(loc)
            el_attribute = el.get_attribute(attribute_name)
            logger.info(f"获取元素属性：元素{loc}属性[{attribute_name}]")
            return el_attribute
        except:
            logger.error(f"获取元素属性失败：{loc}元素{attribute_name}属性！")
            raise Exception(f"获取元素属性失败：{loc}元素{attribute_name}属性！")

    def get_elements_attribute(self,loc,attribute_name):
        """"""
        elements = self.find_elements(loc)
        if not elements:
            raise Exception(f"获取一组元素属性失败：未找到{loc}元素！")
        list_attr = []
        for ele in elements:
            try:
                el_attribute = ele.get_attribute(attribute_name)
                list_attr.append(el_attribute)
            except:
                raise Exception(f"获取元素属性失败：{loc}元素{attribute_name}属性！")
        return list_attr



    def get_element_text(self, loc):
        """
        获取元素文字信息
        """
        return self.find_element(loc).text

    def get_elements_text(self, loc):
        """
        获取一组元素的文字信息
        :param loc:
        :return:
        """
        eles = self.find_elements(loc)
        text_list = []
        for ele in eles:
            self.scroll_into_view(ele) # 有时候元素需要滚动到可见区域才能获取到text
            text_list.append(ele.text)
        return text_list

    def scroll_into_view(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def find_and_scroll_to_element(self, loc):
        """
        定位不可见元素并使页面滚动到该元素
        """
        target = self.find_element(loc)
        self.scroll_into_view(target)
        sleep(.5)
        return target

    def scroll_to_element_and_click(self, ele_loc):
        """
        滚动到元素并点击
        """

        target = self.find_element(ele_loc)
        self.scroll_into_view(target)
        sleep(.5)
        target.click()

    def script(self, src):
        """
        执行js脚本
        """
        return self.driver.execute_script(src)

    def move_on(self, loc):
        """
        鼠标悬停
        """
        if "WebElement" in str(type(loc)):ele = loc # 兼容传入ele的情况
        else:ele = self.find_element(loc)
        ActionChains(self.driver).move_to_element(ele).perform()
        sleep(.5)

    def move_on_with_offset(self,loc,x=50,y=50):
        """
        鼠标悬停到元素相对x、y轴坐标差的地方
        """
        ele = self.find_element(loc)
        ActionChains(self.driver).move_to_element_with_offset(ele,x,y).perform()

    def drag_and_drop(self, ele, target):
        """
        拖拽
        """
        ActionChains(self.driver).drag_and_drop(ele, target).perform()

    def hold_and_drop(self, ele, target):
        """
        按住元素并拖拽
        """
        ActionChains(self.driver).move_to_element(ele).click_and_hold(ele).perform()
        ActionChains(self.driver).move_to_element(target).release().perform()

    def drag_by_pyautogui(self,ele,target,x_offset=20,y_offset=20,duration=1):
        """
        使用pyautogui拖动元素组件——由a拖到b, (拖动时,不能操作鼠标)
        这里的x_offset、y_offset为屏幕左上角(0,0)开始,到目标的坐标。(缩放后的坐标)
        """
        self.sleep(0.5)
        pyautogui.FAILSAFE = False
        # 滚动寻找控件
        self.scroll_into_view(ele)
        element = ele
        self.scroll_into_view(target)
        target = target
        # 通过执行js脚本获取到浏览器的边框高度
        height = self.driver.execute_script('return window.outerHeight - window.innerHeight;')
        # 获取屏幕缩放比例
        radio = self.driver.execute_script("return window.devicePixelRatio")
        # 使用pyautogui实现拖拽
        pyautogui.moveTo(x=(element.location['x'] + x_offset) * radio, y=(element.location['y'] + height + y_offset) * radio, duration=1, tween=pyautogui.linear)  # 移动鼠标
        self.sleep(1)
        pyautogui.dragTo((target.location['x'] + x_offset) * radio, (target.location['y'] + height + y_offset) * radio, duration, button='left')  # 在当前点点击左键拖动到指定坐标后松开左键
        self.sleep(0.5)

    def drag_by_pyautogui_offset(self,ele,x_value=0,y_value=0,x_offset=20,y_offset=20,duration=2):
        """
        使用pyautogui拖动元素组件——根据坐标拖拽, (拖动时,不能操作鼠标)
        这里的x_offset、y_offset为屏幕左上角(0,0)开始,到目标的坐标。(缩放后的坐标)
        注意：一次拖拽可能结果会不精准，可多次调用
        :param x_value:需要横向拖拽的坐标位移值;
        :param y_value:需要纵向拖拽的坐标位移值;
        """
        self.sleep(0.2)
        pyautogui.FAILSAFE = False
        # 滚动寻找控件
        # self.scroll_into_view(ele)
        # 通过执行js脚本获取到浏览器的边框高度
        height = self.driver.execute_script('return window.outerHeight - window.innerHeight;')
        # 获取屏幕缩放比例
        radio = self.driver.execute_script("return window.devicePixelRatio")
        # 使用pyautogui实现拖拽
        x = (ele.location['x'] + x_offset) * radio
        y = (ele.location['y'] + height + y_offset) * radio
        pyautogui.moveTo(x=x, y=y, duration=0.5, tween=pyautogui.linear)  # 移动鼠标到目标元素
        self.sleep(1)
        if x_value:
            x = (ele.location['x']  + x_value) * radio
        if y_value:
            y = (ele.location['y']  + y_value) * radio
        pyautogui.dragTo(x , y , duration, button='left')  # 在当前点点击左键拖动到指定坐标后松开左键
        self.sleep(.5)

    def drag_by_pyautogui_loc(self, loc, x_offset, y_offset, type='absolute', x_value=20, y_value=20, duration=1):
        """
        使用pyautogui拖动元素, 通过绝对坐标/相对坐标拖拽
        :param loc: 元素定位
        :param x_offset: 坐标位移值x （若type='absolute',则坐标位移从浏览器左上角（0，0）开始，若type='relative',则坐标位移从元素左上角开始）(缩放后的位移量)
        :param y_offset: 坐标位移值y （若type='absolute',则坐标位移从浏览器左上角（0，0）开始，若type='relative',则坐标位移从元素左上角开始）(缩放后的位移量)
        :param type: 'absolute' or 'relative'
        :param x_value: 相对于组件左上角的偏移量x
        :param y_value: 相对于组件左上角的偏移量y
        :param duration: 拖拽动作持续时间 （拖拽太快可能造成拖拽失败）
        """
        self.sleep(0.5)
        pyautogui.FAILSAFE = False
        # 滚动寻找控件
        element = self.find_and_scroll_to_element(loc)
        # 通过执行js脚本获取到浏览器的边框高度
        height = self.driver.execute_script('return window.outerHeight - window.innerHeight;')
        # 获取屏幕缩放比例
        radio = self.driver.execute_script("return window.devicePixelRatio")
        # 使用pyautogui实现拖拽
        x = (element.location['x'] + x_value) * radio
        y = (element.location['y'] + height + y_value) * radio
        pyautogui.moveTo(x=x, y=y, duration=0.5, tween=pyautogui.linear)
        if type == 'absolute':
            x1 = x_offset + x_value * radio
            y1 = y_offset + x_value * radio
        else:
            x1 = x_offset + (element.location['x'] + x_value) * radio
            y1 = y_offset + (element.location['y'] + height + y_value) * radio
        pyautogui.dragTo(x=x1, y=y1, duration=duration, button='left')  # 在当前点点击左键拖动到指定坐标后松开左键
        self.sleep(.5)

    def drag_and_drop_by_offset(self, ele, xoffset, yoffset):
        """
        拖拽到某个坐标
        """
        ActionChains(self.driver).click_and_hold(ele).move_by_offset(xoffset, yoffset).release().perform()

    def ele_dragRell(self,sorceLoc,targetLoc,win_x=0,win_y=120):
        """
        相对拖拽
        """
        win_x=win_x or 0
        win_y=win_y or 120

        source_ele = self.find_element(sorceLoc)
        target_ele = self.find_element(targetLoc)
        self.move_on(sorceLoc)
        between_width = target_ele.location['x'] - source_ele.location['x']
        between_height = target_ele.location['y'] - source_ele.location['y']
        source_x = int(source_ele.location['x'] + source_ele.size['width'] / 2 + win_x)
        source_y = int(source_ele.location['y'] + source_ele.size['height'] / 2 + win_y)
        if 'Windows' in this_platform:
            pyautogui.moveTo(x=source_x, y=source_y)
            sleep(.5)
            pyautogui.dragRel(xOffset=between_width, yOffset=between_height, duration=1, mouseDownUp=True)

    def move_click(self, locs, target, interval=0.5):
        """
        悬停后点击,可传多个定位
        """
        if isinstance(locs,list):
            locs = locs
        else:
            locs = [locs]
        for loc in locs:
            self.move_on(loc)
            sleep(interval)
        self.click_element(target)

    def context_click(self, ele):
        """
        右键
        """
        ActionChains(self.driver).context_click(ele).perform()

    def get_alert_text(self):
        """
        获取alert的text内容
        """
        return self.driver.switch_to.alert.text

    def accept_alert(self):
        """
        接受弹框提示
        """
        self.driver.switch_to.alert.accept()

    def clear_element(self,ele):
        """
        针对clear无效的替代方法，全选删除
        """
        # 点击
        self.click_ele(ele)
        # 相当于ctrl + a 快捷键全选
        ele.send_keys(Keys.CONTROL, "a") # windows
        # 快捷键删除
        ele.send_keys(Keys.DELETE)
        sleep(0.5)

    def clear_by_js(self,ele):
        """
        js清空输入框
        """
        ele.click()
        self.driver.execute_script("arguments[0].value = '';", ele)  # value替换为空值

    def click_by_js(self,ele):
        """
        js点击操作
        """
        self.driver.execute_script("arguments[0].click();", ele)

    def switch_frame(self, frame):
        """
        切换frame,可以传入frame的id、name、index以及selenium的WebElement对象
        """
        self.driver.switch_to.frame(frame)

    def get_current_window_handle(self):
        return self.driver.current_window_handle#当前窗口句柄

    def switch_window(self,data,type='index',isClose=False):
        """
        切换窗口,可根据index,url,title,handle切换
        """
        to_window=current_window = self.driver.current_window_handle#当前窗口句柄
        windows = self.driver.window_handles#所有窗口句柄
        if type=='index' and isinstance(data,int):#根据窗口顺序切换
            to_window=windows[data]
        elif type=='handle':
            to_window = data
        else:
            for handle in windows:
                self.driver.switch_to.window(handle)
                if type == 'url':
                    current_url = self.driver.current_url
                    if data in current_url:
                        to_window=handle
                        break
                elif type=='title':
                    current_title=self.driver.title
                    if data in current_title:
                        to_window = handle
                        break
        if isClose:
            self.driver.switch_to.window(current_window)
            self.driver.close()
        self.driver.switch_to.window(to_window)
        return current_window,to_window

    def switch_default_content(self):
        """
        返回默认的父窗口
        """
        try:
            self.driver.switch_to_default_content()
        except Exception as e:
            raise EnvironmentError(f"返回默认的父窗口失败：{e}")

    def switch_close_other_windows(self,current_window):
        """
        关闭除指定窗口以外的窗口
        :param current_window: 指定窗口句柄
        :return:
        """
        # 获取所有窗口句柄
        all_windows = self.driver.window_handles
        # 关闭除当前窗口外的所有窗口
        for window in all_windows:
            if window != current_window:
                self.driver.switch_to.window(window)
                self.driver.close()
        # 切回到原始窗口（当前窗口）
        self.driver.switch_to.window(current_window)

    def sleep(self,seconds):
        """
        等待
        :param seconds:
        :return:
        """
        sleep(seconds)

    def is_data_contain(self, d_input, d_check, check_mode=1):
        '''
        input数据是否包含check数据
        '''
        if isinstance(d_check, (int, float)) or isinstance(d_input, (int, float)):
            d_input = (type(d_check)(d_input))

        result, msg = True, ""
        if type(d_input) != type(d_check):
            result = False
            msg = u"输入和校验的数据类型不一致，分别为：{0}，{1}；".format(type(d_input), type(d_check))

        elif isinstance(d_check, str):
            # 如果比对的是string类型
            if d_input == d_check:
                result = True
            elif check_mode == 2 and d_check != "" and d_input.find(d_check) > -1:
                result = True
            else:
                result = False
                msg = u"输入值:{0},校验值:{1}；".format(d_input, d_check)
        elif isinstance(d_check, dict):
            # 字典类型
            for k in d_check.keys():
                if d_input.get(k) is not None:
                    res1, msg1 = self.is_data_contain(d_input[k], d_check[k], check_mode)
                    if not res1:
                        result = False
                        msg = msg + u'键"' + k + u'"的值不一致：' + msg1
                        break
                else:
                    result = False
                    msg = msg + u"输入值的键不存在:{0}".format(k)
        elif isinstance(d_check, list):
            # 列表类型
            for i in d_check:  # 比较list的每个成员
                bfind = False
                list_msg1 = ""
                # print('check para:',i)
                if i == {} and d_input == []:
                    msg = u"值为空；"
                    return True, "{0}".format(msg)
                for j in d_input:  # 轮询，找到一致的退出
                    # print('para j:',j)
                    res1, msg1 = self.is_data_contain(j, i, check_mode)
                    if res1:
                        bfind = True
                        # print('find para',i)
                        break
                    else:
                        list_msg1 = list_msg1 + msg1
                if not bfind:  # 没有符合的
                    print('not find i:', i)
                    # print(list_msg1)
                    result = False
                    msg = msg + u"输入值没匹配到{0}；".format(i)
        elif d_check == d_input:
            result = True
        else:
            result = False
            msg = u"输入值:{0},校验值:{1}；".format(d_input, d_check)
        return result, u"{0}".format(msg)

    def check_elem_attribute(self,ele,check_data,attribute_name="class"):
        """
        判断元素属性是否包含指定属性值
        """
        attrib_data = ele.get_attribute(attribute_name)
        if attrib_data and check_data in attrib_data:
            return True
        else:
            return False

    def wait_elem_disappear(self,loc,time_out=3):
        """
        等待元素消失
        """
        if isinstance(loc, tuple):
            ele_loc = loc
        else:
            ele_loc = ("xpath", loc)
        try:
            WebDriverWait(self.driver, time_out, _POLL_FREQUENCY).until_not(EC.presence_of_element_located(ele_loc))
        except:
            raise Exception(f"等待元素消失失败：{time_out}秒后元素还存在！")

    def wait_elem_visible(self,loc,time_out=3):
        """
        等待元素可用
        """
        if isinstance(loc, tuple):
            ele_loc = loc
        else:
            ele_loc = ("xpath", loc)
        try:
            WebDriverWait(self.driver, time_out, _POLL_FREQUENCY).until(EC.visibility_of_element_located(ele_loc))
        except Exception as e:
            raise Exception(f"等待元素可用失败：{time_out}秒后元素还不可用:{e}")

    def get_url(self, data, type='index', isClose=False):
        """
        获取窗口的url
        """
        self.switch_window(data, type, isClose)
        url = self.driver.current_url
        return url

    def get_default_download_path(self, browser=_BROWSER_TYPE):
        """获取浏览器默认下载路径"""
        operating_system = platform.system()

        if browser.lower() == "firefox":
            if operating_system == "Windows":
                config_path = os.path.expanduser("~\\AppData\\Roaming\\Mozilla\\Firefox\\profiles.ini")
                with open(config_path, "r") as file:
                    lines = file.readlines()
                    for line in lines:
                        if line.startswith("Path="):
                            path = line.split("=")[1].strip()
                            return os.path.expanduser(os.path.join("~\\AppData\\Roaming\\Mozilla\\Firefox", path))
            elif operating_system == "Linux":
                config_path = os.path.expanduser("~/.mozilla/firefox/profiles.ini")
                with open(config_path, "r") as file:
                    lines = file.readlines()
                    for line in lines:
                        if line.startswith("Path="):
                            path = line.split("=")[1].strip()
                            return os.path.expanduser(os.path.join("~/.mozilla/firefox", path))

        elif browser.lower() == "chrome":
            if operating_system == "Windows":
                process = subprocess.Popen(["reg", "query",
                                            "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders"],
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.DEVNULL,
                                           encoding='utf-8')
                output, _ = process.communicate()

                if process.returncode == 0:
                    lines = output.splitlines()
                    for line in lines:
                        if "Downloads" in line:
                            path = re.search(r"REG_SZ\s+(.*)", line)
                            if path:
                                return os.path.expanduser(path.group(1))
            elif operating_system == "Linux":
                process = subprocess.Popen(["xdg-settings", "get", "default-url-scheme-handler"],
                                           stdout=subprocess.PIPE)
                output, _ = process.communicate()

                if process.returncode == 0 and output.strip() == b'google-chrome.desktop':
                    config_path = os.path.expanduser("~/.config/google-chrome/Default/Preferences")
                    if os.path.isfile(config_path):
                        with open(config_path, "r") as file:
                            preferences = json.load(file)
                            download_path = preferences["download"]["default_directory"]
                            return os.path.expanduser(download_path)

        # 如果无法获取指定浏览器的默认下载路径，则返回 None
        return None

    def keep_a_window(self, data=0, type='index'):
        """
        保留选择的窗口，关闭其它窗口（默认选择第一个窗口）
        """
        # 获取所有窗口句柄
        handles = self.driver.window_handles
        current_window, to_window = self.switch_window(data, type)
        for i in handles:
            if i != to_window:
                self.driver.switch_to.window(i)
                self.driver.close()
        self.driver.switch_to.window(to_window)

    def capture_console_output(self):
        """
        捕获浏览器控制台的输出
        """
        script = """
                window.console_output = [];
                (function() {
                    var oldLog = console.log;
                    console.log = function(message) {
                        window.console_output.push({"type": "log", "message": message});
                        oldLog.apply(console, arguments);
                    };

                    var oldError = console.error;
                    console.error = function(message) {
                        window.console_output.push({"type": "error", "message": message});
                        oldError.apply(console, arguments);
                    };
                })();
                """
        self.driver.execute_script(script)

    def get_console_output(self):
        """
        获取浏览器控制台的输出
        """
        return self.driver.execute_script("return window.console_output;")

    def click_element_disWait(self, *ele_locs, interval=0.5):
        """点击元素、可点击多个、显示等待"""
        for ele_loc in ele_locs:
            if not isinstance(ele_loc, tuple):
                ele_loc = ("xpath", ele_loc)
            # 等待元素可点击
            try:
                logger.info(f"定位元素：{ele_loc}")
                element = WebDriverWait(self.driver, _TIMEOUT, _POLL_FREQUENCY).until(EC.element_to_be_clickable(ele_loc))
                element.click()
                sleep(interval)
            except Exception as e:
                logger.error(f"点击元素失败：{ele_loc}, 具体异常信息：{e}")
                raise Exception(f"点击元素失败：{ele_loc}, 具体异常信息：{e}")

    def scroll_to_loc(self, scroll_loc, target_loc, distance=500, timeout=3, scroll_time=10):
        """
        滚动使不存在的元素出现，并滚动到可见区域
        :param scroll_loc:
        :param target_loc:
        :param distance:
        :param timeout:
        :return:
        """
        scroll_ele = self.find_element(scroll_loc)
        for i in range(scroll_time):
            try:
                target_ele = WebDriverWait(self.driver, timeout, _POLL_FREQUENCY).until(EC.presence_of_element_located(("xpath", target_loc)))
                self.scroll_into_view(target_ele)
                return target_ele
            except Exception as e:
                print(f"滚动错误：{e}")
            # 滚动到当前位置加上滚动距离
            self.driver.execute_script("arguments[0].scrollTop += arguments[1];", scroll_ele, distance)
            # 判断是否已经滚动到底部
            if self.driver.execute_script("return arguments[0].scrollTop + arguments[0].clientHeight >= arguments[0].scrollHeight;", scroll_ele):
                break

    def is_alert_exist(self, timeout=3):
        """
        判断alert是否存在
        """
        try:
            WebDriverWait(self.driver, timeout, _POLL_FREQUENCY).until(EC.alert_is_present())
            return True
        except:
            return False

    def close_alert(self, timeout=3):
        """
        关闭alert
        :param timeout:
        :return:
        """
        alert = self.is_alert_exist(timeout)
        if alert:
            self.driver.switch_to.alert.accept()

    def get_attribute(self, loc, attr):
        """
        获取元素属性值
        :param loc: 元素定位 str or tuple
        :param attr: 属性名 str
        """

        return self.find_element(loc).get_attribute(attr)

    def input_code_to_action(self, code_loc, text, needClearText=True):
        """输入代码文本通过鼠标键盘操作"""

        code_ele = self.find_element(code_loc)
        actions = ActionChains(self.driver)
        actions.move_to_element(code_ele)
        actions.click()
        if needClearText:
            actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL)
            actions.send_keys(Keys.BACKSPACE)
        actions.send_keys(text)
        actions.perform()

    def wait_stalenes(self, loc, timeout=5):
        """
        等待元素变为陈旧（不存在或被替换）
        :param loc:
        :param timeout:
        :return:
        """
        ele = WebDriverWait(self.driver, timeout, _POLL_FREQUENCY).until(EC.staleness_of(self.find_element(loc)))
        return ele

    def load_url_close_alert(self, url, timeout=0.5):
        """
        加载url，关闭alert
        :param url:
        :param timeout:
        :return:
        """
        self.load_url(url)
        self.close_alert(timeout)

    def scroll_to_loc_level(self, scroll_loc, target_loc, distance=50, timeout=3, scroll_time=10):
        """
        横向滚动使不存在的元素出现，并滚动到可见区域
        :param scroll_loc: 滚动条元素定位路径
        :param target_loc: 目标元素定位路径
        :param distance: 每次滚动的距离，默认为 50 像素
        :param timeout: 等待目标元素出现的超时时间，默认为 3 秒
        :param scroll_time: 滚动次数，默认为 10 次
        :return: 目标元素
        """
        scroll_ele = self.find_element(scroll_loc)
        for i in range(scroll_time):
            try:
                target_ele = WebDriverWait(self.driver, timeout, _POLL_FREQUENCY).until(EC.presence_of_element_located(("xpath", target_loc)))
                self.scroll_into_view(target_ele)
                return target_ele
            except Exception as e:
                print(f"滚动错误：{e}")
            # 横向滚动
            self.driver.execute_script("arguments[0].scrollLeft += arguments[1];", scroll_ele, distance)
            # 判断是否已经滚动到最右边
            if self.driver.execute_script("return arguments[0].scrollLeft + arguments[0].clientWidth >= arguments[0].scrollWidth;", scroll_ele):
                break

    def html5_drag_and_drop(self, src_loc, tgt_loc):
        js_code = """
              var dataTransfer =
                {
                    dropEffect: '',
                    effectAllowed: 'all',
                    files: [],
                    items: {},
                    types: [],
                    setData: function (format, data) {
                        this.items[format] = data;
                        this.types.append(format);
                    },
                    getData: function (format) {
                        return this.items[format];
                    },
                    clearData: function (format) {
                    },
                    setDragImage: function (format) {
                    }
                };
            var emit = function (event, target) {
                var evt = document.createEvent('Event');
                evt.initEvent(event, true, false);
                evt.dataTransfer = dataTransfer;
                target.dispatchEvent(evt);
            };

            var DragNDrop = function (src, tgt) {
                emit('dragstart', src);
                emit('dragenter', tgt);
                emit('dragover', tgt);
                emit('drop', tgt);
                emit('dragend', src);
            }

            var src = arguments[0];
            var tgt = arguments[1];

            DragNDrop(src, tgt)
            """
        src = self.find_element(src_loc)
        tgt = self.find_element(tgt_loc)

        self.driver.execute_script(js_code, src, tgt)

    def click_text_element_disWait(self, text, parent_xpath="", POLL_FREQUENCY=0.1, TIMEOUT=15):
        """
        传入需要点击的标签内容，如：<a>hello<a/>，传入hello即可
        :param text: 需要点击的标签内容
        :param parent_xpath: 父元素的xpath，默认为空
        :param POLL_FREQUENCY: 等待频率，默认为0.1秒
        :param TIMEOUT: 超时时间，默认15秒
        """
        loc = parent_xpath + f"//*[text()='{text}']"

        try:
            logger.info(f"定位元素：{loc}")
            element = WebDriverWait(self.driver, TIMEOUT, POLL_FREQUENCY).until(
                EC.element_to_be_clickable((By.XPATH, loc)))
            element.click()

        except Exception as e:
            logger.error(f"点击元素失败：{loc}, 具体异常信息：{e}")
            raise Exception(f"点击元素失败：{loc}, 具体异常信息：{e}")

    def new_window_load_url(self, url, switch_to_new=True):
        """
        新窗口打开url
        :param url:
        :param switch_to_new: 是否切换到新窗口，默认为 True
        :return:
        """
        if "http" in url:
            url = url
        else:
            url = self.base_url + url
        js = f"window.open('{url}')"
        self.driver.execute_script(js)
        if switch_to_new:
            self.switch_window(url, 'url')
    def input_ele(self, ele, value):
        """
        根据ele输入文本信息
        :param ele:
        :param value:
        :param driver:
        :return:
        """
        try:
            ele.send_keys(value)
            logger.info(f"输入信息：{value}")
        except:
            logger.error(f"输入信息失败：{value}！")
            raise Exception(f"输入信息失败：{value}！")

    def click_real_element_disWait(self, element, POLL_FREQUENCY=0.1, TIMEOUT=15):
        """
        传入需要点击的元素对象
        :param element: 需要点击的元素对象
        :param POLL_FREQUENCY: 等待频率，默认为0.1秒
        :param TIMEOUT: 超时时间，默认15秒
        """
        try:
            logger.info(f"定位元素：{element}")
            element = WebDriverWait(self.driver, TIMEOUT, POLL_FREQUENCY).until(EC.visibility_of(element))
            element.click()
        except Exception as e:
            logger.error(f"点击元素失败：{element}, 具体异常信息：{e}")
            raise Exception(f"点击元素失败：{element}, 具体异常信息：{e}")

    def click_all_element_disWait(self, text, parent_xpath="", POLL_FREQUENCY=0.1, TIMEOUT=15):
        """
        传入需要点击的标签内容，如：<a>hello<a/>，传入hello即可
        :param text: 需要点击的标签内容
        :param parent_xpath: 父元素的xpath，默认为空
        :param POLL_FREQUENCY: 等待频率，默认为0.1秒
        :param TIMEOUT: 超时时间，默认15秒
        """
        if not isinstance(text, tuple):
            # 如果他是元组，则表示需要暂停
            pass

        if '/' not in text:

            loc = parent_xpath + f"//*[text()='{text}']"

            try:
                logger.info(f"定位元素：{loc}")
                element = WebDriverWait(self.driver, TIMEOUT, POLL_FREQUENCY).until(
                    EC.element_to_be_clickable((By.XPATH, loc)))
                element.click()

            except Exception as e:
                logger.error(f"点击元素失败：{loc}, 具体异常信息：{e}")
                raise Exception(f"点击元素失败：{loc}, 具体异常信息：{e}")
        else:
            try:
                logger.info(f"定位元素：{text}")
                element = WebDriverWait(self.driver, _TIMEOUT, _POLL_FREQUENCY).until(
                    EC.element_to_be_clickable(("xpath", text)))
                element.click()
                sleep(POLL_FREQUENCY)
            except Exception as e:
                logger.error(f"点击元素失败：{text}, 具体异常信息：{e}")
                raise Exception(f"点击元素失败：{text}, 具体异常信息：{e}")

    def click_and_input_element_disWait_old(self, text, sleep_time=0, parent_xpath="", POLL_FREQUENCY=0.1, TIMEOUT=15):
        """
        传入需要点击的标签内容，
        :param text: 需要点击的标签内容，text格式为列表格式，第一个元素为对象或者定位，第二个元素如果为点击则传入0，如果为输入则传入数值
        :param parent_xpath: 父元素的xpath，默认为空
        :param POLL_FREQUENCY: 等待频率，默认为0.1秒
        :param TIMEOUT: 超时时间，默认15秒
        :param sleep_time: 如果该元素操作完之后需要等待，就需要传入该元素，默认不等待
        """
        if not isinstance(text[0], str):
            # 如果他不是字符串，则表示他是对象，按照对象的处理方法

            try:
                # 如果能取到value，说明是要输入，如果没有，说明是要点击
                value = text[1]
            except Exception as e:
                print(e)
                value = 0

            if value:
                # 取到值了，说明要针对对象，输入文字
                try:
                    logger.info(f"定位元素：{text[0]}")
                    element = WebDriverWait(self.driver, TIMEOUT, POLL_FREQUENCY).until(EC.visibility_of(text[0]))
                    element.send_keys(value)
                    sleep(sleep_time)
                except Exception as e:
                    logger.error(f"点击元素失败：{text[0]}, 具体异常信息：{e}")
                    raise Exception(f"点击元素失败：{text[0]}, 具体异常信息：{e}")
            else:
                # 没有取到值，说明要针对对象，点击
                try:
                    logger.info(f"定位元素：{text[0]}")
                    element = WebDriverWait(self.driver, TIMEOUT, POLL_FREQUENCY).until(EC.visibility_of(text[0]))
                    element.click()
                    sleep(sleep_time)
                except Exception as e:
                    logger.error(f"点击元素失败：{text[0]}, 具体异常信息：{e}")
                    raise Exception(f"点击元素失败：{text[0]}, 具体异常信息：{e}")

        else:
            # 如果他是字符串，并且包含/，则表示他是xpath，不是文字定位，按照xpath处理

            if '/' not in text[0]:
                loc = parent_xpath + f"//*[text()='{text[0]}']"
            else:
                loc = text[0]

            try:
                # 如果能取到value，说明是要输入，如果没有，说明是要点击
                value = text[1]
            except Exception as e:
                print(e)
                value = 0

            if value:
                # 取到值了，说明要针对loc，输入文字
                try:
                    logger.info(f"定位元素：{text[0]}")
                    element = WebDriverWait(self.driver, _TIMEOUT, _POLL_FREQUENCY).until(
                        EC.element_to_be_clickable((By.XPATH, loc)))
                    element.send_keys(value)
                    sleep(sleep_time)
                except Exception as e:
                    logger.error(f"点击元素失败：{text[0]}, 具体异常信息：{e}")
                    raise Exception(f"点击元素失败：{text[0]}, 具体异常信息：{e}")

            else:
                # 没有取到值，说明要针对loc，点击
                try:
                    logger.info(f"定位元素：{('xpath', text[0])}")
                    element = WebDriverWait(self.driver, _TIMEOUT, _POLL_FREQUENCY).until(
                        EC.element_to_be_clickable((By.XPATH, loc)))
                    element.click()
                    sleep(sleep_time)
                except Exception as e:
                    logger.error(f"点击元素失败：{text[0]}, 具体异常信息：{e}")
                    raise Exception(f"点击元素失败：{text[0]}, 具体异常信息：{e}")

    def click_and_input_element_disWait(self, text, sleep_time=0, parent_xpath="", POLL_FREQUENCY=0.1, TIMEOUT=15):
        """
        传入需要点击的标签内容，
        :param text: 需要点击的标签内容，text格式为列表格式，第一个元素为对象或者定位，第二个元素如果为点击则传入0，如果为输入则传入数值
        :param parent_xpath: 父元素的xpath，默认为空
        :param POLL_FREQUENCY: 等待频率，默认为0.1秒
        :param TIMEOUT: 超时时间，默认15秒
        :param sleep_time: 如果该元素操作完之后需要等待，就需要传入该元素，默认不等待
        """
        if isinstance(text, list):
            # 如果他是列表，则表明要传值
            if not isinstance(text[0], str):
                # 如果不是字符串，则表示他是对象，按照对象的处理方法，进行传值操作
                try:
                    logger.info(f"定位元素：{text[0]}")
                    element = WebDriverWait(self.driver, TIMEOUT, POLL_FREQUENCY).until(EC.visibility_of(text[0]))
                    element.send_keys(text[1])
                    sleep(sleep_time)
                except Exception as e:
                    logger.error(f"点击元素失败：{text[0]}, 具体异常信息：{e}")
                    raise Exception(f"点击元素失败：{text[0]}, 具体异常信息：{e}")

            else:
                # 如果是字符串，则按照字符串的定位方法定位， 针对xpath进行输入
                if '/' not in text[0]:
                    loc = parent_xpath + f"//*[text()='{text[0]}']"
                else:
                    loc = text[0]

                try:
                    logger.info(f"定位元素：{text[0]}")
                    element = WebDriverWait(self.driver, _TIMEOUT, _POLL_FREQUENCY).until(
                        EC.element_to_be_clickable((By.XPATH, loc)))
                    element.send_keys(text[1])
                    sleep(sleep_time)
                except Exception as e:
                    logger.error(f"点击元素失败：{text[0]}, 具体异常信息：{e}")
                    raise Exception(f"点击元素失败：{text[0]}, 具体异常信息：{e}")

        else:
            # 不是列表，表明要点击
            if not isinstance(text, str):
                # 如果不是字符串，则表示他是对象，按照对象的处理方法，进行点击操作
                try:
                    logger.info(f"定位元素：{text}")
                    element = WebDriverWait(self.driver, TIMEOUT, POLL_FREQUENCY).until(EC.visibility_of(text))
                    element.click()
                    sleep(sleep_time)
                except Exception as e:
                    logger.error(f"点击元素失败：{text}, 具体异常信息：{e}")
                    raise Exception(f"点击元素失败：{text}, 具体异常信息：{e}")
            else:
                # 如果是字符串，则按照字符串的定位方法定位， 针对xpath进行点击
                if '/' not in text:
                    loc = parent_xpath + f"//*[text()='{text}']"
                else:
                    loc = text

                try:
                    logger.info(f"定位元素：{loc}")
                    element = WebDriverWait(self.driver, _TIMEOUT, _POLL_FREQUENCY).until(
                        EC.element_to_be_clickable((By.XPATH, loc)))
                    element.click()
                    sleep(sleep_time)
                except Exception as e:
                    logger.error(f"点击元素失败：{loc}, 具体异常信息：{e}")
                    raise Exception(f"点击元素失败：{loc}, 具体异常信息：{e}")

    def click_and_input_element_disWait_new(self, text, parent_xpath="", POLL_FREQUENCY=0.1, TIMEOUT=15):
        """
        传入需要点击的标签内容，
        :param text: 需要点击的标签内容，text格式为列表格式，第一个元素为对象或者定位，第二个元素如果为点击则传入0，如果为输入则传入数值，第三个元素为需要等待时间，若第一个元素为字符串则默认只点击不等待
        :param parent_xpath: 父元素的xpath，默认为空
        :param POLL_FREQUENCY: 等待频率，默认为0.1秒
        :param TIMEOUT: 超时时间，默认15秒
        # :param sleep_time: 如果该元素操作完之后需要等待，就需要传入该元素，默认不等待
        """
        if isinstance(text, str):
            # 如果只传入了字符串，说明只需要点击，不需要输入

            if '/' not in text:
                loc = parent_xpath + f"//*[text()='{text}']"
            else:
                loc = text

            try:
                logger.info(f"定位元素：{loc}")
                element = WebDriverWait(self.driver, _TIMEOUT, _POLL_FREQUENCY).until(
                    EC.element_to_be_clickable((By.XPATH, loc)))
                element.click()
            except Exception as e:
                logger.error(f"点击元素失败：{loc}, 具体异常信息：{e}")
                raise Exception(f"点击元素失败：{loc}, 具体异常信息：{e}")

        elif isinstance(text, list):

            # 获取操作完之后需要等待的时间，如果没传值，则默认不等待
            try:
                sleep_time = text[2]
            except Exception as e:
                print(e)
                sleep_time = 0

            # 获取该操作是点击还是输入，如果没传值，则默认点击，如果传值，则为输入
            try:
                real_value = text[1]
            except Exception as e:
                print(e)
                real_value = 0

            if real_value:
                # 如果能取到值，则进行输入
                if not isinstance(text[0], str):
                    # 如果不是字符串，则表示他是对象，按照对象的处理方法，进行传值操作
                    try:
                        logger.info(f"定位元素：{text[0]}")
                        element = WebDriverWait(self.driver, TIMEOUT, POLL_FREQUENCY).until(EC.visibility_of(text[0]))
                        element.send_keys(real_value)
                        sleep(sleep_time)
                    except Exception as e:
                        logger.error(f"点击元素失败：{text[0]}, 具体异常信息：{e}")
                        raise Exception(f"点击元素失败：{text[0]}, 具体异常信息：{e}")

                else:
                    # 如果是字符串，则按照字符串的定位方法定位， 针对xpath进行输入
                    if '/' not in text[0]:
                        loc = parent_xpath + f"//*[text()='{text[0]}']"
                    else:
                        loc = text[0]

                    try:
                        logger.info(f"定位元素：{text[0]}")
                        element = WebDriverWait(self.driver, _TIMEOUT, _POLL_FREQUENCY).until(
                            EC.element_to_be_clickable((By.XPATH, loc)))
                        element.send_keys(real_value)
                        sleep(sleep_time)
                    except Exception as e:
                        logger.error(f"点击元素失败：{text[0]}, 具体异常信息：{e}")
                        raise Exception(f"点击元素失败：{text[0]}, 具体异常信息：{e}")

            else:
                # 没有取到value值，表明要点击
                if not isinstance(text[0], str):
                    # 如果不是字符串，则表示他是对象，按照对象的处理方法，进行点击操作
                    try:
                        logger.info(f"定位元素：{text[0]}")
                        element = WebDriverWait(self.driver, TIMEOUT, POLL_FREQUENCY).until(EC.visibility_of(text[0]))
                        element.click()
                        sleep(sleep_time)
                    except Exception as e:
                        logger.error(f"点击元素失败：{text}, 具体异常信息：{e}")
                        raise Exception(f"点击元素失败：{text}, 具体异常信息：{e}")
                else:
                    # 如果是字符串，则按照字符串的定位方法定位， 针对xpath进行点击
                    if '/' not in text[0]:
                        loc = parent_xpath + f"//*[text()='{text[0]}']"
                    else:
                        loc = text[0]

                    try:
                        logger.info(f"定位元素：{loc}")
                        element = WebDriverWait(self.driver, _TIMEOUT, _POLL_FREQUENCY).until(
                            EC.element_to_be_clickable((By.XPATH, loc)))
                        element.click()
                        sleep(sleep_time)
                    except Exception as e:
                        logger.error(f"点击元素失败：{loc}, 具体异常信息：{e}")
                        raise Exception(f"点击元素失败：{loc}, 具体异常信息：{e}")

        else:
            # 只传入了对象，只需要点击
            try:
                logger.info(f"定位元素：{text}")
                element = WebDriverWait(self.driver, TIMEOUT, POLL_FREQUENCY).until(EC.visibility_of(text))
                element.click()
            except Exception as e:
                logger.error(f"点击元素失败：{text}, 具体异常信息：{e}")
                raise Exception(f"点击元素失败：{text}, 具体异常信息：{e}")

    def click_on_multiple(self, ele):
        for i in ele:
            self.click_and_input_element_disWait_new(i)

    def get_current_title_name(self):
        return self.driver.title

    def move_offset_click(self, ele_loc, target_loc, xoffset, yoffset):
        '''高级表单编辑器，点击单元格，再点击控件，实现控件填充到指定单元格'''
        # 鼠标移动到单元格点击
        target = self.find_element(target_loc)
        ActionChains(self.driver).move_to_element_with_offset(target, xoffset, yoffset).click().perform()
        # 点击元素填入布局
        self.click_element(ele_loc)

    def scroll_to_loc_new(self, scroll_loc, target_loc, distance=500, timeout=3, scroll_time=10):
        """
        支持传入ele对象格式
        滚动使不存在的元素出现，并滚动到可见区域
        :param scroll_loc:
        :param target_loc:
        :param distance:
        :param timeout:
        :return:
        """
        scroll_ele = self.find_elements(scroll_loc)[-1]
        for i in range(scroll_time):
            try:
                target_ele = WebDriverWait(self.driver, timeout, _POLL_FREQUENCY).until(EC.visibility_of(target_loc))

                self.scroll_into_view(target_ele)
                return target_ele
            except Exception as e:
                print(f"滚动错误：{e}")
            # 滚动到当前位置加上滚动距离
            self.driver.execute_script("arguments[0].scrollTop += arguments[1];", scroll_ele, distance)
            # 判断是否已经滚动到底部
            if self.driver.execute_script("return arguments[0].scrollTop + arguments[0].clientHeight >= arguments[0].scrollHeight;", scroll_ele):
                break

    def is_url_exist(self, url, timeout=3):
        """判断url是否存在"""
        end_time = time() + timeout
        while time() <= end_time:
            for handle in self.driver.window_handles:
                self.driver.switch_to.window(handle)
                if url in self.driver.current_url:
                    return True
            sleep(0.5)
        return False

    def wait_loc_disappear(self, loc='', find_time=0.5, time_out=15):
        """
        等待元素消失
        1. 若存在目标元素，则等待目标元素消失。若不存在目标元素，则等待find_time
        2. 默认目标元素为页面加载的loading元素
        """
        loc = f'//*[contains(@class,"ui-spin ui-spin-spinning")]' if not loc else loc
        if self.is_element_exist(loc, find_time):
            self.wait_elem_disappear(loc, time_out)