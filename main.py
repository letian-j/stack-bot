import time
import json
import pyautogui
from pynput import mouse, keyboard


def load_config():
    with open("config.json", "r") as f:
        return json.load(f)


def get_click_position():
    position = None

    def on_click(x, y, button, pressed):
        nonlocal position
        if pressed:
            position = (x, y)
            return False

    print("Click anywhere to set the auto-click position...")
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
    return position


def auto_click(position, config):
    print(f"Position set at {position}. Press 'q' to exit.")
    time.sleep(config["start_delay"])

    exit_flag = False

    def on_press(key):
        nonlocal exit_flag
        if hasattr(key, "char") and key.char == "q":
            exit_flag = True

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    count = 0
    while not exit_flag:
        pyautogui.click(position)
        count += 1
        print(count)
        time.sleep(config["click_interval"])

    listener.stop()


if __name__ == "__main__":
    config = load_config()
    position = get_click_position()
    auto_click(position, config)
