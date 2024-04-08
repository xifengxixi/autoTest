import os
import json
from selenium.webdriver import Remote
from selenium.webdriver.chrome import options
from selenium.common.exceptions import InvalidArgumentException
from selenium import webdriver
from ui_frame.config import UiConfig
from ui_frame.utils.log_util import logger


class ReuseRemote(Remote):

    def __init__(self, command_executor, session_id):
        self.r_session_id = session_id
        Remote.__init__(self, command_executor=command_executor, desired_capabilities={})

    def start_session(self, capabilities, browser_profile=None):
        """
        重写start_session方法
        """
        if not isinstance(capabilities, dict):
            raise InvalidArgumentException("Capabilities must be a dictionary")
        if browser_profile:
            if "moz:firefoxOptions" in capabilities:
                capabilities["moz:firefoxOptions"]["profile"] = browser_profile.encoded
            else:
                capabilities.update({'firefox_profile': browser_profile.encoded})
        option = options.Options()
        option.add_experimental_option("w3c", False)
        self.capabilities = option.to_capabilities()
        self.session_id = self.r_session_id
        self.w3c = False

class openBrowser():

    session_file = "ui_session.json"

    def get_session_path(self):
        base_dir = os.getcwd().split("autoTest")[0]
        dir_path = os.path.join(base_dir, "autoTest", "ui_frame",  self.session_file)
        return dir_path

    def get_chrome_process_ids(self):
        """
        获取chrome进程
        :return:
        """
        f = os.popen('tasklist |find "chrome.exe"')
        lines = f.readlines()
        pids = []
        for line in lines:
            pids.append(line.split()[1])
        return pids

    def is_chrome_cef_exists(self, pids):
        """
        判断pid列表现在是否还存在
        :param pids:
        :return:
        """
        pids_now = self.get_chrome_process_ids()
        for pid in pids:
            if pid in pids_now:
                return True
        return False

    def save_session(self, driver, pids_before):
        # 保存浏览器信息
        executor_url = driver.command_executor._url
        session_id = driver.session_id
        pids_after = self.get_chrome_process_ids()
        pids = [i for i in pids_after if i not in pids_before]
        dir_path = self.get_session_path()
        data = {"session_id": session_id, "executor_url": executor_url, "pids": pids}
        save_data = {}
        if os.path.exists(dir_path):
            with open(dir_path, "r", encoding='utf-8') as f:
                save_data = json.load(f)
        save_data.update(data)
        with open(dir_path, "w", encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False)

    def new_browser(self, browser):
        # 获取开启前pids
        if UiConfig.debug:
            pids_before = self.get_chrome_process_ids()
        options = webdriver.ChromeOptions()
        is_all = os.environ.get('is_all', False)
        if is_all == "True":
            options.add_argument("--force-device-scale-factor=0.8")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("w3c", False)

        browser = browser.capitalize()
        if UiConfig.driver_path:
            driver = getattr(webdriver, browser)(UiConfig.driver_path,options=options)
        else:
            driver = getattr(webdriver, browser)(options=options)
        if UiConfig.debug:
            self.save_session(driver, pids_before)
        return driver

    def open_browser(self, browser):
        """
        打开浏览器（chrome、ie、firefox...）
        :param browser:
        :return:
        """
        try:
            if UiConfig.debug:
                # 打开保存的session信息
                dir_path = self.get_session_path()
                data = {}
                if os.path.exists(dir_path):
                    with open(dir_path, "r", encoding='utf-8') as f:
                        data = json.load(f)
                print(data)
                if data.get("pids") and self.is_chrome_cef_exists(data.get("pids")):
                    print(f"控制原来的浏览器")
                    try:
                        driver = ReuseRemote(data.get("executor_url"), data.get("session_id"))
                    except:
                        driver = self.new_browser(browser)
                else:
                    driver = self.new_browser(browser)
            else:
                driver = self.new_browser(browser)
            driver.set_window_size(1920, 1280)
            logger.info(f"打开浏览器：{browser}")
        except:
            logger.error(f"打开浏览器：{browser}失败！")
            raise Exception(f"打开浏览器：{browser}失败！")

        return driver