import os
import shutil
import json
from pathlib import Path

def get_file_info(directory, exclude_list):
    """Recursively get information for all files in a directory (relative path: mtime + size)"""
    file_map = {}
    base_path = Path(directory)
    
    if not base_path.exists():
        return file_map

    for root, dirs, files in os.walk(directory):
        # Exclude directories
        dirs[:] = [d for d in dirs if d not in exclude_list]
        
        for file in files:
            if file in exclude_list:
                continue
                
            full_path = Path(root) / file
            rel_path = str(full_path.relative_to(base_path))
            
            try:
                stats = full_path.stat()
                # Record modification time and size as comparison criteria
                file_map[rel_path] = (stats.st_mtime, stats.st_size)
            except Exception:
                continue
                
    return file_map

def sync_pair(config):
    name = config['name']
    src = config['source']
    dst = config['destination']
    exclude = config.get('exclude', [])

    print(f"\n{'='*50}")
    print(f" Task: {name}")
    print(f" Source: {src}")
    print(f" Destination: {dst}")
    print(f"{'='*50}")

    if not os.path.exists(src):
        print(f"Error: Source path {src} does not exist, skipping.")
        return

    src_files = get_file_info(src, exclude)
    dst_files = get_file_info(dst, exclude)

    to_add = []
    to_update = []
    to_delete = []

    # Compare source files
    for rel_path, (src_mtime, src_size) in src_files.items():
        if rel_path not in dst_files:
            to_add.append(rel_path)
        else:
            dst_mtime, dst_size = dst_files[rel_path]
            # Update if source is newer or size is different
            if src_mtime > dst_mtime + 1 or src_size != dst_size:
                to_update.append(rel_path)

    # Compare destination files (find those to delete)
    for rel_path in dst_files:
        if rel_path not in src_files:
            to_delete.append(rel_path)

    # Display summary
    if not to_add and not to_update and not to_delete:
        print("Status: Already synchronized. No action needed.")
        return

    print(f"\nPending Changes:")
    if to_add:
        print(f"  [New] {len(to_add)} files")
    if to_update:
        print(f"  [Update] {len(to_update)} files")
    if to_delete:
        print(f"  [Delete] {len(to_delete)} files (not present in source)")

    confirm = input("\nDo you want to proceed with sync? (y/n): ").lower()
    if confirm != 'y':
        print("Sync cancelled.")
        return

    # Execute sync
    print("\nProgress: Executing synchronization...")
    
    # Ensure destination root exists
    os.makedirs(dst, exist_ok=True)

    # Handle Additions and Updates
    for rel_path in to_add + to_update:
        s_file = os.path.join(src, rel_path)
        d_file = os.path.join(dst, rel_path)
        os.makedirs(os.path.dirname(d_file), exist_ok=True)
        shutil.copy2(s_file, d_file) # copy2 preserves metadata/timestamps
        print(f"  Copied: {rel_path}")

    # Handle Deletions
    for rel_path in to_delete:
        d_file = os.path.join(dst, rel_path)
        try:
            if os.path.isfile(d_file):
                os.remove(d_file)
            elif os.path.isdir(d_file):
                shutil.rmtree(d_file)
            print(f"  Deleted: {rel_path}")
        except Exception as e:
            print(f"  Failed to delete {rel_path}: {e}")

    print(f"\nTask '{name}' completed successfully!")

def main():
    # Use absolute path for the config file relative to the script
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sync_config.json')
    if not os.path.exists(config_path):
        print(f"Configuration file not found: {config_path}")
        return

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            configs = json.load(f)
    except Exception as e:
        print(f"Error reading configuration: {e}")
        return

    for pair in configs:
        sync_pair(pair)

if __name__ == "__main__":
    main()
