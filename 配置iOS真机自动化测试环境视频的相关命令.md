安装xcuitest驱动：appium driver install xcuitest

打开WDA的项目：appium driver run xcuitest open-wda

编译WDA：xcodebuild clean build-for-testing -project ~/.appium/node_modules/appium-xcuitest-driver/node_modules/appium-webdriveragent/WebDriverAgent.xcodeproj -derivedDataPath ~/Downloads/appium_wda_ios -scheme WebDriverAgentRunner -destination generic/platform=iOS -allowProvisioningUpdates

在Appium Inspector中配置参数：

{
  "platformName": "iOS",
  "appium:udid": "0000xxx0-000xxxxxxxxxxxxx",
  "appium:bundleId": "com.apple.calculator",
  "appium:automationName": "XCUITest",
  "appium:noReset": true,
  "appium:usePrebuiltWDA": true,
  "appium:deviceName": "xx",
  "appium:derivedDataPath": "~/Downloads/appium_wda_ios"
}


补充内容相关命令（重新安装Appium及相关驱动）：

sudo appium driver uninstall uiautomator2 

sudo npm uninstall -g appium

安装nvm：

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

配置环境变量：

export NVM_DIR="$HOME/.nvm"

[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm

[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

使用nvm安装nodejs：

nvm install --lts

在nvm环境下重新安装appium：

npm install -g appium

appium driver install uiautomator2


相关视频：
https://www.youtube.com/watch?v=wCPNCWMDvFw

