"""
View Method-Level Snapshots
Display student progress on individual methods
"""
import sys
import io
import firebase_manager
from datetime import datetime

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def view_method_snapshots(student_id, protocol):
    """View all method snapshots for a student's protocol"""
    try:
        sessions = firebase_manager.get_student_sessions(student_id)
        
        if not sessions:
            print(f"\nNo sessions found for student: {student_id}")
            return
        
        print("\n" + "=" * 80)
        print(f"METHOD-LEVEL SNAPSHOTS: {student_id} - {protocol}")
        print("=" * 80)
        
        all_method_snapshots = {}
        
        for session in sessions:
            session_id = session['session_id']
            
            # Get method snapshots for this session
            db = firebase_manager.get_firestore()
            activity_logs_ref = (db.collection('students').document(student_id)
                                   .collection('sessions').document(session_id)
                                   .collection('activity_logs'))
            
            for doc in activity_logs_ref.stream():
                doc_id = doc.id
                if doc_id.startswith(f'Snapshot_{protocol}_'):
                    data = doc.to_dict()
                    method_name = data.get('method_name')
                    all_method_snapshots[method_name] = data
        
        if not all_method_snapshots:
            print(f"\nNo method snapshots found for {protocol}")
            print("\nMake sure you:")
            print("1. Run Cell 7 (Setup)")
            print(f"2. Save your {protocol} code (Cell 11 or 23)")
            print(f"3. Track your {protocol} code (Cell 12 or 24)")
            return
        
        print(f"\nTotal Methods: {len(all_method_snapshots)}")
        
        # Display each method's snapshots
        for idx, (method_name, data) in enumerate(sorted(all_method_snapshots.items()), 1):
            snapshots = data.get('snapshots', [])
            total_snapshots = len(snapshots)
            
            print(f"\n{'-' * 80}")
            print(f"[{idx}] Method: {method_name}")
            print(f"Total Snapshots: {total_snapshots}")
            print(f"Created: {data.get('created_at', 'N/A')}")
            print(f"Last Updated: {data.get('last_updated', 'N/A')}")
            
            if snapshots:
                # Calculate total time spent on this method
                total_time_seconds = sum(snap.get('changes', {}).get('time_spent_seconds', 0) for snap in snapshots)
                total_minutes = int(total_time_seconds // 60)
                total_seconds = int(total_time_seconds % 60)
                total_time_str = f"{total_minutes}m {total_seconds}s" if total_minutes > 0 else f"{total_seconds}s"
                
                # Show first and last snapshot
                first_snap = snapshots[0]
                last_snap = snapshots[-1]
                
                print(f"\nProgress Summary:")
                print(f"  Total Time Spent: {total_time_str} ({total_time_seconds:.1f}s)")
                print(f"  Snapshots Created: {total_snapshots}")
                
                print(f"\nFirst Implementation:")
                print(f"  Lines: {first_snap.get('line_count', 0)}")
                print(f"  Chars: {first_snap.get('char_count', 0)}")
                first_time = first_snap.get('timestamp', 'N/A')
                if first_time != 'N/A':
                    try:
                        dt = datetime.fromisoformat(first_time)
                        first_time = dt.strftime('%b %d at %I:%M:%S %p')
                    except:
                        pass
                print(f"  Time: {first_time}")
                
                if total_snapshots > 1:
                    print(f"\nLatest Version (Snapshot {total_snapshots}):")
                    print(f"  Lines: {last_snap.get('line_count', 0)}")
                    print(f"  Chars: {last_snap.get('char_count', 0)}")
                    last_time = last_snap.get('timestamp', 'N/A')
                    if last_time != 'N/A':
                        try:
                            dt = datetime.fromisoformat(last_time)
                            last_time = dt.strftime('%b %d at %I:%M:%S %p')
                        except:
                            pass
                    print(f"  Time: {last_time}")
                    
                    changes = last_snap.get('changes', {})
                    print(f"\nLast Change:")
                    print(f"  Lines added: {changes.get('lines_added', 0)}")
                    print(f"  Lines removed: {changes.get('lines_removed', 0)}")
                    print(f"  Time since previous: {changes.get('time_spent', 'N/A')}")
                    
                    # Alert if stuck
                    time_seconds = changes.get('time_spent_seconds', 0)
                    if time_seconds > 300:
                        print(f"  [ALERT] Long gap - student may have been stuck")
                    elif time_seconds < 10 and changes.get('lines_added', 0) > 10:
                        print(f"  [ALERT] Large addition in short time - possible AI usage")
                
                # Show code preview
                code_lines = last_snap.get('code', [])
                if code_lines:
                    print(f"\nCurrent Code Preview (first 10 lines):")
                    for i, line in enumerate(code_lines[:10], 1):
                        print(f"  {i:3} | {line}")
                    if len(code_lines) > 10:
                        print(f"  ... | ({len(code_lines) - 10} more lines)")
        
        print("\n" + "=" * 80)
        print(f"SUMMARY: {len(all_method_snapshots)} methods tracked for {protocol}")
        print("=" * 80)
        
    except Exception as e:
        print(f"Error viewing method snapshots: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python view_method_snapshots.py <student_id> <BB84|B92>")
        print("\nExample:")
        print("  python view_method_snapshots.py john_doe_2024 BB84")
        sys.exit(1)
    
    student_id = sys.argv[1]
    protocol = sys.argv[2].upper()
    
    view_method_snapshots(student_id, protocol)

