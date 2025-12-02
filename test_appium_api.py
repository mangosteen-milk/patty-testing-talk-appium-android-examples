import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy


dev_id = 'emulator-5554'

# capabilities = dict(
#     platformName='android',
#     automationName='uiautomator2',
#     udid=dev_id,
#     appPackage='com.android.settings',
#     appActivity='.Settings',
#     noReset=True
# )

options = UiAutomator2Options()
options.platform_name = 'android'
options.automation_name = 'uiautomator2'
options.udid = dev_id
options.app_package = 'com.android.settings'
options.app_activity = '.Settings'
options.no_reset = True
options.set_capability('appium:forceAppLaunch', True)

appium_server_url = 'http://localhost:4723'


class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        # self.driver = webdriver.Remote(appium_server_url,
        #                                options=UiAutomator2Options().load_capabilities(capabilities))
        self.driver = webdriver.Remote(appium_server_url, options=options)
        self.driver.implicitly_wait(10)

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_execute_script(self):
        ele = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.android.settings:id/main_content_scrollable_container")')
        self.driver.execute_script(
            'mobile: scroll',
            {'elementId': ele.id, 'strategy': '-android uiautomator', 'selector': 'new UiSelector().text("About emulated device")'})
        self.driver.find_element(AppiumBy.XPATH, '//*[@text="About emulated device"]').click()
        ele1 = self.driver.find_element(AppiumBy.XPATH, '//*[@text="Device name"]')
        self.driver.execute_script(
            'mobile: longClickGesture',
            {'elementId': ele1.id, 'duration': 1000}
        )
        self.driver.find_element(AppiumBy.XPATH, '//*[@text="Copy"]').click()
        assert self.driver.get_clipboard().decode('utf-8') == 'sdk_gphone_x86_64_arm64', '复制设备名称失败，预期为：sdk_gphone_x86_64_arm64'
        self.driver.save_screenshot('screenshot.png')
        ele1.screenshot('ele_screenshot.png')


if __name__ == '__main__':
    unittest.main()
