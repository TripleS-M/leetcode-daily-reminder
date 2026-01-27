import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)


class ReminderPopup(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LeetCode Daily Reminder")
        self.resize(400, 150)

        # Text label
        label = QLabel("Have you done a LeetCode question today?")
        label.setWordWrap(True)

        # Buttons
        yes_button = QPushButton("Yes")
        no_button = QPushButton("No")

        # Connect buttons to actions
        yes_button.clicked.connect(self.on_yes)
        no_button.clicked.connect(self.on_no)

        # Button layout (horizontal)
        button_layout = QHBoxLayout()
        button_layout.addWidget(yes_button)
        button_layout.addWidget(no_button)

        # Main layout (vertical)
        main_layout = QVBoxLayout()
        main_layout.addWidget(label)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def on_yes(self):
        print("User clicked YES")
        QApplication.quit()

    def on_no(self):
        print("User clicked NO")
        QApplication.quit()


def main():
    app = QApplication(sys.argv)

    popup = ReminderPopup()
    popup.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
