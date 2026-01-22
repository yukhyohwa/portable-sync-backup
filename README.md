# Portable Sync Backup

A simple and efficient Python-based file synchronization tool designed for backing up local folders to external drives (like USB sticks) or other local directories.

## Features

- **Smart Comparison**: Compares files based on modification time and file size to detect changes.
- **Mirror Sync**: Ensures the destination folder is an exact mirror of the source (handles additions, updates, and deletions).
- **Multi-Task Configuration**: Supports multiple sync pairs in a single configuration file.
- **Exclusion List**: Ability to skip specific directories or files (e.g., `.git`, `node_modules`).
- **Safety First**: Provides a summary of changes and requires manual confirmation before performing any write/delete operations.
- **Metadata Preservation**: Uses `shutil.copy2` to preserve file timestamps.

## Prerequisites

- Python 3.x

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yukhyohwa/portable-sync-backup.git
   cd portable-sync-backup
   ```

2. (Optional) Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

## Configuration

Modify `sync_config.json` to define your sync tasks:

```json
[
    {
        "name": "My Project Backup",
        "source": "C:\\path\\to\\source",
        "destination": "D:\\path\\to\\backup",
        "exclude": [".git", "node_modules", "__pycache__"]
    }
]
```

- `name`: A descriptive name for the task.
- `source`: The folder you want to back up.
- `destination`: The target folder where the backup will be stored.
- `exclude`: List of file or folder names to ignore.

## Usage

Simply run the script:

```bash
python sync_backup.py
```

The script will:
1. Scan the source and destination.
2. Display a summary of pending changes (New, Update, Delete).
3. Wait for your confirmation (`y/n`).
4. Execute the synchronization if confirmed.

## License

MIT
