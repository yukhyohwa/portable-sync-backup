import os
import shutil
from pathlib import Path
from datetime import datetime

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

def write_log(log_dir, task_name, log_content):
    """Write sync logs to a .txt file"""
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"sync_{task_name}_{timestamp}.txt"
    log_path = os.path.join(log_dir, log_filename)
    
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(log_content))
    
    return log_path

def sync_pair(config, auto_confirm=False):
    name = config['name']
    src = config['source']
    dst = config['destination']
    exclude = config.get('exclude', [])
    # Default log directory is a 'logs' folder in the script's directory
    # Note: script_dir here refers to where the package is, but we want logs relative to execution root or as configured
    script_dir = os.getcwd() 
    log_dir = config.get('log_dir', os.path.join(script_dir, 'logs'))

    log_messages = []
    header = f"Sync Task: {name}\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nSource: {src}\nDestination: {dst}\n{'='*50}"
    log_messages.append(header)
    print(f"\n{header}")

    if not os.path.exists(src):
        msg = f"Error: Source path {src} does not exist, skipping."
        print(msg)
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
        msg = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Status: Already synchronized. No action needed."
        print(msg)
        log_messages.append(msg)
        log_path = write_log(log_dir, name, log_messages)
        print(f"Log saved to: {log_path}")
        return

    summary_msgs = [f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Pending Changes:"]
    if to_add:
        summary_msgs.append(f"  [New] {len(to_add)} files:")
        for f in to_add:
            summary_msgs.append(f"    + {f}")
    if to_update:
        summary_msgs.append(f"  [Update] {len(to_update)} files:")
        for f in to_update:
            summary_msgs.append(f"    ~ {f}")
    if to_delete:
        summary_msgs.append(f"  [Delete] {len(to_delete)} files (not present in source):")
        for f in to_delete:
            summary_msgs.append(f"    - {f}")
    
    for msg in summary_msgs:
        print(msg)
        log_messages.append(msg)

    if not auto_confirm:
        confirm = input("\nDo you want to proceed with sync? (y/n): ").lower()
        if confirm != 'y':
            msg = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sync cancelled by user."
            print(msg)
            log_messages.append(msg)
            write_log(log_dir, name, log_messages)
            return
    else:
        print("\nAuto-confirm enabled, proceeding with sync...")

    # Execute sync
    exe_header = f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sync Execution Detail:"
    log_messages.append(exe_header)
    print(exe_header)
    
    # Ensure destination root exists
    os.makedirs(dst, exist_ok=True)

    # Handle Additions
    for rel_path in to_add:
        s_file = os.path.join(src, rel_path)
        d_file = os.path.join(dst, rel_path)
        os.makedirs(os.path.dirname(d_file), exist_ok=True)
        try:
            shutil.copy2(s_file, d_file)
            msg = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [New] Copied: {rel_path}"
            print(msg)
            log_messages.append(msg)
        except Exception as e:
            msg = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [Error] Failed to copy {rel_path}: {e}"
            print(msg)
            log_messages.append(msg)

    # Handle Updates
    for rel_path in to_update:
        s_file = os.path.join(src, rel_path)
        d_file = os.path.join(dst, rel_path)
        os.makedirs(os.path.dirname(d_file), exist_ok=True)
        try:
            shutil.copy2(s_file, d_file)
            msg = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [Update] Updated: {rel_path}"
            print(msg)
            log_messages.append(msg)
        except Exception as e:
            msg = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [Error] Failed to update {rel_path}: {e}"
            print(msg)
            log_messages.append(msg)

    # Handle Deletions
    for rel_path in to_delete:
        d_file = os.path.join(dst, rel_path)
        try:
            if os.path.isfile(d_file):
                os.remove(d_file)
            elif os.path.isdir(d_file):
                shutil.rmtree(d_file)
            msg = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [Delete] Deleted: {rel_path}"
            print(msg)
            log_messages.append(msg)
        except Exception as e:
            msg = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [Error] Failed to delete {rel_path}: {e}"
            print(msg)
            log_messages.append(msg)

    final_msg = f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Task '{name}' completed successfully!"
    print(final_msg)
    log_messages.append(final_msg)
    
    # Write the log file
    log_path = write_log(log_dir, name, log_messages)
    print(f"Log saved to: {log_path}")
