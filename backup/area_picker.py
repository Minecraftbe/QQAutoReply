import pyautogui
import time

print("🖱️ 移动鼠标到左上角，3 秒后获取坐标")
time.sleep(3)
x1, y1 = pyautogui.position()
print(f"📍 左上角：({x1}, {y1})")

print("🖱️ 移动鼠标到右下角，3 秒后获取坐标")
time.sleep(3)
x2, y2 = pyautogui.position()
print(f"📍 右下角：({x2}, {y2})")

width = x2 - x1
height = y2 - y1
print(f"✅ 截图区域: ({x1}, {y1}, {width}, {height})")
