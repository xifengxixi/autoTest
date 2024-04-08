import logging
import colorlog
import os, sys
sys.path.append(os.getcwd())
from datetime import datetime
from ui_frame.config import UiConfig


log_dir = UiConfig.log_dir
is_log = UiConfig.is_log


class MyLogger:

    def __init__(self, log_name='', level='INFO', fmt='', datefmt='', **kwargs):
        self.log_name = log_name or f'log_{datetime.now().strftime("%Y%m%d-%H%M")}.log'
        self.log_dir = os.path.join(log_dir, self.log_name) if not kwargs.get('log_dir') else kwargs.get('log_dir')
        self.level = level
        self.fmt = fmt or '%(asctime)s|%(filename)s:%(lineno)d|%(levelname)s| %(message)s'
        self.datefmt = datefmt or '%Y-%m-%d %H:%M:%S'

    def create_log(self):
        # 创建一个日志对象
        self.logger = logging.getLogger('')
        # 设置全局的日志级别 DEBUG < INFO < WARNING < ERROR < CRITICAL
        self.logger.setLevel(logging.getLevelName(self.level))
        if is_log:
            # ----------文件日志----------
            # 创建文件日志的控制器
            self.file_handler = logging.FileHandler(self.log_dir, encoding='utf-8')
            formatter = logging.Formatter(self.fmt, datefmt=self.datefmt)
            self.file_handler.setFormatter(formatter)
            # 将文件日志控制器加入到日志对象
            self.logger.addHandler(self.file_handler)
            # ----------控制台日志----------
            # 创建控制台日志的控制器
            self.console_handler = colorlog.StreamHandler()
            # 设置控制台日志的格式
            format = colorlog.ColoredFormatter(f"%(log_color)s{self.fmt}")
            self.console_handler.setFormatter(format)
            # 将控制台日志控制器加入到日志对象
            self.logger.addHandler(self.console_handler)
        return self.logger

logger = MyLogger().create_log()

if __name__ == '__main__':
    logger.debug("这是一个debug信息")
    logger.info("这是一个info信息")
    logger.warning("这是一个warning信息")
    logger.error("这是一个error信息")
    logger.critical("这是一个critical信息")
