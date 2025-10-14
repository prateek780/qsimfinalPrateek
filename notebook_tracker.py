"""
Simple Notebook Activity Tracker
Tracks student vibe coding cells for BB84 and B92 protocols
Saves to Firebase cloud database and local JSON backups
"""
import json
import os
from datetime import datetime
from pathlib import Path

# Import Firebase module
try:
    import firebase_manager
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    print("Warning: Firebase module not available. Saving to JSON only.")


class NotebookTracker:
    """Tracks student coding activity in notebook cells"""
    
    def __init__(self, student_id, use_firebase=True):
        self.student_id = student_id
        self.use_firebase = use_firebase and FIREBASE_AVAILABLE
        self.session_id = None
        
        # Initialize Firebase if available
        if self.use_firebase:
            try:
                # Initialize Firebase
                print("Step 1/3: Initializing Firebase connection...")
                firebase_manager.init_firebase()
                
                # Get or create student
                print(f"Step 2/3: Setting up student record ({student_id})...")
                firebase_manager.get_or_create_student(student_id)
                print("  > Student record ready")
                
                # Create new session
                print("Step 3/3: Creating session...")
                self.session_id = firebase_manager.create_session(student_id)
                
                print(f"SUCCESS: Firebase fully connected - Session ID: {self.session_id}")
            except Exception as e:
                print(f"Firebase error: {e}")
                print("Falling back to JSON-only mode")
                self.use_firebase = False
        
        # Setup local JSON logging (always keep as backup)
        self.log_dir = Path("student_logs")
        self.log_dir.mkdir(exist_ok=True)
        self.session_file = self.log_dir / f"{student_id}_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.session_data = {
            "student_id": student_id,
            "session_id": self.session_id,
            "session_start": datetime.now().isoformat(),
            "activities": [],
            "firebase_enabled": self.use_firebase
        }
        
    def track_cell(self, protocol, cell_code, output=""):
        """Track a single cell execution"""
        # Save code as array of lines for better readability in JSON
        code_lines = cell_code.split('\n')
        
        activity = {
            "protocol": protocol,
            "timestamp": datetime.now().isoformat(),
            "code": code_lines,  # Store as array of lines
            "output": str(output),
            "code_length": len(cell_code),
            "line_count": len(code_lines)
        }
        
        # Save to local JSON
        self.session_data["activities"].append(activity)
        self._save()
        
        # Save to Firebase
        if self.use_firebase and self.session_id:
            try:
                # Save code version to Firebase
                firebase_manager.save_code_version(
                    self.student_id,
                    self.session_id,
                    protocol,
                    code_lines,  # Firebase saves as array of lines
                    len(code_lines),
                    len(cell_code)
                )
                
                # Log activity
                firebase_manager.save_activity_log(
                    self.student_id,
                    self.session_id,
                    'code_tracked',
                    protocol,
                    f"{protocol} code tracked: {len(code_lines)} lines"
                )
                
                print(f"Tracked {protocol} cell: {activity['line_count']} lines, {activity['code_length']} chars")
                
            except Exception as e:
                print(f"Firebase save error: {e}")
        
    def _save(self):
        """Save session data to JSON file"""
        self.session_data["last_updated"] = datetime.now().isoformat()
        with open(self.session_file, 'w', encoding='utf-8') as f:
            json.dump(self.session_data, f, indent=2, ensure_ascii=False)
    
    def get_summary(self):
        """Get session summary"""
        bb84_count = sum(1 for a in self.session_data["activities"] if a["protocol"] == "BB84")
        b92_count = sum(1 for a in self.session_data["activities"] if a["protocol"] == "B92")
        
        return {
            "student_id": self.student_id,
            "total_activities": len(self.session_data["activities"]),
            "bb84_attempts": bb84_count,
            "b92_attempts": b92_count,
            "session_file": str(self.session_file)
        }


# Global tracker instance
_tracker = None
_session_id = None
_student_id = None

def init_tracker(student_id, use_firebase=True):
    """Initialize the tracker for a student"""
    global _tracker, _session_id, _student_id
    
    _student_id = student_id
    _tracker = NotebookTracker(student_id, use_firebase=use_firebase)
    _session_id = _tracker.session_id
    
    print("=" * 60)
    print(f"TRACKING STARTED FOR STUDENT: {student_id}")
    print("=" * 60)
    
    if _tracker.use_firebase:
        print(f"Firebase: Connected (Session ID: {_session_id})")
        print("Cloud Storage: All data saved to Firebase")
    else:
        print("Firebase: Not available (JSON-only mode)")
    
    print(f"Backup JSON: {_tracker.session_file}")
    print("\nYour vibe coding will be automatically tracked.")
    print("Code in BB84 and B92 cells will be logged on each run.\n")
    return _tracker

def get_session_id():
    """Get the current session ID"""
    return _session_id

def get_student_id():
    """Get the current student ID"""
    return _student_id

def track(protocol, code, output=""):
    """Track a cell execution"""
    if _tracker is None:
        print("⚠️ Tracker not initialized. Please run the setup cell first.")
        return
    _tracker.track_cell(protocol, code, output)

def get_tracker():
    """Get the current tracker instance"""
    return _tracker

def verify_file_updated(protocol):
    """Check if implementation file exists and was recently modified"""
    import time
    from pathlib import Path
    
    filename = f'student_{protocol.lower()}_impl.py'
    filepath = Path(filename)
    
    if not filepath.exists():
        return False, f"File {filename} not found. Did you run %save?"
    
    # Check if file was modified in last 60 seconds
    mod_time = filepath.stat().st_mtime
    age = time.time() - mod_time
    
    if age > 60:
        return False, f"File {filename} is {age:.0f}s old. Run %save again to update it."
    
    # Check if file is not empty
    if filepath.stat().st_size == 0:
        return False, f"File {filename} is empty. Make sure %save captured your code."
    
    return True, "File verified"

def _clean_code(code):
    """Remove PROMPT sections and keep only actual code"""
    import re
    
    # Remove # PROMPT comment lines first
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
                # Single-line docstring - check if it's a prompt
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
            # Check the next few lines for prompt keywords
            for j in range(i, min(i + 10, len(lines))):
                next_line_lower = lines[j].lower()
                if any(keyword in next_line_lower for keyword in ['implement', 'prompt', 'skeleton', 'constructor', 'method should']):
                    is_prompt = True
                    break
                if delimiter in lines[j] and j > i:  # Found closing delimiter
                    break
            
            if is_prompt:
                # Skip until we find the closing delimiter
                skip_docstring = True
                docstring_delimiter = delimiter
                i += 1
                continue
            else:
                # Not a prompt docstring, keep it
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

def _save_snapshot_from_tracker(protocol, code):
    """Helper function to save method-level snapshots when tracking code"""
    if _tracker is None or not _tracker.use_firebase or not _tracker.session_id:
        return
    
    try:
        # Import method snapshot tracker
        import method_snapshot_tracker
        
        # Extract and save snapshots for each method
        print(f"\nCreating method-level snapshots for {protocol}:")
        methods = method_snapshot_tracker.save_method_snapshots(
            _tracker.student_id,
            _tracker.session_id,
            protocol,
            code,
            previous_methods=None  # TODO: Track previous state
        )
        
        print(f"Total methods tracked: {len(methods)}")
        
        # Full code snapshots are handled by the background watcher
        # We only create method-level snapshots here
        
        # Log the snapshot creation
        firebase_manager.save_activity_log(
            _tracker.student_id,
            _tracker.session_id,
            'method_snapshots_saved',
            protocol,
            f"{protocol} method snapshots: {len(methods)} methods tracked"
        )
    except Exception as e:
        print(f"Snapshot save error: {e}")
        import traceback
        traceback.print_exc()

def track_bb84(code=None, validate=True):
    """
    Track the BB84 cell - call this after defining StudentQuantumHost
    
    Usage:
        Method 1: notebook_tracker.track_bb84()  # Reads from student_bb84_impl.py
        Method 2: notebook_tracker.track_bb84('''your code here''')  # Pass code directly
    """
    if _tracker is None:
        print("⚠️ Tracker not initialized. Please run Cell 7 (Setup) first.")
        return
    
    try:
        # If code is provided directly, use it
        if code is not None:
            cleaned_code = _clean_code(code)
            _tracker.track_cell("BB84", cleaned_code)
            _save_snapshot_from_tracker("BB84", cleaned_code)
            print("✓ BB84 code tracked and snapshot saved!")
            print("\n⏱️ WAIT 5 SECONDS before continuing to next method!")
            return
        
        # Validate file if requested
        if validate:
            ok, msg = verify_file_updated('BB84')
            if not ok:
                print(f"⚠️ {msg}")
                return
        
        # Try to read from the student implementation file
        from pathlib import Path
        bb84_file = Path("student_bb84_impl.py")
        
        if bb84_file.exists():
            with open(bb84_file, 'r', encoding='utf-8') as f:
                code = f.read()
            # Clean the code to remove prompts
            cleaned_code = _clean_code(code)
            _tracker.track_cell("BB84", cleaned_code)
            _save_snapshot_from_tracker("BB84", cleaned_code)
            print(f"✓ BB84 code tracked from student_bb84_impl.py")
            print(f"✓ Snapshot saved to Firebase")
            print(f"\n{'='*60}")
            print(f"⏱️ WAIT 5 SECONDS BEFORE CONTINUING!")
            print(f"{'='*60}")
            print("This allows the background watcher to capture your progress.")
        else:
            print("✗ ERROR: student_bb84_impl.py not found")
            print("\nDid you forget to save your code?")
            print("Run: %save -f student_bb84_impl.py <cell_number>")
    except Exception as e:
        print(f"✗ ERROR: Could not track BB84: {e}")

def track_b92(code=None, validate=True):
    """
    Track the B92 cell - call this after defining StudentB92Host
    
    Usage:
        Method 1: notebook_tracker.track_b92()  # Reads from student_b92_impl.py
        Method 2: notebook_tracker.track_b92('''your code here''')  # Pass code directly
    """
    if _tracker is None:
        print("⚠️ Tracker not initialized. Please run Cell 7 (Setup) first.")
        return
    
    try:
        # If code is provided directly, use it
        if code is not None:
            cleaned_code = _clean_code(code)
            _tracker.track_cell("B92", cleaned_code)
            _save_snapshot_from_tracker("B92", cleaned_code)
            print("✓ B92 code tracked and snapshot saved!")
            print("\n⏱️ WAIT 5 SECONDS before continuing to next method!")
            return
        
        # Validate file if requested
        if validate:
            ok, msg = verify_file_updated('B92')
            if not ok:
                print(f"⚠️ {msg}")
                return
        
        # Try to read from the student implementation file
        from pathlib import Path
        b92_file = Path("student_b92_impl.py")
        
        if b92_file.exists():
            with open(b92_file, 'r', encoding='utf-8') as f:
                code = f.read()
            # Clean the code to remove prompts
            cleaned_code = _clean_code(code)
            _tracker.track_cell("B92", cleaned_code)
            _save_snapshot_from_tracker("B92", cleaned_code)
            print(f"✓ B92 code tracked from student_b92_impl.py")
            print(f"✓ Snapshot saved to Firebase")
            print(f"\n{'='*60}")
            print(f"⏱️ WAIT 5 SECONDS BEFORE CONTINUING!")
            print(f"{'='*60}")
            print("This allows the background watcher to capture your progress.")
        else:
            print("✗ ERROR: student_b92_impl.py not found")
            print("\nDid you forget to save your code?")
            print("Run: %save -f student_b92_impl.py <cell_number>")
    except Exception as e:
        print(f"✗ ERROR: Could not track B92: {e}")

