"""
Notebook Validation and Recovery System
Prevents students from breaking the notebook
"""
import json
import os
from pathlib import Path
from IPython import get_ipython
from IPython.display import display, HTML
import warnings


class NotebookValidator:
    """Validates and protects notebook structure"""
    
    def __init__(self, notebook_path=None):
        self.notebook_path = notebook_path
        self.required_cells = {
            'tracking_setup': {
                'type': 'setup',
                'content_contains': 'notebook_tracker.init_tracker',
                'description': 'Student tracking initialization',
                'critical': True
            },
            'bb84_implementation': {
                'type': 'vibe_code',
                'content_contains': 'StudentQuantumHost',
                'description': 'BB84 implementation',
                'critical': False
            },
            'b92_implementation': {
                'type': 'vibe_code',
                'content_contains': 'StudentB92Host',
                'description': 'B92 implementation',
                'critical': False
            }
        }
        self.validation_results = {}
    
    def validate_environment(self):
        """Validate Python environment and dependencies"""
        errors = []
        warnings_list = []
        
        # Check critical imports
        critical_modules = ['notebook_tracker', 'firebase_manager']
        for module in critical_modules:
            try:
                __import__(module)
            except ImportError:
                errors.append(f"Missing module: {module}")
        
        # Check optional imports
        optional_modules = ['IPython', 'ast', 'json']
        for module in optional_modules:
            try:
                __import__(module)
            except ImportError:
                warnings_list.append(f"Missing optional module: {module}")
        
        return len(errors) == 0, errors, warnings_list
    
    def validate_files(self):
        """Validate required files exist"""
        errors = []
        
        required_files = [
            'notebook_tracker.py',
            'firebase_manager.py',
            'protocol_helpers.py'
        ]
        
        for file in required_files:
            if not os.path.exists(file):
                errors.append(f"Missing file: {file}")
        
        return len(errors) == 0, errors
    
    def check_tracker_state(self):
        """Check if tracker is properly initialized"""
        try:
            import notebook_tracker
            tracker = notebook_tracker.get_tracker()
            
            if tracker is None:
                return False, "Tracker not initialized"
            
            student_id = notebook_tracker.get_student_id()
            if not student_id:
                return False, "Student ID not set"
            
            session_id = notebook_tracker.get_session_id()
            if not session_id:
                return False, "Session ID not set"
            
            return True, {
                'student_id': student_id,
                'session_id': session_id,
                'firebase_enabled': tracker.use_firebase
            }
        
        except Exception as e:
            return False, f"Tracker error: {str(e)}"
    
    def validate_cell_structure(self):
        """Validate notebook cell structure (if notebook file provided)"""
        if not self.notebook_path or not os.path.exists(self.notebook_path):
            return True, []  # Skip if no notebook file
        
        try:
            with open(self.notebook_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            
            cells = notebook.get('cells', [])
            errors = []
            
            # Check for minimum cells
            if len(cells) < 5:
                errors.append("Too few cells - notebook may be corrupted")
            
            # Check for setup cell
            setup_found = False
            for cell in cells:
                if cell.get('cell_type') == 'code':
                    source = ''.join(cell.get('source', []))
                    if 'notebook_tracker.init_tracker' in source:
                        setup_found = True
                        break
            
            if not setup_found:
                errors.append("Tracking setup cell missing or modified")
            
            return len(errors) == 0, errors
        
        except Exception as e:
            return False, [f"Validation error: {str(e)}"]
    
    def run_full_validation(self):
        """Run all validation checks"""
        results = {
            'environment': {'status': 'pending', 'errors': [], 'warnings': []},
            'files': {'status': 'pending', 'errors': []},
            'tracker': {'status': 'pending', 'info': None},
            'structure': {'status': 'pending', 'errors': []}
        }
        
        # Environment check
        valid, errors, warnings_list = self.validate_environment()
        results['environment'] = {
            'status': 'pass' if valid else 'fail',
            'errors': errors,
            'warnings': warnings_list
        }
        
        # Files check
        valid, errors = self.validate_files()
        results['files'] = {
            'status': 'pass' if valid else 'fail',
            'errors': errors
        }
        
        # Tracker check
        valid, info = self.check_tracker_state()
        results['tracker'] = {
            'status': 'pass' if valid else 'fail',
            'info': info if valid else None,
            'error': info if not valid else None
        }
        
        # Structure check
        valid, errors = self.validate_cell_structure()
        results['structure'] = {
            'status': 'pass' if valid else 'fail',
            'errors': errors
        }
        
        return results
    
    def display_validation_report(self, results):
        """Display validation results in notebook"""
        html = ['<div style="border: 2px solid #333; padding: 15px; margin: 10px 0;">']
        html.append('<h3>Notebook Validation Report</h3>')
        
        overall_status = all(
            r['status'] == 'pass' 
            for r in results.values()
        )
        
        if overall_status:
            html.append('<p style="color: green; font-weight: bold;">All checks passed</p>')
        else:
            html.append('<p style="color: red; font-weight: bold;">Some checks failed</p>')
        
        # Environment
        html.append('<h4>Environment</h4>')
        env = results['environment']
        if env['status'] == 'pass':
            html.append('<p style="color: green;">Pass</p>')
        else:
            html.append('<p style="color: red;">Fail</p>')
            for error in env['errors']:
                html.append(f'<p style="color: red;">- {error}</p>')
        
        # Files
        html.append('<h4>Required Files</h4>')
        files = results['files']
        if files['status'] == 'pass':
            html.append('<p style="color: green;">Pass</p>')
        else:
            html.append('<p style="color: red;">Fail</p>')
            for error in files['errors']:
                html.append(f'<p style="color: red;">- {error}</p>')
        
        # Tracker
        html.append('<h4>Tracker Status</h4>')
        tracker = results['tracker']
        if tracker['status'] == 'pass':
            html.append('<p style="color: green;">Pass</p>')
            info = tracker['info']
            html.append(f'<p>Student ID: {info["student_id"]}</p>')
            html.append(f'<p>Session ID: {info["session_id"]}</p>')
            html.append(f'<p>Firebase: {"Enabled" if info["firebase_enabled"] else "Disabled"}</p>')
        else:
            html.append(f'<p style="color: red;">Fail: {tracker["error"]}</p>')
        
        # Structure
        html.append('<h4>Notebook Structure</h4>')
        structure = results['structure']
        if structure['status'] == 'pass':
            html.append('<p style="color: green;">Pass</p>')
        else:
            html.append('<p style="color: red;">Fail</p>')
            for error in structure['errors']:
                html.append(f'<p style="color: red;">- {error}</p>')
        
        html.append('</div>')
        
        display(HTML(''.join(html)))
        
        return overall_status


def validate_notebook(notebook_path=None):
    """
    Main validation function to call in notebook
    
    Usage in notebook cell:
        from notebook_validator import validate_notebook
        validate_notebook()
    """
    validator = NotebookValidator(notebook_path)
    results = validator.run_full_validation()
    overall_pass = validator.display_validation_report(results)
    
    if not overall_pass:
        print("\nAction required: Fix errors above before continuing")
    
    return overall_pass, results

