import pyautogui
import time

print("🖱️ 请将鼠标移动到目标区域，2 秒后将获取坐标...")
time.sleep(2)
x, y = pyautogui.position()
print(f"📍 当前坐标：({x}, {y})")
