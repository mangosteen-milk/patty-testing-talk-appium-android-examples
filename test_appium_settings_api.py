import os
import unittest
from time import sleep

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy


dev_id = 'emulator-5554'

options = UiAutomator2Options()
options.platform_name = 'android'
options.automation_name = 'uiautomator2'
options.udid = dev_id
options.app = f'{os.getcwd()}/app/AndroidDemoNew.apk'
options.app_package = 'com.example.androiddemo'
options.app_activity = 'com.example.androiddemo.MainActivity'
options.no_reset = True
options.set_capability('appium:forceAppLaunch', True)

# 写法1
# options.set_capability('appium:settings[ignoreUnimportantViews]', True)

# 写法2，从Appium 2.1开始支持
# options.set_capability('appium:settings', {
#     'ignoreUnimportantViews': True,
#     'actionAcknowledgmentTimeout': 5000
# })

appium_server_url = 'http://localhost:4723'


class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, options=options)
        self.driver.implicitly_wait(10)

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_enable_multiwindows(self):
        self.driver.update_settings({'enableMultiWindows': True})
        ele = self.driver.find_element(AppiumBy.ID, 'com.example.androiddemo:id/edit_url_input')
        self.driver.execute_script(
            'mobile: longClickGesture',
            {'elementId': ele.id, 'duration': 1000}
        )
        self.driver.find_element(AppiumBy.XPATH, '//*[@text="Paste"]').click()
        sleep(2)
        ele.clear()

    def test_ignore_unimportant_views(self):
        print(len(self.driver.find_elements(AppiumBy.XPATH, '//*')))
        self.driver.update_settings({
            'ignoreUnimportantViews': True
        })
        print('忽略不重要的元素后，元素总数为：')
        print(len(self.driver.find_elements(AppiumBy.XPATH, '//*')))

    def test_allow_invisible_elements(self):
        print(len(self.driver.find_elements(AppiumBy.XPATH, '//*[@displayed="false"]')))
        self.driver.update_settings({
            'allowInvisibleElements': True
        })
        print('不可见元素数量为：')
        print(len(self.driver.find_elements(AppiumBy.XPATH, '//*[@displayed="false"]')))


if __name__ == '__main__':
    unittest.main()
