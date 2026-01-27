import sys
import os
import json
import random
from datetime import datetime, date, timedelta

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import QUrl, QTimer
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage

# -------------------
# Config
# -------------------
CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
STREAK_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "streak.json")
LEETCODE_PROFILE = os.path.join(os.getcwd(), "leetcode_profile")

def load_config():
    default_config = {
        "start_hour": 9,
        "end_hour": 21,
        "test_mode": True,
        "popup_message": "Have you done a LeetCode question today?",
        "leetcode_url": "https://leetcode.com/problemset/all/"
    }
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump(default_config, f)
        return default_config
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
    # Ensure all keys exist
    for key, value in default_config.items():
        config.setdefault(key, value)
    return config

config = load_config()
TEST_MODE = config["test_mode"]

# -------------------
# Streak Storage Utils
# -------------------
def initialize_streak():
    if not os.path.exists(STREAK_FILE):
        save_streak(0, None)
        print("streak.json created")

def load_streak():
    try:
        with open(STREAK_FILE, "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return {"streak": 0, "last_done": None}

def save_streak(streak, last_done):
    with open(STREAK_FILE, "w") as f:
        json.dump({"streak": streak, "last_done": last_done}, f)

def update_streak():
    data = load_streak()
    today_str = date.today().isoformat()
    if data["last_done"] == (date.today() - timedelta(days=1)).isoformat():
        streak = data["streak"] + 1  # consecutive
    else:
        streak = 1  # reset
    save_streak(streak, today_str)
    print(f"Streak updated! Current streak: {streak}")

# -------------------
# Browser Window
# -------------------
class BrowserWindow(QWidget):
    def __init__(self, url):
        super().__init__()
        self.setWindowTitle("LeetCode")
        self.resize(1200, 800)

        os.makedirs(LEETCODE_PROFILE, exist_ok=True)
        profile = QWebEngineProfile("LeetCodeProfile", self)
        profile.setPersistentStoragePath(LEETCODE_PROFILE)
        profile.setCachePath(LEETCODE_PROFILE)

        page = QWebEnginePage(profile, self)
        self.browser = QWebEngineView(self)
        self.browser.setPage(page)
        self.browser.load(QUrl(url))

        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        self.setLayout(layout)

        self.destroyed.connect(self.on_close)

    def on_close(self):
        update_streak()
        QApplication.quit()

# -------------------
# Reminder Popup
# -------------------
popup_window = None  # keep reference alive
browser_window = None

class ReminderPopup(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LeetCode Daily Reminder")
        self.resize(400, 150)

        label = QLabel(config["popup_message"])
        label.setWordWrap(True)

        yes_button = QPushButton("Yes")
        no_button = QPushButton("No")

        yes_button.clicked.connect(self.on_yes)
        no_button.clicked.connect(self.on_no)

        button_layout = QHBoxLayout()
        button_layout.addWidget(yes_button)
        button_layout.addWidget(no_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(label)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def on_yes(self):
        update_streak()
        QApplication.quit()

    def on_no(self):
        global browser_window
        browser_window = BrowserWindow(url=config["leetcode_url"])
        browser_window.show()
        self.close()

# -------------------
# App Startup & Scheduler
# -------------------
def show_popup():
    global popup_window
    popup_window = ReminderPopup()
    popup_window.show()

def schedule_popup():
    if TEST_MODE:
        show_popup()
        return

    start_hour = config["start_hour"]
    end_hour = config["end_hour"]

    now = datetime.now()
    hour = random.randint(start_hour, end_hour - 1)
    minute = random.randint(0, 59)

    popup_time = datetime(now.year, now.month, now.day, hour, minute)
    if popup_time < now:
        popup_time += timedelta(days=1)

    delay_ms = int((popup_time - now).total_seconds() * 1000)
    print(f"Popup scheduled at {popup_time.strftime('%H:%M:%S')} (in {delay_ms/1000:.0f}s)")
    QTimer.singleShot(delay_ms, show_popup)

class DevPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dev/Test Panel")
        self.resize(300, 150)

        show_popup_btn = QPushButton("Show Popup Now")
        reset_streak_btn = QPushButton("Reset Streak")
        toggle_test_btn = QPushButton(f"TEST_MODE: {TEST_MODE}")

        show_popup_btn.clicked.connect(self.show_popup_now)
        reset_streak_btn.clicked.connect(self.reset_streak)
        toggle_test_btn.clicked.connect(lambda: self.toggle_test(toggle_test_btn))

        layout = QVBoxLayout()
        layout.addWidget(show_popup_btn)
        layout.addWidget(reset_streak_btn)
        layout.addWidget(toggle_test_btn)
        self.setLayout(layout)

    def show_popup_now(self):
        show_popup()

    def reset_streak(self):
        save_streak(0, None)
        print("Streak reset to 0")

    def toggle_test(self, button):
        global TEST_MODE
        TEST_MODE = not TEST_MODE
        button.setText(f"TEST_MODE: {TEST_MODE}")
        print(f"TEST_MODE set to {TEST_MODE}")

# Deletes streak.json temporarily to simulate new day (uncomment code to reset day)
import os
streak_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "streak.json")
if os.path.exists(streak_file):
    os.remove(streak_file)

# -------------------
# Main
# -------------------
def main():
    initialize_streak()
    data = load_streak()
    today_str = date.today().isoformat()
    if data["last_done"] == today_str:
        print("Already completed today! Exiting...")
        return

    app = QApplication(sys.argv)

    if TEST_MODE:
        # Show developer panel for testing
        dev_panel = DevPanel()
        dev_panel.show()
    else:
        schedule_popup()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
