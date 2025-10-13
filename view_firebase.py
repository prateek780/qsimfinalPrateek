#!/usr/bin/env python3
"""
Firebase Student Activity Viewer (for Instructors)
View and analyze student coding activity stored in Firebase
"""
import sys
import json
import firebase_manager
from datetime import datetime


def list_students():
    """List all students in Firebase"""
    try:
        students = firebase_manager.get_all_students()
        
        if not students:
            print("No students found in Firebase")
            return
        
        print("\n" + "=" * 80)
        print(f"ALL STUDENTS ({len(students)} total)")
        print("=" * 80)
        
        for idx, student in enumerate(students, 1):
            student_id = student['student_id']
            
            # Get session count
            sessions = firebase_manager.get_student_sessions(student_id)
            session_count = len(sessions) if sessions else 0
            
            # Get code version counts
            bb84_count = 0
            b92_count = 0
            snapshot_count = 0
            
            for session in sessions:
                session_id = session['session_id']
                bb84_versions = firebase_manager.get_code_versions(student_id, session_id, 'BB84')
                b92_versions = firebase_manager.get_code_versions(student_id, session_id, 'B92')
                snapshots = firebase_manager.get_snapshots(student_id, session_id)
                
                bb84_count += len(bb84_versions)
                b92_count += len(b92_versions)
                snapshot_count += len(snapshots)
            
            # Format timestamp
            created = student.get('created_at', 'N/A')
            if created != 'N/A':
                try:
                    dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                    created = dt.strftime('%b %d, %Y')
                except:
                    pass
            
            print(f"\n[{idx}] {student_id}")
            print(f"    Sessions:  {session_count}")
            print(f"    BB84 code: {bb84_count} version(s)")
            print(f"    B92 code:  {b92_count} version(s)")
            print(f"    Snapshots: {snapshot_count}")
            print(f"    Created:   {created}")
        
        print("\n" + "=" * 80)
        print("\nTo view details: python view_firebase.py student <student_id>")
        print("To view code:    python view_firebase.py code <student_id> <BB84|B92>")
        print("To view snaps:   python view_firebase.py snapshots <student_id> <BB84|B92>")
        print("=" * 80)
        
    except Exception as e:
        print(f"Error listing students: {e}")


def view_student_detail(student_id):
    """View detailed activity for a specific student"""
    try:
        # Get all sessions
        sessions = firebase_manager.get_student_sessions(student_id)
        
        if not sessions:
            print(f"\nNo sessions found for student: {student_id}")
            return
        
        print("\n" + "=" * 80)
        print(f"STUDENT ACTIVITY SUMMARY: {student_id}")
        print("=" * 80)
        
        total_bb84 = 0
        total_b92 = 0
        total_snapshots = 0
        
        for idx, session in enumerate(sessions, 1):
            session_id = session['session_id']
            
            # Format timestamp
            started = session.get('started_at', 'N/A')
            if started != 'N/A':
                try:
                    dt = datetime.fromisoformat(started.replace('Z', '+00:00'))
                    started = dt.strftime('%b %d, %Y at %I:%M %p')
                except:
                    pass
            
            print(f"\n{'-' * 80}")
            print(f"Session {idx}")
            print(f"Started: {started}")
            print(f"Status:  {session.get('status', 'N/A')}")
            
            # Get code versions with protocol breakdown
            bb84_versions = firebase_manager.get_code_versions(student_id, session_id, 'BB84')
            b92_versions = firebase_manager.get_code_versions(student_id, session_id, 'B92')
            
            print(f"\nCode Submissions:")
            print(f"  BB84: {len(bb84_versions)} version(s)")
            for v in bb84_versions:
                print(f"    - {v['line_count']} lines, {v['char_count']} chars")
            
            print(f"  B92:  {len(b92_versions)} version(s)")
            for v in b92_versions:
                print(f"    - {v['line_count']} lines, {v['char_count']} chars")
            
            # Get snapshots with protocol breakdown
            bb84_snaps = firebase_manager.get_snapshots(student_id, session_id, 'BB84')
            b92_snaps = firebase_manager.get_snapshots(student_id, session_id, 'B92')
            
            print(f"\nCode Evolution Snapshots:")
            print(f"  BB84: {len(bb84_snaps)} snapshot(s)")
            print(f"  B92:  {len(b92_snaps)} snapshot(s)")
            
            # Analyze progress
            if bb84_snaps:
                first_snap = bb84_snaps[0]
                last_snap = bb84_snaps[-1]
                print(f"\n  BB84 Progress:")
                print(f"    Started with:  {first_snap['line_count']} lines")
                print(f"    Ended with:    {last_snap['line_count']} lines")
                print(f"    Growth:        +{last_snap['line_count'] - first_snap['line_count']} lines")
            
            if b92_snaps:
                first_snap = b92_snaps[0]
                last_snap = b92_snaps[-1]
                print(f"\n  B92 Progress:")
                print(f"    Started with:  {first_snap['line_count']} lines")
                print(f"    Ended with:    {last_snap['line_count']} lines")
                print(f"    Growth:        +{last_snap['line_count'] - first_snap['line_count']} lines")
            
            # Get activity logs
            logs = firebase_manager.get_activity_logs(student_id, session_id)
            print(f"\nActivity Logs: {len(logs)}")
            
            total_bb84 += len(bb84_versions)
            total_b92 += len(b92_versions)
            total_snapshots += len(bb84_snaps) + len(b92_snaps)
        
        print("\n" + "=" * 80)
        print(f"TOTALS: {total_bb84} BB84, {total_b92} B92, {total_snapshots} snapshots")
        print("=" * 80)
        
    except Exception as e:
        print(f"Error viewing student: {e}")


def view_code_history(student_id, protocol=None):
    """View code evolution for a student"""
    try:
        sessions = firebase_manager.get_student_sessions(student_id)
        
        if not sessions:
            print(f"\nNo sessions found for student: {student_id}")
            return
        
        print("\n" + "=" * 80)
        print(f"CODE EVOLUTION: {student_id}" + (f" - {protocol}" if protocol else ""))
        print("=" * 80)
        
        all_versions = []
        for session in sessions:
            session_id = session['session_id']
            versions = firebase_manager.get_code_versions(student_id, session_id, protocol)
            all_versions.extend(versions)
        
        if not all_versions:
            print("\nNo code versions found")
            return
        
        print(f"\nTotal Versions: {len(all_versions)}")
        
        for i, version in enumerate(all_versions, 1):
            timestamp = version.get('created_at', 'N/A')
            if timestamp != 'N/A':
                try:
                    # Parse and format timestamp nicely
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    time_str = dt.strftime('%b %d, %Y at %I:%M:%S %p')
                except:
                    time_str = timestamp
            else:
                time_str = 'N/A'
            
            print(f"\n{'-' * 80}")
            print(f"Version {i} - {version['protocol']}")
            print(f"Time: {time_str}")
            print(f"Size: {version['line_count']} lines, {version['char_count']} characters")
            
            code_lines = version.get('code', [])
            
            # Show key class/function definitions
            print(f"\nCode Structure:")
            for j, line in enumerate(code_lines[:50], 1):
                stripped = line.strip()
                if stripped.startswith('class ') or stripped.startswith('def '):
                    print(f"  Line {j:3}: {line[:70]}")
            
            print(f"\nCode Preview (first 15 lines):")
            for j, line in enumerate(code_lines[:15], 1):
                print(f"  {j:3} | {line}")
            
            if len(code_lines) > 15:
                print(f"  ... | ({len(code_lines) - 15} more lines)")
                print(f"  {len(code_lines):3} | {code_lines[-1]}")
        
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"Error viewing code history: {e}")


def view_snapshots(student_id, protocol=None):
    """View all snapshots for a student"""
    try:
        sessions = firebase_manager.get_student_sessions(student_id)
        
        if not sessions:
            print(f"\nNo sessions found for student: {student_id}")
            return
        
        print("\n" + "=" * 80)
        print(f"SNAPSHOTS: {student_id}" + (f" - {protocol}" if protocol else ""))
        print("=" * 80)
        
        all_snapshots = []
        for session in sessions:
            session_id = session['session_id']
            snapshots = firebase_manager.get_snapshots(student_id, session_id, protocol)
            all_snapshots.extend(snapshots)
        
        if not all_snapshots:
            print("\nNo snapshots found")
            return
        
        print(f"\nTotal Snapshots: {len(all_snapshots)}")
        
        for i, snap in enumerate(all_snapshots, 1):
            timestamp = snap.get('created_at', 'N/A')
            if timestamp != 'N/A':
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    time_str = dt.strftime('%b %d, %Y at %I:%M:%S %p')
                except:
                    time_str = timestamp
            else:
                time_str = 'N/A'
            
            print(f"\n{'-' * 80}")
            print(f"Snapshot {i} - {snap['protocol']}")
            print(f"Time: {time_str}")
            print(f"Size: {snap['line_count']} lines, {snap['char_count']} characters")
            
            # Parse and display changes
            if snap.get('changes_detected'):
                try:
                    changes = json.loads(snap['changes_detected'])
                    time_seconds = changes.get('time_spent_seconds', 0)
                    
                    print(f"\nChanges Since Last Snapshot:")
                    print(f"  Lines added:   {changes.get('lines_added', 0):4}")
                    print(f"  Lines removed: {changes.get('lines_removed', 0):4}")
                    print(f"  Time spent:    {changes.get('time_spent', 'N/A')}")
                    
                    # Analyze what happened
                    if time_seconds > 300:
                        print(f"  [ALERT] Long gap detected - student may be stuck ({time_seconds:.0f}s)")
                    elif time_seconds < 10 and changes.get('lines_added', 0) > 20:
                        print(f"  [ALERT] Large code addition in short time - possible AI usage")
                    elif 60 < time_seconds < 180:
                        print(f"  [OK] Normal coding pace")
                    
                except json.JSONDecodeError:
                    print(f"\nChanges: {snap['changes_detected']}")
            
            # Show code structure if available
            code_lines = snap.get('code', [])
            if code_lines:
                print(f"\nCode Structure:")
                class_count = 0
                method_count = 0
                for line in code_lines[:30]:
                    stripped = line.strip()
                    if stripped.startswith('class '):
                        class_count += 1
                        print(f"  {stripped[:60]}")
                    elif stripped.startswith('def '):
                        method_count += 1
                        print(f"    {stripped[:60]}")
                
                print(f"\nComplexity: {class_count} class(es), {method_count} method(s)")
        
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"Error viewing snapshots: {e}")


def analyze_stuck_periods(student_id):
    """Analyze periods where student got stuck"""
    try:
        sessions = firebase_manager.get_student_sessions(student_id)
        
        if not sessions:
            print(f"\nNo sessions found for student: {student_id}")
            return
        
        print("\n" + "=" * 80)
        print(f"STUCK PERIODS ANALYSIS: {student_id}")
        print("=" * 80)
        
        all_snapshots = []
        for session in sessions:
            session_id = session['session_id']
            snapshots = firebase_manager.get_snapshots(student_id, session_id)
            all_snapshots.extend(snapshots)
        
        if len(all_snapshots) < 2:
            print("\nNot enough snapshots for analysis (need at least 2)")
            return
        
        stuck_periods = firebase_manager.analyze_stuck_periods(all_snapshots)
        
        if not stuck_periods:
            print("\nNo stuck periods detected (gaps > 3 minutes with no code changes)")
            return
        
        print(f"\nFound {len(stuck_periods)} stuck periods:")
        
        for i, period in enumerate(stuck_periods, 1):
            print(f"\n--- Stuck Period {i} ---")
            print(f"Protocol: {period['protocol']}")
            print(f"Start: {period['start_time']}")
            print(f"End: {period['end_time']}")
            print(f"Duration: {period['duration_minutes']} minutes")
            print(f"Code state (first 5 lines):")
            for j, line in enumerate(period['code_state'][:5], 1):
                print(f"  {j}: {line}")
        
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"Error analyzing stuck periods: {e}")


def analyze_ai_usage(student_id):
    """Detect potential AI-assisted code generation"""
    try:
        sessions = firebase_manager.get_student_sessions(student_id)
        
        if not sessions:
            print(f"\nNo sessions found for student: {student_id}")
            return
        
        print("\n" + "=" * 80)
        print(f"AI USAGE ANALYSIS: {student_id}")
        print("=" * 80)
        
        all_snapshots = []
        for session in sessions:
            session_id = session['session_id']
            snapshots = firebase_manager.get_snapshots(student_id, session_id)
            all_snapshots.extend(snapshots)
        
        if len(all_snapshots) < 2:
            print("\nNot enough snapshots for analysis (need at least 2)")
            return
        
        ai_events = firebase_manager.analyze_ai_usage(all_snapshots)
        
        if not ai_events:
            print("\nNo AI-assisted events detected (large code additions in short time)")
            return
        
        print(f"\nFound {len(ai_events)} potential AI-assisted events:")
        
        for i, event in enumerate(ai_events, 1):
            print(f"\n--- Event {i} ---")
            print(f"Protocol: {event['protocol']}")
            print(f"Time: {event['timestamp']}")
            print(f"Lines Added: {event['lines_added']}")
            print(f"Time Gap: {event['time_gap_seconds']} seconds")
            print(f"AI Likelihood: {event['likelihood']}")
        
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"Error analyzing AI usage: {e}")


def print_usage():
    """Print usage instructions"""
    print("""
Firebase Student Activity Viewer (for Instructors)

Usage:
  python view_firebase.py list                        List all students
  python view_firebase.py view <student_id>           View student details
  python view_firebase.py code <student_id> [protocol] View code history
  python view_firebase.py snapshots <student_id> [protocol] View snapshots
  python view_firebase.py stuck <student_id>          Analyze stuck periods
  python view_firebase.py ai <student_id>             Analyze AI usage

Examples:
  python view_firebase.py list
  python view_firebase.py view alice
  python view_firebase.py code alice BB84
  python view_firebase.py snapshots bob B92
  python view_firebase.py stuck alice
  python view_firebase.py ai bob

Note: Make sure firebase-credentials.json is in the same directory.
""")


def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    try:
        # Initialize Firebase
        firebase_manager.init_firebase()
        
        if command == "list":
            list_students()
        
        elif command == "view":
            if len(sys.argv) < 3:
                print("Error: student_id required")
                print_usage()
                sys.exit(1)
            view_student_detail(sys.argv[2])
        
        elif command == "code":
            if len(sys.argv) < 3:
                print("Error: student_id required")
                print_usage()
                sys.exit(1)
            protocol = sys.argv[3].upper() if len(sys.argv) > 3 else None
            view_code_history(sys.argv[2], protocol)
        
        elif command == "snapshots":
            if len(sys.argv) < 3:
                print("Error: student_id required")
                print_usage()
                sys.exit(1)
            protocol = sys.argv[3].upper() if len(sys.argv) > 3 else None
            view_snapshots(sys.argv[2], protocol)
        
        elif command == "stuck":
            if len(sys.argv) < 3:
                print("Error: student_id required")
                print_usage()
                sys.exit(1)
            analyze_stuck_periods(sys.argv[2])
        
        elif command == "ai":
            if len(sys.argv) < 3:
                print("Error: student_id required")
                print_usage()
                sys.exit(1)
            analyze_ai_usage(sys.argv[2])
        
        else:
            print(f"Unknown command: {command}")
            print_usage()
            sys.exit(1)
    
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("\nPlease download firebase-credentials.json from Firebase Console")
        print("See FIREBASE_SETUP_INSTRUCTIONS.txt for details")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

