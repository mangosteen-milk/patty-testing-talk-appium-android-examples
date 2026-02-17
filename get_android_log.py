import asyncio
import websockets
import requests


async def connect(session_id):
    ws_url = f'ws://localhost:4723/ws/session/{session_id}/appium/device/logcat'
    async with websockets.connect(ws_url) as ws:
        async for message in ws:
            print(message)

# Appium2 获取会话的url
# response = requests.get('http://localhost:4723/sessions')
# Appium3 获取会话的url
# 要获取会话信息，Appium启动时需带安全相关参数  appium --relaxed-security
response = requests.get('http://localhost:4723/appium/sessions')
sessions = response.json()
sess_id = sessions['value'][0]['id']
asyncio.run(connect(sess_id))
