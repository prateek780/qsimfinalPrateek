"""
Method-Level Snapshot Tracker
Tracks each method separately for BB84 and B92 protocols
"""
import re
import ast
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import firebase_manager


def extract_methods_from_code(code: str) -> Dict[str, Dict]:
    """
    Extract all methods from code and return dict with method details
    
    Returns:
        {
            'method_name': {
                'code': 'method code',
                'line_start': int,
                'line_end': int,
                'lines': ['line1', 'line2', ...]
            }
        }
    """
    methods = {}
    
    try:
        # Parse code into AST
        tree = ast.parse(code)
        
        # Find all class definitions
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Extract methods from the class
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_name = item.name
                        line_start = item.lineno
                        line_end = item.end_lineno if hasattr(item, 'end_lineno') else line_start
                        
                        # Extract method code
                        code_lines = code.split('\n')
                        method_lines = code_lines[line_start-1:line_end]
                        method_code = '\n'.join(method_lines)
                        
                        methods[method_name] = {
                            'code': method_code,
                            'line_start': line_start,
                            'line_end': line_end,
                            'lines': method_lines,
                            'line_count': len(method_lines),
                            'char_count': len(method_code)
                        }
        
    except SyntaxError:
        # If AST parsing fails, try regex fallback
        methods = extract_methods_regex(code)
    
    return methods


def extract_methods_regex(code: str) -> Dict[str, Dict]:
    """
    Fallback method extraction using regex (for incomplete/invalid syntax)
    """
    methods = {}
    lines = code.split('\n')
    
    current_method = None
    method_start = 0
    method_lines = []
    
    for i, line in enumerate(lines, 1):
        # Check if line starts a method definition
        if re.match(r'\s*def\s+(\w+)\s*\(', line):
            # Save previous method if exists
            if current_method:
                method_code = '\n'.join(method_lines)
                methods[current_method] = {
                    'code': method_code,
                    'line_start': method_start,
                    'line_end': i - 1,
                    'lines': method_lines,
                    'line_count': len(method_lines),
                    'char_count': len(method_code)
                }
            
            # Start new method
            match = re.match(r'\s*def\s+(\w+)\s*\(', line)
            current_method = match.group(1)
            method_start = i
            method_lines = [line]
        
        elif current_method:
            # Check if we're still in the method (indented or blank)
            if line.strip() == '' or line.startswith('    ') or line.startswith('\t'):
                method_lines.append(line)
            else:
                # Method ended, save it
                method_code = '\n'.join(method_lines)
                methods[current_method] = {
                    'code': method_code,
                    'line_start': method_start,
                    'line_end': i - 1,
                    'lines': method_lines,
                    'line_count': len(method_lines),
                    'char_count': len(method_code)
                }
                current_method = None
                method_lines = []
    
    # Save last method if exists
    if current_method:
        method_code = '\n'.join(method_lines)
        methods[current_method] = {
            'code': method_code,
            'line_start': method_start,
            'line_end': len(lines),
            'lines': method_lines,
            'line_count': len(method_lines),
            'char_count': len(method_code)
        }
    
    return methods


def save_method_snapshots(
    student_id: str,
    session_id: str,
    protocol: str,
    code: str,
    previous_methods: Optional[Dict] = None
) -> Dict[str, Dict]:
    """
    Extract methods and save snapshots for each method
    
    Args:
        student_id: Student ID
        session_id: Session ID
        protocol: 'BB84' or 'B92'
        code: Full code string
        previous_methods: Previously extracted methods (for change detection)
    
    Returns:
        Dictionary of current methods
    """
    # Extract all methods from code
    current_methods = extract_methods_from_code(code)
    
    if not current_methods:
        print(f"  No methods found in {protocol} code")
        return {}
    
    # Get Firebase client
    db = firebase_manager.get_firestore()
    
    # Find the most recent method snapshot for this protocol (any method)
    # to calculate time since last method was saved
    activity_logs_ref = (db.collection('students').document(student_id)
                          .collection('sessions').document(session_id)
                          .collection('activity_logs'))
    
    most_recent_time = None
    for doc in activity_logs_ref.stream():
        if doc.id.startswith(f'Snapshot_{protocol}_'):
            data = doc.to_dict()
            snapshots = data.get('snapshots', [])
            if snapshots:
                last_snap = snapshots[-1]
                snap_time = datetime.fromisoformat(last_snap.get('timestamp'))
                if most_recent_time is None or snap_time > most_recent_time:
                    most_recent_time = snap_time
    
    # Track each method separately
    for method_name, method_data in current_methods.items():
        # Check if this specific method already exists
        snapshot_ref = (db.collection('students').document(student_id)
                          .collection('sessions').document(session_id)
                          .collection('activity_logs')
                          .document(f'Snapshot_{protocol}_{method_name}'))
        
        existing_snapshot = snapshot_ref.get()
        
        if existing_snapshot.exists:
            # Method already exists - check if code changed
            existing_data = existing_snapshot.to_dict()
            snapshots_list = existing_data.get('snapshots', [])
            
            if snapshots_list:
                last_snapshot = snapshots_list[-1]
                last_code = '\n'.join(last_snapshot.get('code', []))
                
                # Check if code changed
                if last_code == method_data['code']:
                    # No changes, skip this method
                    continue
                
                # Code changed - calculate time since last snapshot of THIS method
                last_time = datetime.fromisoformat(last_snapshot.get('timestamp'))
                current_time = datetime.now()
                time_spent_seconds = (current_time - last_time).total_seconds()
                minutes = int(time_spent_seconds // 60)
                seconds = int(time_spent_seconds % 60)
                time_spent_str = f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s"
                
                # Calculate line changes
                prev_lines = last_snapshot.get('code', [])
                curr_lines = method_data['lines']
                lines_added = len(curr_lines) - len(prev_lines)
                lines_removed = max(0, len(prev_lines) - len(curr_lines))
                
                changes = {
                    'is_new': False,
                    'lines_added': lines_added,
                    'lines_removed': lines_removed,
                    'time_spent': time_spent_str,
                    'time_spent_seconds': round(time_spent_seconds, 1)
                }
            else:
                # Shouldn't happen, but handle it
                changes = {
                    'is_new': True,
                    'lines_added': method_data['line_count'],
                    'lines_removed': 0,
                    'time_spent': '0s',
                    'time_spent_seconds': 0
                }
        else:
            # New method - calculate time since LAST method was saved (any method)
            if most_recent_time:
                current_time = datetime.now()
                time_spent_seconds = (current_time - most_recent_time).total_seconds()
                minutes = int(time_spent_seconds // 60)
                seconds = int(time_spent_seconds % 60)
                time_spent_str = f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s"
                
                changes = {
                    'is_new': True,
                    'lines_added': method_data['line_count'],
                    'lines_removed': 0,
                    'time_spent': time_spent_str,
                    'time_spent_seconds': round(time_spent_seconds, 1)
                }
            else:
                # Very first method - no previous methods
                changes = {
                    'is_new': True,
                    'lines_added': method_data['line_count'],
                    'lines_removed': 0,
                    'time_spent': '0s',
                    'time_spent_seconds': 0
                }
        
        # Save method snapshot to Firebase
        save_method_snapshot_to_firebase(
            student_id,
            session_id,
            protocol,
            method_name,
            method_data,
            changes
        )
    
    return current_methods


def save_method_snapshot_to_firebase(
    student_id: str,
    session_id: str,
    protocol: str,
    method_name: str,
    method_data: Dict,
    changes: Dict
):
    """
    Save a single method snapshot to Firebase under ActivityLog/Snapshot
    """
    snapshot_data = {
        'protocol': protocol,
        'method_name': method_name,
        'line_start': method_data['line_start'],
        'line_end': method_data['line_end'],
        'code': method_data['lines'],  # Array of code lines
        'line_count': method_data['line_count'],
        'char_count': method_data['char_count'],
        'changes': changes,
        'timestamp': datetime.now().isoformat(),
        'is_new_method': changes['is_new']
    }
    
    # Get Firestore client
    db = firebase_manager.get_firestore()
    
    # Save to: students/{student_id}/sessions/{session_id}/activity_logs/Snapshot_{protocol}_{method_name}
    snapshot_ref = (db.collection('students').document(student_id)
                      .collection('sessions').document(session_id)
                      .collection('activity_logs')
                      .document(f'Snapshot_{protocol}_{method_name}'))
    
    # Check if snapshot already exists
    existing_snapshot = snapshot_ref.get()
    
    if existing_snapshot.exists:
        # Append to snapshots array
        existing_data = existing_snapshot.to_dict()
        snapshots_list = existing_data.get('snapshots', [])
        snapshots_list.append({
            **snapshot_data,
            'snapshot_number': len(snapshots_list) + 1
        })
        
        snapshot_ref.update({
            'snapshots': snapshots_list,
            'last_updated': datetime.now().isoformat(),
            'total_snapshots': len(snapshots_list)
        })
    else:
        # Create new snapshot document
        snapshot_ref.set({
            'protocol': protocol,
            'method_name': method_name,
            'snapshots': [{
                **snapshot_data,
                'snapshot_number': 1
            }],
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'total_snapshots': 1
        })
    
    print(f"  Snapshot saved: {protocol}.{method_name} ({method_data['line_count']} lines)")


def get_method_snapshots(student_id: str, session_id: str, protocol: str) -> Dict:
    """
    Retrieve all method snapshots for a protocol
    
    Returns:
        {
            'method_name': {
                'snapshots': [...],
                'total_snapshots': int
            }
        }
    """
    db = firebase_manager.get_firestore()
    
    # Query all Snapshot documents for this protocol
    activity_logs_ref = (db.collection('students').document(student_id)
                           .collection('sessions').document(session_id)
                           .collection('activity_logs'))
    
    snapshots_data = {}
    
    for doc in activity_logs_ref.stream():
        doc_id = doc.id
        if doc_id.startswith(f'Snapshot_{protocol}_'):
            data = doc.to_dict()
            method_name = data.get('method_name')
            snapshots_data[method_name] = data
    
    return snapshots_data

