import base64
import unittest
from pprint import pprint
from time import sleep

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy


dev_id = 'emulator-5554'

options = UiAutomator2Options()
options.platform_name = 'android'
options.automation_name = 'uiautomator2'
options.udid = dev_id
# options.app_package = 'com.android.settings'
# options.app_activity = '.Settings'
# options.app_package = 'com.example.androiddemo'
# options.app_activity = 'com.example.androiddemo.MainActivity'
options.app_package = 'com.google.android.apps.messaging'
options.app_activity = 'com.google.android.apps.messaging.ui.ConversationListActivity'
# options.app = f'{os.getcwd()}/app/AndroidDemoNew.apk'
options.no_reset = True
options.set_capability('appium:forceAppLaunch', True)

appium_server_url = 'http://localhost:4723'


class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, options=options)
        self.driver.implicitly_wait(10)

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_mobile_shell(self):
        # 通过adb执行测试设备的shell命令
        pprint(
            self.driver.execute_script('mobile: shell',
                                       {'command': 'ls', 'args': '/sdcard/Download/', 'includeStderr': True}))

    def test_mobile_exec_emu_console_command(self):
        # 执行模拟设备控制台命令
        print(self.driver.execute_script('mobile: execEmuConsoleCommand', {'command': 'help-verbose'}))
        print(self.driver.execute_script('mobile: execEmuConsoleCommand', {'command': 'help sensor'}))
        print(self.driver.execute_script('mobile: execEmuConsoleCommand', {'command': 'rotate'}))

    def test_long_click_gesture(self):
        # 长按手势
        self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
            value='new UiScrollable(new UiSelector().resourceId("com.android.settings:id/main_content_scrollable_container"))' \
                  '.scrollIntoView(new UiSelector().text("About emulated device"))').click()
        ele = self.driver.find_element(AppiumBy.XPATH, '//*[@text="Device name"]')
        self.driver.execute_script('mobile: longClickGesture', {'elementId': ele.id, 'duration': 1000})

    def test_double_click_gesture(self):
        # 双击手势
        self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
            value='new UiScrollable(new UiSelector().resourceId("com.android.settings:id/main_content_scrollable_container"))' \
                  '.scrollIntoView(new UiSelector().text("About emulated device"))').click()
        self.driver.find_element(AppiumBy.XPATH, '//*[@text="Device name"]').click()
        ele = self.driver.find_element(AppiumBy.ID, 'android:id/edit')
        self.driver.execute_script('mobile: doubleClickGesture', {'elementId': ele.id})

    def test_drag_gesture(self):
        # 拖拽手势
        self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
            value='new UiScrollable(new UiSelector().resourceId("com.android.settings:id/main_content_scrollable_container"))' \
                  '.scrollIntoView(new UiSelector().text("System"))').click()
        self.driver.find_element(AppiumBy.XPATH, '//*[@text="Languages & input"]').click()
        self.driver.find_element(AppiumBy.XPATH, '//*[@text="Languages"]').click()
        ele = self.driver.find_elements(AppiumBy.ID, 'com.android.settings:id/dragHandle')[1]
        ele1 = self.driver.find_elements(AppiumBy.ID, 'com.android.settings:id/dragHandle')[0]
        self.driver.execute_script('mobile: dragGesture',
                                   {'elementId': ele.id, 'endX': ele1.location['x'], 'endY': ele1.location['y']})
        ele = self.driver.find_elements(AppiumBy.ID, 'com.android.settings:id/dragHandle')[1]
        ele1 = self.driver.find_elements(AppiumBy.ID, 'com.android.settings:id/dragHandle')[0]
        self.driver.execute_script('mobile: dragGesture',
                                   {'elementId': ele.id, 'endX': ele1.location['x'], 'endY': ele1.location['y']})

    def test_fling_gesture(self):
        # 快速滑动。（释放后会有惯性继续移动）
        self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
            value='new UiScrollable(new UiSelector().resourceId("com.android.settings:id/main_content_scrollable_container"))' \
                  '.scrollIntoView(new UiSelector().text("System"))').click()
        self.driver.find_element(AppiumBy.XPATH, '//*[@text="Languages & input"]').click()
        self.driver.find_element(AppiumBy.XPATH, '//*[@text="Languages"]').click()
        self.driver.find_element(AppiumBy.XPATH, '//*[@text="Add a language"]').click()
        ele = self.driver.find_element(AppiumBy.ID, 'android:id/list')
        print(self.driver.execute_script('mobile: flingGesture',
                                         {'elementId': ele.id, 'direction': 'down', 'speed': 15000}))

    def test_pinch_gesture(self):
        # 放大、缩小手势
        self.driver.activate_app('com.google.android.apps.photos')
        self.driver.find_element(AppiumBy.XPATH, '//*[@text="Pictures"]').click()
        self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                 'new UiSelector().descriptionContains("Photo taken on")').click()
        ele = self.driver.find_element(AppiumBy.ID,
                                       'com.google.android.apps.photos:id/video_player_controller_fragment_container')
        self.driver.execute_script('mobile: pinchOpenGesture', {'elementId': ele.id, 'percent': 0.75})
        self.driver.execute_script('mobile: pinchCloseGesture', {'elementId': ele.id, 'percent': 0.75})
        self.driver.terminate_app('com.google.android.apps.photos')

    def test_swipe_gesture(self):
        # 滑动手势
        self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
            value='new UiScrollable(new UiSelector().resourceId("com.android.settings:id/main_content_scrollable_container"))' \
                  '.scrollIntoView(new UiSelector().text("System"))').click()
        self.driver.find_element(AppiumBy.XPATH, '//*[@text="Languages & input"]').click()
        self.driver.find_element(AppiumBy.XPATH, '//*[@text="Languages"]').click()
        self.driver.find_element(AppiumBy.XPATH, '//*[@text="Add a language"]').click()
        ele = self.driver.find_element(AppiumBy.ID, 'android:id/list')
        self.driver.execute_script('mobile: swipeGesture',
                                   {'elementId': ele.id, 'direction': 'up', 'percent': 1})

    def test_scroll_gesture(self):
        # 滚动手势
        ele = self.driver.find_element(AppiumBy.ID, 'com.android.settings:id/main_content_scrollable_container')
        self.driver.execute_script('mobile: scrollGesture',
                                   {'elementId': ele.id, 'direction': 'down', 'percent': 1})

    def test_deep_link(self):
        # 深度链接。以模拟器自带的Messages APP的deeplink为例
        self.driver.execute_script('mobile: deepLink',
                                   {'url': 'sms:10086?body=KTHKRTC ', 'package': 'com.google.android.apps.messaging'})
        sleep(5)
        self.driver.save_screenshot('test_deep_link.png')
        self.driver.terminate_app('com.google.android.apps.messaging')

    def test_logs_broadcast(self):
        # 日志广播
        print(self.driver.session_id)
        self.driver.execute_script('mobile: startLogsBroadcast')
        # 在此等待期间，启动 get_android_log 脚本
        sleep(15)
        self.driver.find_element(AppiumBy.XPATH, '//*[@text="Battery"]').click()
        self.driver.execute_script('mobile: stopLogsBroadcast')

    def test_device_idle(self):
        # 禁止、启用APP的电池优化选项。以AndroidDemoNew APP为例
        self.driver.execute_script('mobile: deviceidle',
                                   {'action': 'whitelistAdd', 'packages': ['com.example.androiddemo']})
        # self.driver.execute_script('mobile: deviceidle', {'action': 'whitelistRemove', 'packages': ['com.example.androiddemo']})

    def test_accept_alert(self):
        # 处理系统弹窗。以AndroidDemoNew APP为例
        self.driver.wait_activity('com.example.androiddemo.MainActivity', timeout=5)
        self.driver.execute_script('mobile: acceptAlert', {'buttonLabel': 'Only this time'})
        try:
            self.driver.execute_script('mobile: acceptAlert', {'buttonLabel': 'Allow'})
        except Exception:
            pass
        self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Open navigation drawer').click()

    def test_change_permissions(self):
        # 在运行时修改权限。以AndroidDemoNew APP为例
        print(self.driver.execute_script('mobile: getPermissions', {'type': 'denied'}))
        self.driver.execute_script('mobile: changePermissions', {
            'permissions': 'android.permission.READ_CONTACTS',
            'target': 'pm',
            'action': 'revoke'  # grant
        })
        print(self.driver.execute_script('mobile: getPermissions', {'type': 'denied'}))
        print(self.driver.execute_script('mobile: getPermissions', {'type': 'granted'}))

    def test_perform_editor_action(self):
        # 以模拟器自带的Messages APP为例
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Search messages').click()
        self.driver.find_element(AppiumBy.CLASS_NAME, 'android.widget.EditText').send_keys('test')
        self.driver.execute_script('mobile: performEditorAction', {'action': 'search'})

    def test_get_notifications(self):
        # 获取通知
        pprint(self.driver.execute_script('mobile: getNotifications'))

    def test_open_notifications(self):
        # 打开通知栏
        self.driver.execute_script('mobile: openNotifications')
        self.driver.find_element(AppiumBy.XPATH, '//*[@text="Appium Settings"]')

    def test_get_sms_list(self):
        # 获取短信列表
        pprint(self.driver.execute_script('mobile: listSms'))

    def test_type(self):
        # 以模拟器自带的Messages APP为例
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Search messages').click()
        self.driver.execute_script('mobile: type', {'text': 'test01'})

    def test_sensor_set(self):
        # 模拟改变传感器的值。仅用于模拟器
        self.driver.execute_script('mobile: sensorSet', {'sensorType': 'pressure', 'value': 450})
        print(self.driver.execute_script('mobile: execEmuConsoleCommand', {'command': 'sensor get pressure'}))

    def test_pull_file(self):
        # 从测试设备拉取文件
        # content = self.driver.execute_script('mobile: pullFile', {'remotePath': '/sdcard/Download/ui_hierchary.xml'})
        content = self.driver.pull_file('/sdcard/Download/ui_hierchary.xml')
        binary_data = base64.b64decode(content)
        output = 'ui_hierchary.xml'
        with open(output, 'wb') as f:
            f.write(binary_data)

    def test_push_file(self):
        # 把文件传到测试设备
        file_path = 'app/AndroidDemoNew.apk'
        with open(file_path, 'rb') as file:
            binary_data = file.read()
            base64_encoded = base64.b64encode(binary_data)
            base64_string = base64_encoded.decode('utf-8')
            self.driver.execute_script('mobile: pushFile',
                                       {'remotePath': '/sdcard/Download/AndroidDemoNew.apk', 'payload': base64_string})
            # self.driver.push_file(destination_path='/sdcard/Download/AndroidDemoNew.apk', base64data=base64_string)
        # self.driver.push_file(destination_path='/sdcard/Download/AndroidDemoNew.apk', source_path=file_path)

    def test_delete_file(self):
        # 删除测试设备里的文件
        self.driver.execute_script('mobile: deleteFile', {'remotePath': '/sdcard/Download/AndroidDemoNew.apk'})

    def test_pull_folder(self):
        # 从测试设备拉取文件夹
        content = self.driver.execute_script('mobile: pullFolder', {'remotePath': '/sdcard/Download/Test01'})
        # content = self.driver.pull_folder('/sdcard/Download/Test01')
        binary_data = base64.b64decode(content)
        output = 'Test01.zip'
        with open(output, 'wb') as f:
            f.write(binary_data)

    def test_is_app_installed(self):
        # 检测APP是否安装
        print(self.driver.execute_script('mobile: isAppInstalled', {'appId': 'com.example.androiddemo'}))
        # print(self.driver.is_app_installed('com.example.androiddemo'))

    def test_query_app_state(self):
        # 查询APP状态
        print(self.driver.execute_script('mobile: queryAppState', {'appId': 'com.example.androiddemo'}))
        # self.driver.query_app_state('com.example.androiddemo')

    def test_remove_app(self):
        # 删除APP
        self.driver.execute_script('mobile: removeApp', {'appId': 'com.example.androiddemo'})
        # self.driver.remove_app('com.example.androiddemo')

    def test_install_app(self):
        # 安装APP。以AndroidDemoNew APP为例
        self.driver.execute_script('mobile: installApp',
                                   {'appPath': './app/AndroidDemoNew.apk', 'allowTestPackages': True,
                                    'grantPermissions': True})
        # self.driver.install_app(app_path='./app/AndroidDemoNew.apk', allowTestPackages=True, grantPermissions=True)
        self.driver.activate_app('com.example.androiddemo')
        self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Open navigation drawer').click()

    def test_get_app_strings(self):
        # 获取APP文本
        pprint(self.driver.execute_script('mobile: getAppStrings'))

    def test_geolocation(self):
        # 设置/获取地理位置
        self.driver.execute_script('mobile: setGeolocation', {'latitude': 39.9042, 'longitude': 116.4074})
        # 刷新GPS缓存，有时候刷新后仍获取到旧的，可多刷新几次
        self.driver.execute_script('mobile: refreshGpsCache')
        print(self.driver.execute_script('mobile: getGeolocation'))

    def test_get_system_bars(self):
        # 获取系统状态栏和导航栏信息
        print(self.driver.execute_script('mobile: getSystemBars'))
        # print(self.driver.get_system_bars())

    def test_send_sms(self):
        # 模拟发送短信，仅适用于模拟器
        # self.driver.execute_script('mobile: sendSms', {'phoneNumber': '+8615700030006', 'message': 'test'})
        self.driver.send_sms('+8615700030006', 'test')

    def test_gsm_call(self):
        # 模拟打电话，仅适用于模拟器。例如用于模拟APP操作时被电话中断的情况
        self.driver.execute_script('mobile: gsmCall', {'phoneNumber': '+8615700030006', 'action': 'call'})

    def test_ui_mode(self):
        # 设置深色模式。可选值yes,no,auto,custom_schedule,custom_bedtime
        self.driver.execute_script('mobile: setUiMode', {'mode': 'night', 'value': 'no'})
        # 获取UI模式
        print(self.driver.execute_script('mobile: getUiMode', {'mode': 'night'}))
