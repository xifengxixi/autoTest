import re
from time import strftime
from secrets import token_urlsafe


class budildData():

    @staticmethod
    def time_strf():
        return strftime("%Y%m%d%H%M%S")

    @staticmethod
    def token_strf():
        return re.sub(r'[^a-zA-Z\u4e00-\u9fff]', '', token_urlsafe(8))
