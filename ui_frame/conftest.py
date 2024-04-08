# -*- coding: utf-8 -*-
import allure
import pytest
import inspect
from time import strftime
from datetime import datetime
from ui_frame.config import UiConfig
from pageObject.common.base import Page
from ui_frame.utils.log_util import logger
from pageObject.common.reuse_remote import openBrowser


_TIMEOUT = UiConfig.timeout
_POLL_FREQUENCY = UiConfig.poll_frequency
_SCREEN_DIR = UiConfig.screen_dir
driver = UiConfig.driver
driver2 = UiConfig.driver2
_FILE_NAME = UiConfig.filename


@pytest.fixture(scope="function", autouse=True)
def add_custom_fields(request):
    start_time = strftime("%Y-%m-%d %H:%M:%S")
    allure.dynamic.testcase('', start_time)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """失败截图"""
    try:
        outcome = yield
        global driver, driver2
        rep = outcome.get_result()
        if rep.when == 'call' and rep.failed or rep.when == 'setup' and rep.failed:
            # 用例被调用且失败了
            imgName = "失败截图{}".format(str(datetime.now().strftime('%Y%m%d-%H%M%S')))
            imgPath = _SCREEN_DIR + imgName + ".png"
            fixture_names = item.fixturenames
            if driver and "browser" in fixture_names:
                img1 = imgPath.replace(".png", "_1.png")
                driver.save_screenshot(img1)
                allure.attach.file(img1, imgName + "_1.png", allure.attachment_type.PNG)
            else:
                logger.info(f"driver is None or browser not in fixture_names:{fixture_names}")
            if driver2 and "browser2" in fixture_names:
                img2 = imgPath.replace(".png", "_2.png")
                driver2.save_screenshot(img2)
                allure.attach.file(img2, imgName + "_2.png", allure.attachment_type.PNG)
    except:
        pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_assume_fail(lineno, entry):
    # assume失败时的操作
    yield  # 使用 yield处理完及时返回对象
    global driver, driver2
    agrs_data = "function='pytest_pyfunc_call"
    list_msg = inspect.stack()
    result,result2 = False,False
    for i in list_msg:
        if agrs_data in i.filename:
            try:
                for k, v in i.frame.f_locals.items():
                    if k == "funcargs":
                        args_keys = v.keys()
                        if "browser" in args_keys:
                            result = True
                        if "browser2" in args_keys:
                            result2 = True
            except Exception:
                pass
    imgName = "失败截图{}".format(str(datetime.now().strftime('%Y%m%d-%H%M%S')))
    imgPath = _SCREEN_DIR + imgName + ".png"
    if driver and result:
        img1 = imgPath.replace(".png", "_1.png")
        driver.save_screenshot(img1)
        allure.attach.file(img1, imgName + "_1.png", allure.attachment_type.PNG)
    if driver2 and result2:
        img2 = imgPath.replace(".png", "_2.png")
        driver2.save_screenshot(img2)
        allure.attach.file(img2, imgName+ "_2.png", allure.attachment_type.PNG)

@pytest.fixture(scope='class', autouse=True)
def browser():
    global driver  # global变量，相当于给上面driver = None赋值了
    if driver is None:
        logger.info("启动浏览器")
        driver = openBrowser().open_browser(UiConfig.browser_type)
        driver.maximize_window()
    yield driver
    if not UiConfig.debug:
        try:
            driver.quit()
            driver = None
            logger.info(f"关闭所有窗口，并退出相关的驱动程序")
        except:
            logger.error(f"关闭所有窗口，并退出相关的驱动程序失败！")

@pytest.fixture(scope='class', autouse=False)
def browser2():
    global driver2  # global变量，相当于给上面driver = None赋值了
    if driver2 is None:
        logger.info("启动浏览器")
        op_B = openBrowser()
        op_B.session_file = "ui_session2.json"
        driver2 =  op_B.open_browser(UiConfig.browser_type)
        driver2.maximize_window()
    yield driver2
    if not UiConfig.debug:
        try:
            driver2.quit()
            driver2 = None
            logger.info(f"关闭所有窗口，并退出相关的驱动程序")
        except:
            logger.error(f"关闭所有窗口，并退出相关的驱动程序失败！")

@pytest.fixture(scope="class", autouse=False)
def class_login(browser, filename=_FILE_NAME):
    logger.info("登录")
    # 打开文件，获取账号密码
    _BASE_URL = UiConfig.base_url
    obj = Page(browser)
    users = obj.get_user_account(filename)
    username = users[1][0]
    password = users[2][0]
    obj.login(username, password, _BASE_URL)
    return username, password

@pytest.fixture(scope="class", autouse=False)
def class_login2(browser2, filename=_FILE_NAME):
    logger.info("登录")
    # 打开文件，获取账号密码
    _BASE_URL = UiConfig.base_url
    obj = Page(browser2)
    users = obj.get_user_account(filename)
    username = users[1][1]
    password = users[2][1]
    obj.login(username, password, _BASE_URL)
    return username, password


def pytest_collection_modifyitems(items):
    for item in list(items):
        if 'skip' in item.keywords:
            items.remove(item)
