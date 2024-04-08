import pytest
import os
from config import UiConfig


_REPORT_DIR = UiConfig.reports_dir
reruns = UiConfig.reruns
_TEMPS = UiConfig.temp_dir
base_url = UiConfig.base_url
environment_path = UiConfig.testdata_dir + '/environment.properties'


if __name__ == '__main__':
    if not os.path.exists(UiConfig.screen_dir):
        os.makedirs(UiConfig.screen_dir)
    pytest.main([
        "-vs", "testCase",
        "--reruns", reruns,
        '--alluredir', _TEMPS, '--clean-alluredir',
    ])

    os.system("allure generate {} -o {} --clean".format(_TEMPS, _REPORT_DIR))
    with open(environment_path, 'w') as f:
        f.write('base_url={}'.format(base_url))
    with open(environment_path, 'r') as f:
        properties = f.read()
    with open(rf'{_TEMPS}/environment.properties', 'w') as f:
        f.write(properties)

    os.system("allure serve {} -p 9999".format(_TEMPS))
