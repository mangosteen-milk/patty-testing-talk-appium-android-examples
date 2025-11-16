"""
 run server with args:
 appium --allow-insecure uiautomator2:chromedriver_autodownload
"""

import unittest
import os
from time import sleep

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy


def webview_context_available(driver):
    contexts = driver.contexts
    return len(contexts) > 1


dev_id = 'emulator-5554'

capabilities = dict(
    platformName='android',
    automationName='uiautomator2',
    udid=dev_id,
    app=f'{os.getcwd()}/AndroidDemoNew.apk',
    appPackage='com.example.androiddemo',
    appActivity='com.example.androiddemo.MainActivity',
    language='en',
    locale='US',
    # chromedriverExecutable=f'{os.getcwd()}/chromedriver/chromedriver',
    # chromedriverDisableBuildCheck=True,
    chromedriverExecutableDir=f'{os.getcwd()}/chromedriver',
    chromedriverChromeMappingFile=f'{os.getcwd()}/mapping.json',
    showChromedriverLog=True,
    # autoWebview=True,
    # browserName='chrome'
)

options = UiAutomator2Options().load_capabilities(capabilities)

appium_server_url = 'http://localhost:4723'

class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, options=options)
        self.driver.implicitly_wait(10)

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_find_gallery(self) -> None:
        el = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Open navigation drawer')
        # el = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='打开抽屉式导航栏')
        # el = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='開啟導覽列')
        el.click()
        el_1 = self.driver.find_element(by=AppiumBy.ID, value='com.example.androiddemo:id/nav_gallery')
        el_1.click()
        # 等待webview上下文可用
        WebDriverWait(self.driver, 15).until(webview_context_available)
        contexts = self.driver.contexts
        print(contexts)
        print(self.driver.context)
        self.driver.switch_to.context(contexts[1])
        # 注意此处上下文已切换到webview，查找元素用selenium的By，而不是Appium的AppiumBy
        self.driver.find_element(By.XPATH, '//button[text()="显示图片"]').click()
        sleep(2)
        self.driver.save_screenshot('screenshot.png')
        print(self.driver.context)
        # 如果还需要继续操作原生的元素，可以再切回原生的上下文
        self.driver.switch_to.context(contexts[0])
        print(self.driver.context)
        self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Open navigation drawer').click()
        el_2 = self.driver.find_element(AppiumBy.ID, 'com.example.androiddemo:id/nav_home')
        el_2.click()


if __name__ == '__main__':
    unittest.main()
