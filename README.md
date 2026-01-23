# 🚀 Portable Sync Backup

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/yukhyohwa/portable-sync-backup/graphs/commit-activity)
[![GitHub repo size](https://img.shields.io/github/repo-size/yukhyohwa/portable-sync-backup)](https://github.com/yukhyohwa/portable-sync-backup)
[![GitHub last commit](https://img.shields.io/github/last-commit/yukhyohwa/portable-sync-backup)](https://github.com/yukhyohwa/portable-sync-backup/commits/main)
[![GitHub issues](https://img.shields.io/github/issues/yukhyohwa/portable-sync-backup)](https://github.com/yukhyohwa/portable-sync-backup/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/yukhyohwa/portable-sync-backup)](https://github.com/yukhyohwa/portable-sync-backup/pulls)

A professional, lightweight, and robust file synchronization tool built in Python. Perfect for maintaining mirrors of your critical projects on portable drives, USB sticks, or secondary local storage.

---

## ✨ Key Features

-   **🔍 Smart Diffing**: High-performance comparison using file modification timestamps and sizes.
-   **🪞 Mirror Mode**: Syncs source to destination accurately, handling new files, updates, and orphaned deletions.
-   **📂 Multi-Task Support**: Configure and execute multiple independent sync tasks in one run.
-   **🚫 Intelligent Exclusions**: Skip large or sensitive directories like `.git`, `node_modules`, or `__pycache__`.
-   **📅 Detailed Logging**: Automated generation of timestamped logs for every operation, tracking exactly what was changed.
-   **🛡️ Safety First**: Interactive summaries and confirmation prompts prevent accidental data loss.
-   **🦾 Automation Ready**: Command-line flags (e.g., `--yes`) for non-interactive execution (perfect for scheduled tasks).
-   **✅ Task Toggling**: Easily enable or disable specific sync tasks via the `enabled` configuration property.

---

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/portable-sync-backup.git
cd portable-sync-backup
```

### 2. Setup (Optional but Recommended)
Create a virtual environment to keep your system Python clean:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

---

## ⚙️ Configuration

Copy the example configuration to create your own:
```bash
cp config/sync_config.json.example config/sync_config.json
```

### Configuration Schema
Edit `config/sync_config.json` with your project paths:
```json
[
    {
        "name": "Project Alpha",
        "source": "C:\\Users\\User\\Projects\\Alpha",
        "destination": "E:\\Backup\\Alpha",
        "enabled": true,
        "exclude": [".git", "node_modules", ".venv"]
    }
]
```

| Key | Description |
| :--- | :--- |
| `name` | Identity of the sync task. |
| `source` | Absolute path to the source folder. |
| `destination` | Absolute path to the destination folder. |
| `enabled` | `true` (default) or `false`. Disabled tasks are skipped. |
| `exclude` | List of folder/file names to ignore during sync. |

---

## 🚀 Usage

Run the sync tool from the root directory:

```bash
python sync_backup.py [options]
```

### Command Line Options

| Option | Shorthand | Description |
| :--- | :--- | :--- |
| `--yes` | `-y` | Skip the confirmation prompt and execute immediately. |
| `--help` | `-h` | Show help message and exit. |

---

## 📂 Project Structure

```text
portable-sync-backup/
├── src/                # Internal application logic
│   └── portable_sync/  # Core package
├── config/             # Configuration files
│   ├── sync_config.json        # Your private configuration (ignored by Git)
│   └── sync_config.json.example # Template for new users
├── logs/               # Automated execution logs (generated at runtime)
├── sync_backup.py      # Main execution script (entry point)
├── .gitignore          # Standard Python ignore rules
├── LICENSE             # MIT License
└── README.md           # You are here!
```

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
