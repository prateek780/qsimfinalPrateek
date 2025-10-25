"""
Custom IPython Magic for Automatic Vibe Code Tracking
Replaces manual %save + track_bb84() workflow
"""
from IPython.core.magic import Magics, magics_class, cell_magic
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython import get_ipython
import ast
import sys
import os
import traceback
from datetime import datetime


@magics_class
class VibeCodeMagic(Magics):
    """Custom magic for automatic code tracking"""
    
    def __init__(self, shell):
        super().__init__(shell)
        self.student_id = None
        self.session_id = None
        self.tracker = None
        
    def _validate_syntax(self, code):
        """Validate Python syntax before execution"""
        try:
            ast.parse(code)
            return True, None
        except SyntaxError as e:
            return False, f"Syntax Error at line {e.lineno}: {e.msg}"
        except Exception as e:
            return False, f"Parse Error: {str(e)}"
    
    def _detect_protocol(self, code):
        """Detect protocol from code content"""
        if 'StudentQuantumHost' in code or 'bb84' in code.lower():
            return 'bb84'
        elif 'StudentB92Host' in code or 'b92' in code.lower():
            return 'b92'
        return 'bb84'  # Default
    
    def _check_tracker_initialized(self):
        """Check if tracker is initialized"""
        try:
            import notebook_tracker
            tracker = notebook_tracker.get_tracker()
            if tracker is None:
                return False, "Tracker not initialized. Run the tracking setup cell first."
            self.tracker = tracker
            self.student_id = notebook_tracker.get_student_id()
            self.session_id = notebook_tracker.get_session_id()
            return True, None
        except Exception as e:
            return False, f"Tracker error: {str(e)}"
    
    def _save_to_file(self, code, protocol):
        """Save code to implementation file - overwrites entire file"""
        filename = f"student_{protocol}_impl.py"
        
        try:
            # Simply overwrite the file with current code
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # Verify file was written
            if not os.path.exists(filename):
                return False, f"Failed to create {filename}"
            
            file_size = os.path.getsize(filename)
            if file_size == 0:
                return False, f"{filename} is empty after save"
            
            # Count lines and methods
            lines = code.split('\n')
            method_count = code.count('def ')
            
            print(f"Saved: {len(lines)} lines, {method_count} methods")
            return True, filename
        
        except PermissionError:
            return False, f"Permission denied: Cannot write to {filename}"
        except IOError as e:
            return False, f"IO Error: {str(e)}"
        except Exception as e:
            return False, f"Save error: {str(e)}"
    
    def _track_code(self, protocol):
        """Track code in Firebase"""
        try:
            import notebook_tracker
            
            if protocol == 'bb84':
                notebook_tracker.track_bb84(validate=False)
            elif protocol == 'b92':
                notebook_tracker.track_b92(validate=False)
            else:
                return False, f"Unknown protocol: {protocol}"
            
            return True, None
        
        except Exception as e:
            return False, f"Tracking error: {str(e)}"
    
    @cell_magic
    @magic_arguments()
    @argument('--protocol', '-p', default=None,
              help='Protocol: bb84 or b92')
    def vibe_code(self, line, cell):
        """
        Execute, save, and track vibe code automatically
        
        Usage:
            %%vibe_code
            class StudentQuantumHost:
                def __init__(self, name):
                    pass
                
                def bb84_send_qubits(self, num_qubits):
                    pass
                
                def process_received_qbit(self, qbit, from_channel):
                    pass
        """
        args = parse_argstring(self.vibe_code, line)
        protocol = args.protocol
        
        print("=" * 60)
        print("VIBE CODE: Automatic Save & Track")
        print("=" * 60)
        
        # Step 1: Check tracker initialization
        print("\n[1/4] Checking tracker...")
        initialized, error = self._check_tracker_initialized()
        if not initialized:
            print(f"ERROR: {error}")
            print("\nAction required: Run tracking setup cell first")
            return
        print(f"Student ID: {self.student_id}")
        
        # Step 2: Validate syntax
        print("\n[2/4] Validating syntax...")
        valid, error = self._validate_syntax(cell)
        if not valid:
            print(f"ERROR: {error}")
            print("\nAction required: Fix syntax errors before running")
            return
        print("Syntax valid")
        
        # Step 3: Detect protocol
        if not protocol:
            protocol = self._detect_protocol(cell)
        print(f"\nProtocol detected: {protocol.upper()}")
        
        # Step 4: Execute code
        print("\n[3/4] Executing code...")
        try:
            self.shell.run_cell(cell)
            print("Execution successful")
        except Exception as e:
            print(f"ERROR: Execution failed")
            print(f"Error: {str(e)}")
            print("\nAction required: Fix runtime errors")
            return
        
        # Step 5: Save and track
        print("\n[4/4] Saving and tracking...")
        
        # Save to file (overwrites)
        saved, result = self._save_to_file(cell, protocol)
        if not saved:
            print(f"ERROR: {result}")
            return
        print(f"File: {result}")
        
        # Track in Firebase
        tracked, error = self._track_code(protocol)
        if not tracked:
            print(f"WARNING: {error}")
            print("Code saved locally but not tracked in Firebase")
        else:
            print("Tracked in Firebase")
        
        print("\n" + "=" * 60)
        print("SUCCESS: Code executed, saved, and tracked")
        print("=" * 60)
        print("\nBackground watcher will capture changes every 3 seconds")


def load_ipython_extension(ipython):
    """Load the extension"""
    ipython.register_magics(VibeCodeMagic)


def unload_ipython_extension(ipython):
    """Unload the extension"""
    pass
