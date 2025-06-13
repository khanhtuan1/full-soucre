import pyautogui
import time
import keyboard

def auto_send_messages(filename, delay, start_delay):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Không tìm thấy file: {filename}")
        return

    print(f"Bạn có {start_delay} giây để chuyển sang cửa sổ cần gửi tin nhắn...")
    time.sleep(start_delay)

    print("Bắt đầu gửi... Nhấn F2 để tạm dừng / tiếp tục, F3 để thoát.")

    paused = False

    while True:
        for line in lines:
            if keyboard.is_pressed('F3'):
                print("Đã thoát!")
                return

            if keyboard.is_pressed('F2'):
                paused = not paused
                print("Tạm dừng..." if paused else "Tiếp tục...")
                time.sleep(0.5)

            while paused:
                if keyboard.is_pressed('F2'):
                    paused = False
                    print("Tiếp tục...")
                    time.sleep(0.5)
                elif keyboard.is_pressed('F3'):
                    print("Đã thoát!")
                    return
                time.sleep(0.1)

            pyautogui.write(line.strip())  # Gõ tin nhắn
            pyautogui.press('enter')       # Gửi tin nhắn
            time.sleep(delay)              # Delay giữa các tin

        print("Đã gửi hết danh sách tin nhắn. Lặp lại...")

if __name__ == "__main__":
    delay = float(input("Nhập delay giữa mỗi tin nhắn (giây): "))
    start_delay = float(input("Nhập delay trước khi bắt đầu gửi (giây): "))
    auto_send_messages("nhay.txt", delay, start_delay)