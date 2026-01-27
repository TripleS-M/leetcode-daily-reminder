import sys
import os
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage


class BrowserWindow(QWidget):
    def __init__(self, url):
        super().__init__()
        self.setWindowTitle("LeetCode")
        self.resize(1200, 800)

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

        self.destroyed.connect(QApplication.quit)



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
        QApplication.quit()

    def on_no(self):
        print("User clicked NO")
        # Open the embedded browser
        self.browser_window = BrowserWindow(url="https://leetcode.com/problemset/all/")
        self.browser_window.show()
        # Close the popup
        self.close()


def main():
    app = QApplication(sys.argv)
    popup = ReminderPopup()
    popup.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
