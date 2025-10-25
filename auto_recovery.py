"""
Automatic recovery system for deleted/corrupted cells
"""
import json
import os
from datetime import datetime
from pathlib import Path


class CellRecovery:
    """Recovers deleted or corrupted cells"""
    
    def __init__(self):
        self.backup_dir = Path("notebook_backups")
        self.backup_dir.mkdir(exist_ok=True)
        
        # Template cells
        self.templates = {
            'tracking_setup': '''# STUDENT ACTIVITY TRACKING SETUP WITH FIREBASE
import importlib
import notebook_tracker
importlib.reload(notebook_tracker)

# Get student ID
try:
    student_id
    print(f"Welcome back, {student_id}!")
except NameError:
    student_id = input("Enter your Student ID: ")

# Initialize tracker
notebook_tracker.init_tracker(student_id, use_firebase=True)
''',
            'bb84_template': '''%%vibe_code bb84_send_qubits
class StudentQuantumHost:
    def __init__(self, name):
        self.name = name
        self.sent_bits = []
        self.sent_bases = []
    
    def bb84_send_qubits(self, num_qubits):
        """Send qubits encoded with random bits and bases"""
        # Your implementation here
        pass
''',
            'b92_template': '''%%vibe_code b92_send_qubits
class StudentB92Host:
    def __init__(self, name):
        self.name = name
        self.sent_bits = []
    
    def b92_send_qubits(self, num_qubits):
        """Send qubits using B92 protocol"""
        # Your implementation here
        pass
'''
        }
    
    def create_backup(self, notebook_path):
        """Create backup of current notebook"""
        if not os.path.exists(notebook_path):
            return False, "Notebook file not found"
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"notebook_backup_{timestamp}.ipynb"
            backup_path = self.backup_dir / backup_name
            
            with open(notebook_path, 'r', encoding='utf-8') as src:
                content = src.read()
            
            with open(backup_path, 'w', encoding='utf-8') as dst:
                dst.write(content)
            
            return True, str(backup_path)
        
        except Exception as e:
            return False, f"Backup failed: {str(e)}"
    
    def get_template_cell(self, template_name):
        """Get template cell code"""
        return self.templates.get(template_name, None)
    
    def restore_from_backup(self, backup_path, notebook_path):
        """Restore notebook from backup"""
        try:
            if not os.path.exists(backup_path):
                return False, "Backup file not found"
            
            with open(backup_path, 'r', encoding='utf-8') as src:
                content = src.read()
            
            with open(notebook_path, 'w', encoding='utf-8') as dst:
                dst.write(content)
            
            return True, "Notebook restored successfully"
        
        except Exception as e:
            return False, f"Restore failed: {str(e)}"
    
    def list_backups(self):
        """List all available backups"""
        backups = list(self.backup_dir.glob("notebook_backup_*.ipynb"))
        backups.sort(reverse=True)  # Most recent first
        return backups


def create_emergency_backup():
    """
    Emergency backup function for students to call
    
    Usage in notebook:
        from auto_recovery import create_emergency_backup
        create_emergency_backup()
    """
    recovery = CellRecovery()
    success, result = recovery.create_backup("qsimnotebook.ipynb")
    
    if success:
        print(f"Emergency backup created: {result}")
        print("If something goes wrong, contact instructor with this backup file")
    else:
        print(f"Backup failed: {result}")
    
    return success


def get_tracking_setup_cell():
    """
    Get tracking setup cell template
    
    Usage: If student deletes Cell 1, run this to get the code back
    """
    recovery = CellRecovery()
    template = recovery.get_template_cell('tracking_setup')
    
    print("Copy this code into a new cell and run it:")
    print("=" * 60)
    print(template)
    print("=" * 60)
    
    return template

