"""
Firebase Manager for Student Activity Tracking
Replaces SQLite with Firebase Firestore for cloud storage
"""
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    print("Warning: firebase-admin not installed. Run: pip install firebase-admin")


# Global Firebase app and db
_firebase_app = None
_firestore_db = None
_credentials_path = "firebase-credentials.json"


def init_firebase():
    """Initialize Firebase connection"""
    global _firebase_app, _firestore_db
    
    if not FIREBASE_AVAILABLE:
        raise ImportError("firebase-admin not installed. Run: pip install firebase-admin")
    
    if _firebase_app is not None:
        return _firestore_db
    
    # Check if credentials file exists
    if not os.path.exists(_credentials_path):
        raise FileNotFoundError(
            f"Firebase credentials not found: {_credentials_path}\n"
            f"Please download from Firebase Console and save as {_credentials_path}\n"
            f"See FIREBASE_SETUP_INSTRUCTIONS.txt for details"
        )
    
    try:
        # Initialize Firebase
        cred = credentials.Certificate(_credentials_path)
        _firebase_app = firebase_admin.initialize_app(cred)
        _firestore_db = firestore.client()
        
        print(f"Firebase connected: qsimnotebookfinal-e73e9")
        return _firestore_db
        
    except Exception as e:
        raise Exception(f"Failed to initialize Firebase: {e}")


def get_firestore():
    """Get Firestore database instance"""
    if _firestore_db is None:
        return init_firebase()
    return _firestore_db


def get_or_create_student(student_id: str, name: Optional[str] = None, email: Optional[str] = None) -> Dict:
    """
    Get existing student or create new one in Firestore
    Returns student record
    """
    db = get_firestore()
    student_ref = db.collection('students').document(student_id)
    student_doc = student_ref.get()
    
    if student_doc.exists:
        return student_doc.to_dict()
    else:
        # Create new student
        student_data = {
            'student_id': student_id,
            'name': name or student_id,
            'email': email,
            'created_at': firestore.SERVER_TIMESTAMP,
            'last_activity': firestore.SERVER_TIMESTAMP
        }
        student_ref.set(student_data)
        return student_data


def create_session(student_id: str) -> str:
    """
    Create a new session for a student
    Returns session ID
    """
    db = get_firestore()
    
    # Update student's last activity
    student_ref = db.collection('students').document(student_id)
    student_ref.update({'last_activity': firestore.SERVER_TIMESTAMP})
    
    # Create session
    session_data = {
        'student_id': student_id,
        'started_at': firestore.SERVER_TIMESTAMP,
        'status': 'active'
    }
    
    session_ref = student_ref.collection('sessions').document()
    session_ref.set(session_data)
    
    return session_ref.id


def save_code_version(
    student_id: str,
    session_id: str,
    protocol: str,
    code_content: List[str],
    line_count: int,
    char_count: int
) -> str:
    """
    Save a code version to Firestore
    Returns version ID
    """
    db = get_firestore()
    
    version_data = {
        'protocol': protocol,
        'code': code_content,  # Array of code lines
        'line_count': line_count,
        'char_count': char_count,
        'timestamp': firestore.SERVER_TIMESTAMP,
        'created_at': datetime.now().isoformat()
    }
    
    # Save to student → session → code_versions
    version_ref = (db.collection('students').document(student_id)
                     .collection('sessions').document(session_id)
                     .collection('code_versions').document())
    
    version_ref.set(version_data)
    
    return version_ref.id


def save_snapshot(
    student_id: str,
    session_id: str,
    protocol: str,
    code_content: List[str],
    line_count: int,
    char_count: int,
    changes_detected: Optional[str] = None
) -> str:
    """
    Save a code snapshot to Firestore
    Returns snapshot ID
    """
    db = get_firestore()
    
    snapshot_data = {
        'protocol': protocol,
        'code': code_content,  # Array of code lines
        'line_count': line_count,
        'char_count': char_count,
        'changes_detected': changes_detected,
        'timestamp': firestore.SERVER_TIMESTAMP,
        'created_at': datetime.now().isoformat()
    }
    
    # Save to student → session → snapshots
    snapshot_ref = (db.collection('students').document(student_id)
                      .collection('sessions').document(session_id)
                      .collection('snapshots').document())
    
    snapshot_ref.set(snapshot_data)
    
    return snapshot_ref.id


def save_activity_log(
    student_id: str,
    session_id: str,
    activity_type: str,
    protocol: Optional[str] = None,
    details: Optional[str] = None
) -> str:
    """
    Save an activity log entry
    Returns log ID
    """
    db = get_firestore()
    
    log_data = {
        'activity_type': activity_type,  # e.g., 'code_tracked', 'snapshot_saved'
        'protocol': protocol,
        'details': details,
        'timestamp': firestore.SERVER_TIMESTAMP,
        'created_at': datetime.now().isoformat()
    }
    
    # Save to student → session → activity_logs
    log_ref = (db.collection('students').document(student_id)
                 .collection('sessions').document(session_id)
                 .collection('activity_logs').document())
    
    log_ref.set(log_data)
    
    return log_ref.id


def get_all_students() -> List[Dict]:
    """Get all students from Firestore"""
    db = get_firestore()
    students = []
    
    for doc in db.collection('students').stream():
        student_data = doc.to_dict()
        student_data['student_id'] = doc.id
        students.append(student_data)
    
    return students


def get_student_sessions(student_id: str) -> List[Dict]:
    """Get all sessions for a student"""
    db = get_firestore()
    sessions = []
    
    session_ref = (db.collection('students').document(student_id)
                     .collection('sessions'))
    
    for doc in session_ref.stream():
        session_data = doc.to_dict()
        session_data['session_id'] = doc.id
        sessions.append(session_data)
    
    return sessions


def get_code_versions(student_id: str, session_id: str, protocol: Optional[str] = None) -> List[Dict]:
    """Get code versions for a student session"""
    db = get_firestore()
    versions = []
    
    versions_ref = (db.collection('students').document(student_id)
                       .collection('sessions').document(session_id)
                       .collection('code_versions'))
    
    # Get all versions without ordering (to avoid index requirement)
    for doc in versions_ref.stream():
        version_data = doc.to_dict()
        version_data['version_id'] = doc.id
        versions.append(version_data)
    
    # Filter by protocol in Python if specified
    if protocol:
        versions = [v for v in versions if v.get('protocol') == protocol]
    
    # Sort by created_at in Python
    versions.sort(key=lambda x: x.get('created_at', ''))
    
    return versions


def get_snapshots(student_id: str, session_id: str, protocol: Optional[str] = None) -> List[Dict]:
    """Get snapshots for a student session"""
    db = get_firestore()
    snapshots = []
    
    snapshots_ref = (db.collection('students').document(student_id)
                        .collection('sessions').document(session_id)
                        .collection('snapshots'))
    
    # Get all snapshots without ordering (to avoid index requirement)
    for doc in snapshots_ref.stream():
        snapshot_data = doc.to_dict()
        snapshot_data['snapshot_id'] = doc.id
        snapshots.append(snapshot_data)
    
    # Filter by protocol in Python if specified
    if protocol:
        snapshots = [s for s in snapshots if s.get('protocol') == protocol]
    
    # Sort by created_at in Python
    snapshots.sort(key=lambda x: x.get('created_at', ''))
    
    return snapshots


def get_activity_logs(student_id: str, session_id: str) -> List[Dict]:
    """Get activity logs for a student session"""
    db = get_firestore()
    logs = []
    
    logs_ref = (db.collection('students').document(student_id)
                   .collection('sessions').document(session_id)
                   .collection('activity_logs'))
    
    # Get all logs without ordering (to avoid index requirement)
    for doc in logs_ref.stream():
        log_data = doc.to_dict()
        log_data['log_id'] = doc.id
        logs.append(log_data)
    
    # Sort by created_at in Python
    logs.sort(key=lambda x: x.get('created_at', ''))
    
    return logs


def analyze_stuck_periods(snapshots: List[Dict], threshold_minutes: int = 3) -> List[Dict]:
    """
    Analyze snapshots to find periods where student got stuck
    Returns list of stuck periods with duration and code state
    """
    stuck_periods = []
    
    if len(snapshots) < 2:
        return stuck_periods
    
    for i in range(len(snapshots) - 1):
        current = snapshots[i]
        next_snap = snapshots[i + 1]
        
        # Parse timestamps
        current_time = datetime.fromisoformat(current['created_at'].replace('Z', '+00:00'))
        next_time = datetime.fromisoformat(next_snap['created_at'].replace('Z', '+00:00'))
        
        # Calculate gap in minutes
        gap_minutes = (next_time - current_time).total_seconds() / 60
        
        # Check if code didn't change much but time gap is large
        current_code = '\n'.join(current['code'])
        next_code = '\n'.join(next_snap['code'])
        
        if gap_minutes >= threshold_minutes and current_code == next_code:
            stuck_periods.append({
                'start_time': current['created_at'],
                'end_time': next_snap['created_at'],
                'duration_minutes': round(gap_minutes, 1),
                'code_state': current['code'][:10],  # First 10 lines
                'protocol': current['protocol']
            })
    
    return stuck_periods


def analyze_ai_usage(snapshots: List[Dict]) -> List[Dict]:
    """
    Detect potential AI-assisted code generation
    Returns list of events where large code changes appeared suddenly
    """
    ai_events = []
    
    if len(snapshots) < 2:
        return ai_events
    
    for i in range(len(snapshots) - 1):
        current = snapshots[i]
        next_snap = snapshots[i + 1]
        
        # Parse timestamps
        current_time = datetime.fromisoformat(current['created_at'].replace('Z', '+00:00'))
        next_time = datetime.fromisoformat(next_snap['created_at'].replace('Z', '+00:00'))
        
        # Calculate time gap and line change
        time_gap_seconds = (next_time - current_time).total_seconds()
        line_diff = next_snap['line_count'] - current['line_count']
        
        # Detect sudden large additions (>20 lines in <30 seconds)
        if line_diff > 20 and time_gap_seconds < 30:
            ai_events.append({
                'timestamp': next_snap['created_at'],
                'lines_added': line_diff,
                'time_gap_seconds': round(time_gap_seconds, 1),
                'protocol': next_snap['protocol'],
                'likelihood': 'HIGH' if line_diff > 50 else 'MEDIUM'
            })
    
    return ai_events


# Firestore structure:
# students/
#   {student_id}/
#     - student_id, name, email, created_at, last_activity
#     sessions/
#       {session_id}/
#         - student_id, started_at, status
#         code_versions/
#           {version_id}/
#             - protocol, code[], line_count, char_count, timestamp
#         snapshots/
#           {snapshot_id}/
#             - protocol, code[], line_count, char_count, changes_detected, timestamp
#         activity_logs/
#           {log_id}/
#             - activity_type, protocol, details, timestamp

