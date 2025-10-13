"""
Student Code Change Watcher
Monitors student implementation files and saves timestamped snapshots
Saves to Firebase cloud database and local JSON backups
"""
import os
import sys
import time
import json
import hashlib
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Import Firebase module
try:
    import firebase_manager
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    print("Warning: Firebase module not available. Saving snapshots to JSON only.")


class StudentCodeWatcher(FileSystemEventHandler):
    """Watch student implementation files and save snapshots on changes"""
    
    def __init__(self, student_id, snapshot_interval=3, session_id=None, use_firebase=True):
        self.student_id = student_id
        self.snapshot_interval = snapshot_interval
        self.session_id = session_id
        self.use_firebase = use_firebase and FIREBASE_AVAILABLE
        
        # Initialize Firebase if available
        if self.use_firebase:
            try:
                firebase_manager.init_firebase()
                
                # If no session_id provided, try to get from notebook_tracker
                if not self.session_id:
                    # Import notebook_tracker to get session_id
                    try:
                        import notebook_tracker
                        self.session_id = notebook_tracker.get_session_id()
                    except:
                        pass
                
                # If still no session_id, create one
                if not self.session_id:
                    firebase_manager.get_or_create_student(student_id)
                    self.session_id = firebase_manager.create_session(student_id)
                
                print(f"Firebase connected - Session ID: {self.session_id}")
            except Exception as e:
                print(f"Firebase error: {e}")
                print("Falling back to JSON-only mode")
                self.use_firebase = False
        
        self.snapshots_dir = Path("student_snapshots")
        self.snapshots_dir.mkdir(exist_ok=True)
        
        # Track file hashes to avoid duplicate snapshots
        self.file_hashes = {
            'bb84': None,
            'b92': None
        }
        
        # Track last snapshot time
        self.last_snapshot = {
            'bb84': 0,
            'b92': 0
        }
        
        # Snapshot counters
        self.snapshot_counts = {
            'bb84': 0,
            'b92': 0
        }
        
        print(f"Watching code changes for student: {student_id}")
        print(f"Snapshot interval: {snapshot_interval} seconds")
        print(f"Snapshots directory: {self.snapshots_dir}")
        if not self.use_firebase:
            print("Firebase: Not available (JSON-only mode)")
        
    def _get_file_hash(self, filepath):
        """Get MD5 hash of file content"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None
    
    def _should_snapshot(self, protocol, filepath):
        """Check if we should create a snapshot"""
        current_time = time.time()
        
        # Check if enough time has passed
        if current_time - self.last_snapshot[protocol] < self.snapshot_interval:
            return False
        
        # Check if file content actually changed
        new_hash = self._get_file_hash(filepath)
        if new_hash == self.file_hashes[protocol]:
            return False
        
        self.file_hashes[protocol] = new_hash
        self.last_snapshot[protocol] = current_time
        return True
    
    def _clean_code(self, code):
        """Remove PROMPT sections and keep only actual code"""
        import re
        
        lines = code.split('\n')
        cleaned_lines = []
        skip_docstring = False
        docstring_delimiter = None
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Skip comment lines with PROMPT
            if 'PROMPT FOR' in line or '# PROMPT:' in line:
                i += 1
                continue
            
            # Check for docstring start
            if ('"""' in line or "'''" in line) and not skip_docstring:
                delimiter = '"""' if '"""' in line else "'''"
                
                # Check if it's a complete single-line docstring
                if line.count(delimiter) >= 2:
                    line_lower = line.lower()
                    if any(keyword in line_lower for keyword in ['implement', 'prompt', 'skeleton', 'constructor', 'method should']):
                        i += 1
                        continue
                    else:
                        cleaned_lines.append(line)
                        i += 1
                        continue
                
                # Multi-line docstring - look ahead to check if it's a prompt
                is_prompt = False
                for j in range(i, min(i + 10, len(lines))):
                    next_line_lower = lines[j].lower()
                    if any(keyword in next_line_lower for keyword in ['implement', 'prompt', 'skeleton', 'constructor', 'method should']):
                        is_prompt = True
                        break
                    if delimiter in lines[j] and j > i:
                        break
                
                if is_prompt:
                    skip_docstring = True
                    docstring_delimiter = delimiter
                    i += 1
                    continue
                else:
                    cleaned_lines.append(line)
                    i += 1
                    continue
            
            # Check for docstring end
            if skip_docstring and docstring_delimiter in line:
                skip_docstring = False
                i += 1
                continue
            
            # Skip if we're inside a prompt docstring
            if skip_docstring:
                i += 1
                continue
            
            cleaned_lines.append(line)
            i += 1
        
        # Remove excessive blank lines (more than 2 consecutive)
        result = '\n'.join(cleaned_lines)
        result = re.sub(r'\n\n\n+', '\n\n', result)
        
        return result
    
    def _save_snapshot(self, protocol, filepath):
        """Save a timestamped snapshot"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Clean the code to remove prompts
            code = self._clean_code(code)
            
            self.snapshot_counts[protocol] += 1
            snapshot_num = self.snapshot_counts[protocol]
            timestamp = datetime.now()
            
            # Calculate time since last snapshot
            time_since_last = 0
            if snapshot_num > 1:
                # Get previous snapshot timestamp
                prev_snapshots = list(self.snapshots_dir.glob(f"{self.student_id}_{protocol}_*.json"))
                if prev_snapshots:
                    prev_file = sorted(prev_snapshots)[-1]
                    with open(prev_file, 'r', encoding='utf-8') as f:
                        prev_data = json.load(f)
                        prev_time = datetime.fromisoformat(prev_data['timestamp'])
                        time_since_last = (timestamp - prev_time).total_seconds()
            
            # Create snapshot data
            snapshot = {
                'student_id': self.student_id,
                'protocol': protocol,
                'snapshot_number': snapshot_num,
                'timestamp': timestamp.isoformat(),
                'time_since_last_change': time_since_last,
                'code': code.split('\n'),
                'code_length': len(code),
                'line_count': len(code.split('\n')),
                'file_hash': self.file_hashes[protocol],
                'changes': {}  # Initialize changes
            }
            
            # Calculate diff if not first snapshot
            if snapshot_num == 1:
                # First snapshot - no previous data
                snapshot['changes'] = {
                    'lines_added': snapshot['line_count'],
                    'lines_removed': 0,
                    'code_length_change': snapshot['code_length'],
                    'time_spent_seconds': 0,
                    'time_spent': '0s'
                }
            elif snapshot_num > 1:
                prev_snapshots = list(self.snapshots_dir.glob(f"{self.student_id}_{protocol}_*.json"))
                if prev_snapshots:
                    prev_file = sorted(prev_snapshots)[-1]
                    with open(prev_file, 'r', encoding='utf-8') as f:
                        prev_data = json.load(f)
                        prev_lines = prev_data['code']
                        curr_lines = snapshot['code']
                        
                        # Calculate time spent in human-readable format
                        minutes = int(time_since_last // 60)
                        seconds = int(time_since_last % 60)
                        time_spent_str = f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s"
                        
                        snapshot['changes'] = {
                            'lines_added': len(curr_lines) - len(prev_lines),
                            'lines_removed': max(0, len(prev_lines) - len(curr_lines)),
                            'code_length_change': snapshot['code_length'] - prev_data['code_length'],
                            'time_spent_seconds': round(time_since_last, 1),
                            'time_spent': time_spent_str
                        }
            
            # Save snapshot to local JSON
            timestamp_str = timestamp.strftime('%Y%m%d_%H%M%S')
            snapshot_file = self.snapshots_dir / f"{self.student_id}_{protocol}_{snapshot_num:03d}_{timestamp_str}.json"
            
            with open(snapshot_file, 'w', encoding='utf-8') as f:
                json.dump(snapshot, f, indent=2, ensure_ascii=False)
            
            # Save snapshot to Firebase
            if self.use_firebase and self.session_id:
                try:
                    # Save full code snapshot
                    firebase_manager.save_snapshot(
                        self.student_id,
                        self.session_id,
                        protocol.upper(),
                        snapshot['code'],  # Pass code lines array
                        snapshot['line_count'],
                        snapshot['code_length'],
                        json.dumps(snapshot.get('changes', {}))  # Serialize changes
                    )
                    
                    # Method-level snapshots are only created by notebook_tracker.track_bb84/b92()
                    # to avoid duplicates and ensure accurate time tracking
                    
                    # Log activity
                    firebase_manager.save_activity_log(
                        self.student_id,
                        self.session_id,
                        'snapshot_saved',
                        protocol.upper(),
                        f"Snapshot {snapshot_num}: {snapshot['line_count']} lines, stuck={time_since_last > 180}"
                    )
                except Exception as e:
                    print(f"  Firebase save error: {e}")
            
            print(f"[{timestamp.strftime('%H:%M:%S')}] Snapshot {snapshot_num} saved: {protocol.upper()} - {snapshot['line_count']} lines")
            
            if snapshot_num > 1 and time_since_last > 180:
                print(f"  WARNING: {time_since_last:.0f}s gap - student may be stuck")
            
        except Exception as e:
            print(f"Error saving snapshot: {e}")
    
    def _handle_file_event(self, filepath):
        """Handle file creation or modification"""
        filename = filepath.name
        
        # Check which protocol file was changed
        if filename == 'student_bb84_impl.py':
            if self._should_snapshot('bb84', filepath):
                self._save_snapshot('bb84', filepath)
        
        elif filename == 'student_b92_impl.py':
            if self._should_snapshot('b92', filepath):
                self._save_snapshot('b92', filepath)
    
    def on_created(self, event):
        """Handle file creation events (when %save creates new file)"""
        if event.is_directory:
            return
        
        filepath = Path(event.src_path)
        self._handle_file_event(filepath)
    
    def on_modified(self, event):
        """Handle file modification events"""
        if event.is_directory:
            return
        
        filepath = Path(event.src_path)
        self._handle_file_event(filepath)


def main():
    if len(sys.argv) < 2:
        print("Usage: python watch_student_changes.py <student_id> [interval_seconds]")
        print("Example: python watch_student_changes.py alice 10")
        sys.exit(1)
    
    student_id = sys.argv[1]
    interval = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    # Create watcher
    watcher = StudentCodeWatcher(student_id, interval)
    
    # Set up observer
    observer = Observer()
    observer.schedule(watcher, path='.', recursive=False)
    observer.start()
    
    print(f"\nWatching for changes... Press Ctrl+C to stop\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n\nStopped watching")
        print(f"Total snapshots: BB84={watcher.snapshot_counts['bb84']}, B92={watcher.snapshot_counts['b92']}")
    
    observer.join()


if __name__ == "__main__":
    main()

