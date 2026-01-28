# LeetCode Daily Reminder

A lightweight desktop application designed to keep your LeetCode streak alive. It pops up a reminder at a randomized time during your active hours, prompting you to complete your daily challenge. If you haven't done it, it opens an embedded browser directly to LeetCode, saving your session so you don't have to log in every time.

## 🚀 Features

- **Smart Random Reminders**: Schedules a popup at a random time between your specified start and end hours.
- **Embedded Browser**: Opens LeetCode in a dedicated window using QtWebEngine.
- **Persistent Sessions**: Saves your LeetCode login state in a local profile folder.
- **Streak Tracking**: Automatically tracks your daily streak and stores it locally.
- **Customizable**: Configure reminder messages, active hours, and target URLs via a simple JSON file.
- **Auto-Exit**: Closes automatically and saves progress once you confirm completion.

## 🛠️ How It Works

1.  **Initialization**: On launch, the app checks if you've already completed today's task.
2.  **Scheduling**: If not completed, it picks a random time within your `start_hour` and `end_hour`.
3.  **Reminder**: At the scheduled time, a "Yes/No" popup appears.
4.  **Action**:
    -   **Yes**: Streak increments, and the app closes.
    -   **No**: Opens the embedded browser. Closing the browser window then triggers the streak update and app exit.
5.  **Persistence**: Streak data is saved in `streak.json`, and browser data (cookies, etc.) is saved in the `leetcode_profile/` directory.

## 📦 Setup & Installation

### Prerequisites
- Python 3.8+
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)

### Local Development
1. Clone the repository:
   ```bash
   git clone https://github.com/TripleS-M/leetcode-daily-reminder.git
   cd leetcode-daily-reminder
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   python app/main.py
   ```

## 🏗️ Creating an Executable (.exe)

To package the application into a standalone executable for Windows:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Build the EXE:
   ```bash
   pyinstaller --noconsole --onefile --name LeetCodeDaily app/main.py
   ```
   *Note: If you have a custom `.spec` file, you can run `pyinstaller LeetCodeDaily.spec` instead.*

The executable will be generated in the `dist/` folder.

## 📂 Project Structure
```text
leetcode-daily-reminder/
├── app/
│   └── main.py            # Core application logic
├── data/
│   └── user_data.json     # (Optional) backup for user info
├── config.json            # App configuration (auto-generated on first run)
├── streak.json            # Local streak tracking (auto-generated)
├── leetcode_profile/      # Browser session data (auto-generated)
├── requirements.txt       # Python dependencies
└── README.md
```

## ⚙️ Configuration (`config.json`)
The first time you run the app, it creates a `config.json`. You can modify it:
```json
{
    "start_hour": 9,
    "end_hour": 21,
    "test_mode": false,
    "popup_message": "Have you done a LeetCode question today?",
    "leetcode_url": "https://leetcode.com/problemset/all/"
}
```

## ⏰ Linking to Startup on Boot

### Windows
1. Press `Win + R`, type `shell:startup`, and hit Enter.
2. Create a shortcut to the `LeetCodeDaily.exe` (found in your `dist` folder) and paste it into this folder.

### macOS
1. Open **System Settings** > **General** > **Login Items**.
2. Click the **+** button and select the bundled application.

### Linux (Ubuntu/GNOME)
1. Open **Startup Applications**.
2. Click **Add**, give it a name, and browse for the script or executable.
3. Alternatively, create a `.desktop` file in `~/.config/autostart/`.

---
*Created by [TripleS-M](https://github.com/TripleS-M)*
