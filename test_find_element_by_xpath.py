""" 相关视频：https://www.youtube.com/watch?v=cEhUKWZMon4 """

import unittest
from time import sleep

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains

dev_id = 'emulator-5554'

capabilities = dict(
    platformName='android',
    automationName='uiautomator2',
    udid=dev_id,
    appPackage='com.android.settings',
    appActivity='.Settings'
)

appium_server_url = 'http://localhost:4723'


class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url,
                                       options=UiAutomator2Options().load_capabilities(capabilities))
        self.driver.implicitly_wait(10)

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_get_page_source(self):
        print('打印当前界面元素xml树')
        print(self.driver.page_source)

    def test_find_by_xpath_text(self):
        # 按元素文本查找
        print('点击"搜索设置"')
        self.driver.find_element(AppiumBy.XPATH, '//*[@text="搜索设置"]').click()

    def test_find_by_xpath_class(self):
        print('点击"电池"一项，在电池设置界面中，查找开关类型的元素并点击')
        self.driver.find_element(AppiumBy.XPATH, '//*[@text="电池"]').click()
        # 按元素的类查找
        self.driver.find_element(AppiumBy.XPATH, '//android.widget.Switch').click()
        self.driver.find_element(AppiumBy.XPATH, '//*[@class="android.widget.Switch"]').click()

    def test_find_by_xpath_resource_id(self):
        # 通过resource-id查找
        print('点击搜索框')
        self.driver.find_element(AppiumBy.XPATH,
                                 '//*[@resource-id="com.android.settings:id/search_action_bar"]').click()

    def test_find_by_xpath_desc(self):
        self.driver.find_element(AppiumBy.XPATH, '//*[@text="显示"]').click()
        # 通过描述信息查找
        self.driver.find_element(AppiumBy.XPATH,
                                 '//*[@content-desc="上一步"]').click()

    def test_find_by_xpath_matches_multiple_criteria(self):
        self.driver.find_element(AppiumBy.XPATH, '//*[@text="网络和互联网"]').click()
        airplane_mode_switch = self.driver.find_element(AppiumBy.XPATH, '(//android.widget.Switch)[2]')
        if not airplane_mode_switch.get_attribute('checked'):
            airplane_mode_switch.click()
        # 查找满足多种条件的元素
        ele = self.driver.find_element(AppiumBy.XPATH, '//*[@enabled="false" and @resource-id="android:id/title"]')
        print(f'被禁用的是 {ele.text} 这一项')

    def test_find_by_xpath_index(self):
        self.driver.find_element(AppiumBy.XPATH, '//*[@text="网络和互联网"]').click()
        # 按索引号获取查找到的所有匹配元素中的第n个
        self.driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.Switch)[2]')

    def test_find_by_xpath_node_index(self):
        # 存在多个同类型节点，获取特定顺序的节点
        # 点击第三个设置项
        self.driver.find_element(by=AppiumBy.XPATH, value='//*[@resource-id="com.android.settings:id/recycler_view"]/android.widget.LinearLayout[3]').click()

    def test_find_by_xpath_attribute_contains(self):
        # 查找属性包含特定内容的元素
        self.driver.find_element(AppiumBy.XPATH, '//*[contains(@resource-id, "search_bar")]').click()

    def test_find_by_xpath_attribute_starts_with(self):
        # 查找某个属性以特定文本开头的元素
        self.driver.find_element(AppiumBy.XPATH, '//*[starts-with(@text, "应用")]').click()

    def test_find_by_xpath_attribute_ends_with(self):
        # 查找某个属性以特定文本结尾的元素
        self.driver.find_element(AppiumBy.XPATH, '//*[ends-with(@text, "通知")]').click()

    def test_find_by_xpath_attribute_matches(self):
        # 查找某个属性符合一定规则（正则表达式）的元素
        ele = self.driver.find_element(AppiumBy.XPATH, r'//*[matches(@text, "已使用 .+? - 还剩 .+? GB")]')
        print(f'存储空间使用情况为：{ele.text}')

    def test_find_descendant_element_by_xpath(self):
        # 查找后代元素。两个斜杠 // 表示任意层级的后代
        self.driver.find_element(AppiumBy.XPATH,
                                 '//*[@resource-id="com.android.settings:id/search_bar"]//android.widget.ImageButton').click()

    def test_find_child_element_by_xpath(self):
        # 查找子元素（直接下级元素）。一个斜杠 / 表示子元素，即第一层级的后代
        self.driver.find_element(AppiumBy.XPATH, '//*[@resource-id="com.android.settings:id/search_action_bar"]/android.widget.ImageButton').click()

    def test_find_ancestor_element_by_xpath(self):
        # 查找祖先元素。ancestor:: 表示任意层级的祖先
        ele = self.driver.find_element(AppiumBy.XPATH, '//*[@text="声音"]/ancestor::android.widget.ScrollView')
        print(f'目标元素的resource-id为：{ele.get_attribute('resource-id')}')

    def test_find_parent_element_by_xpath(self):
        # 查找父元素（直接上级元素）。可以用 parent:: 表达，也可以用两个点 .. 表达
        ele = self.driver.find_element(AppiumBy.XPATH, '//*[@resource-id="com.android.settings:id/homepage_container"]/..')
        print(f'父元素的类型为：{ele.get_attribute("className")}')

    def test_find_sibling_element_by_xpath(self):
        # 查找兄弟元素
        # 往后查找兄弟元素 following-sibling::
        ele = self.driver.find_element(AppiumBy.XPATH, '//*[@text="显示"]/following-sibling::android.widget.TextView')
        print(f'往后查找第一个类型为TextView的兄弟元素，文本内容为{ele.text}')
        # 往前查找兄弟元素 /preceding-sibling::
        ele = self.driver.find_element(AppiumBy.XPATH, '//*[@text="音量、振动、勿扰"]/preceding-sibling::android.widget.TextView')
        print(f'往前查找第一个类型为TextView的兄弟元素，文本内容为{ele.text}')

    def test_find_related_element_by_xpath(self):
        # 通过复杂关系定位元素。如：查找父元素的兄弟元素的子元素
        ele = self.driver.find_element(AppiumBy.XPATH, '//*[@text="电池"]/../../following-sibling::*//*[@resource-id="android:id/title"]')
        print(f'"电池"的下一项设置是：{ele.text}')


if __name__ == '__main__':
    unittest.main()
