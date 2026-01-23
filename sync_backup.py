import os
import sys
import json
import argparse

# Add src to python path so we can import our package
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from portable_sync import sync_pair
except ImportError as e:
    print(f"Error: Could not find portable_sync package. Make sure you are running from the root directory. {e}")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="🚀 Portable Sync Backup Tool")
    parser.add_argument("-y", "--yes", action="store_true", help="Automatically confirm sync without prompting")
    parser.add_argument("-c", "--config", default="config/sync_config.json", help="Path to the config file (default: config/sync_config.json)")
    args = parser.parse_args()

    # Use absolute path for the config file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, args.config)
    
    if not os.path.exists(config_path):
        print(f"❌ Configuration file not found: {config_path}")
        print("💡 Hint: Copy sync_config.json.example to sync_config.json and edit it.")
        return

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            configs = json.load(f)
    except Exception as e:
        print(f"❌ Error reading configuration: {e}")
        return

    print(f"🔍 Found {len(configs)} tasks in configuration.")

    for pair in configs:
        if not pair.get('enabled', True):
            print(f"\n⏭️  Task '{pair.get('name', 'Unknown')}' is disabled, skipping.")
            continue
        
        try:
            sync_pair(pair, auto_confirm=args.yes)
        except Exception as e:
            print(f"💥 Task '{pair.get('name', 'Unknown')}' failed: {e}")

if __name__ == "__main__":
    main()
