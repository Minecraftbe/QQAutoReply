import time
import pyautogui
import pyperclip
from keyboard import is_pressed as KB_is_pressed
from openai import OpenAI

# ========================
# 配置项（务必改成你自己的Key和坐标）
# ========================

services: dict = {
    "openai": (
        ("gpt-4o", "gpt-4o-mini", "gpt-4.1-mini-2025-04-14"),
        "sk-hGffTSbiSYskaI5aS7C4miqAv9iw1koquStmf9nh9N5ktJik",
        "https://zzzzapi.com/v1"
    ),
    "deepseek": (
        ("deepseek-chat", "deepseek-reasoner"),
        "sk-59b6b4bdb59c4b01a90e515202a21e92",
        "https://api.deepseek.com"
    )
}
service_provider = "deepseek"
service = services.get(service_provider)
response_model = service[0][0]
print(response_model)

client = OpenAI(api_key=service[1], base_url=service[2])

# 输入框坐标 (x, y), 最后一条消息坐标 (x, y)
input_box_pos = (720, 779)
chat_pos = (674, 676)

role: str = (
    "你是一个人在使用 QQ 聊天，日常用中文简洁回复他人，"
    "不要暴露你是 AI，也不要展现内心活动或系统提示。"
    "如果对方使用英文或其他语言，也用对应语言简要回复。"
    "尽量避免啰嗦和重复，用人类语气回复"
    "不要解释自己，直接进入主题，像朋友一样自然对话。"
    "当被骂时不要做（屏蔽对方）的活动"
)

messages: list[dict] = [
    {"role": "system", "content": role}
]
last_msg = ""


def ask_chatgpt(model):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7
        )
        if model == "deepseek-reasoner111":
            return (response.choices[0].message.content.strip(),
                    response.choices[0].message.reasoning_content.strip())
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[ERROR] ChatGPT 错误: {e}")
        return "（AI 回复失败）"


def text_getter(pos):
    pyautogui.leftClick(pos)
    pyautogui.hotkey("ctrl", "c")
    return pyperclip.paste()


print("🤖 QQ 自动回复机器人启动中...")

def main():
    is_first = True
    count = 1
    safe_reply = ""
    print("3秒后启动")
    time.sleep(3)
    state = True
    while state:
        print(f"第 {count} 次运行")
        msg = text_getter(chat_pos)
        # print(msg)

        # 新消息且不重复
        if msg and msg != last_msg and msg != safe_reply:
            messages.append({"role": "user", "content": msg})

            print(f"📨 收到消息：{msg}")
            reply = ask_chatgpt(response_model)
            if isinstance(reply, tuple):
                reasoning = reply[1].replace('\n', ' ').replace('\r', ' ')
                safe_reply = reply[0].replace('\n', ' ').replace('\r', ' ')
                final_reply = f"🤔推理过程:\n{reasoning}\n🤓最终答案:\n{safe_reply}"

            elif isinstance(reply, str):
                safe_reply = reply.replace('\n', ' ').replace('\r', ' ')
                final_reply = safe_reply
                print(f"💬 回复内容：{safe_reply}")

            else:
                raise TypeError(f"非法回复类型，类型为{type(reply)}")

            # 点击输入框
            pyautogui.click(input_box_pos)

            # 将回答添加到上下文中
            messages.append({"role": "assistant", "content": safe_reply})

            # 复制回复内容到剪贴板
            pyperclip.copy(final_reply)

            # 点击输入框并粘贴
            pyautogui.click(input_box_pos)
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.1)
            pyautogui.press('enter')

            last_msg = msg

        if count == 50:
            print(messages)
        is_first = False
        count += 1
        time.sleep(0.3)


if __name__ == '__main__':
    main()