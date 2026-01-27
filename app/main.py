import sys
import os
import json
import random
from datetime import datetime, date, timedelta

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import QUrl, QTimer
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage

# Deletes streak.json temporarily to simulate new day (uncomment code to reset day)
#import os
#streak_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "streak.json")
#if os.path.exists(streak_file):
#    os.remove(streak_file)


TEST_Mode = True
# -------------------
# Streak Storage Utils
# -------------------
STREAK_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "streak.json")

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
        streak = 1  # reset or first day

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

        # Persistent profile
        profile_path = os.path.join(os.getcwd(), "leetcode_profile")
        os.makedirs(profile_path, exist_ok=True)

        profile = QWebEngineProfile("LeetCodeProfile", self)
        profile.setPersistentStoragePath(profile_path)
        profile.setCachePath(profile_path)

        page = QWebEnginePage(profile, self)

        self.browser = QWebEngineView(self)
        self.browser.setPage(page)
        self.browser.load(QUrl(url))

        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        self.setLayout(layout)

        # Close browser → update streak and quit app
        self.destroyed.connect(self.on_close)

    def on_close(self):
        update_streak()
        QApplication.quit()


# -------------------
# Reminder Popup
# -------------------
class ReminderPopup(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LeetCode Daily Reminder")
        self.resize(400, 150)

        label = QLabel("Have you done a LeetCode question today?")
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
        print("User clicked YES")
        update_streak()
        QApplication.quit()

    def on_no(self):
        print("User clicked NO")
        self.browser_window = BrowserWindow(url="https://leetcode.com/problemset/all/")
        self.browser_window.show()
        self.close()


# -------------------
# App Startup & Scheduler
# -------------------
def schedule_popup():

    if TEST_Mode:
        delay_ms = 1000
        print("Test mode: Popup will appear in 1 second")
        QTimer.singleShot(delay_ms, show_popup)
        return

    # Random time between X and Y
    start_hour = 12
    end_hour = 13

    now = datetime.now()
    hour = random.randint(start_hour, end_hour - 1)
    minute = random.randint(4, 6)

    popup_time = datetime(now.year, now.month, now.day, hour, minute)
    if popup_time < now:
        popup_time += timedelta(days=1)

    delay_ms = int((popup_time - now).total_seconds() * 1000)
    print(f"Popup scheduled at {popup_time.strftime('%H:%M:%S')} (in {delay_ms/1000:.0f}s)")

    QTimer.singleShot(delay_ms, show_popup)


def show_popup():
    app = QApplication.instance()
    app.popup_window = ReminderPopup()
    app.popup_window.show()

    # popup = ReminderPopup()
    # popup.show()
    # return popup


def main():
    # Load streak and check if already done today
    data = load_streak()
    today_str = date.today().isoformat()
    if data["last_done"] == today_str:
        print("Already completed today! Exiting...")
        return  # Exit app

    app = QApplication(sys.argv)

    # Schedule popup at random time
    schedule_popup()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
