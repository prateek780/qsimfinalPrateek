"""
Smart Save - Auto-fix indentation before saving to impl files

Provides magic commands:
    %%save_and_track_bb84  - Auto-fix, save, execute, and track BB84
    %%save_and_track_b92   - Auto-fix, save, execute, and track B92
    %%save_bb84            - Auto-fix, save, and execute BB84 only
    %%save_b92             - Auto-fix, save, and execute B92 only
"""
from IPython.core.magic import register_cell_magic
from IPython import get_ipython
import re


def fix_indentation(code: str, class_name: str) -> str:
    """Automatically fix indentation for methods inside the class"""
    lines = code.split('\n')
    fixed_lines = []
    in_class = False
    class_indent = 0
    
    for i, line in enumerate(lines):
        if re.match(rf'^\s*class\s+{class_name}', line):
            in_class = True
            class_indent = len(line) - len(line.lstrip())
            fixed_lines.append(line)
            continue
        
        if in_class:
            current_indent = len(line) - len(line.lstrip())
            
            if re.match(r'^\s*def\s+\w+\s*\(', line):
                if current_indent != class_indent + 4:
                    fixed_line = ' ' * (class_indent + 4) + line.lstrip()
                    fixed_lines.append(fixed_line)
                else:
                    fixed_lines.append(line)
                continue
            
            last_method_indent = None
            for prev_line in reversed(fixed_lines):
                if re.match(r'^\s*def\s+\w+\s*\(', prev_line):
                    last_method_indent = len(prev_line) - len(prev_line.lstrip())
                    break
            
            if last_method_indent is not None and line.strip():
                if current_indent > 0 and current_indent < last_method_indent + 4:
                    fixed_line = ' ' * (last_method_indent + 4) + line.lstrip()
                    fixed_lines.append(fixed_line)
                    continue
        
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)


@register_cell_magic
def save_bb84(line, cell):
    """Auto-fix indentation and save BB84 code"""
    fixed_code = fix_indentation(cell, "StudentQuantumHost")
    
    with open('student_bb84_impl.py', 'w', encoding='utf-8') as f:
        f.write(fixed_code)
    
    get_ipython().run_cell(fixed_code)
    print("Saved to student_bb84_impl.py")


@register_cell_magic
def save_b92(line, cell):
    """Auto-fix indentation and save B92 code"""
    fixed_code = fix_indentation(cell, "StudentB92Host")
    
    with open('student_b92_impl.py', 'w', encoding='utf-8') as f:
        f.write(fixed_code)
    
    get_ipython().run_cell(fixed_code)
    print("Saved to student_b92_impl.py")


@register_cell_magic
def save_and_track_bb84(line, cell):
    """Auto-fix, save, execute, and track BB84 code"""
    fixed_code = fix_indentation(cell, "StudentQuantumHost")
    
    with open('student_bb84_impl.py', 'w', encoding='utf-8') as f:
        f.write(fixed_code)
    
    get_ipython().run_cell(fixed_code)
    
    try:
        import notebook_tracker
        notebook_tracker.track_bb84(validate=False)
    except Exception as e:
        print(f"Tracking error: {e}")


@register_cell_magic
def save_and_track_b92(line, cell):
    """Auto-fix, save, execute, and track B92 code"""
    fixed_code = fix_indentation(cell, "StudentB92Host")
    
    with open('student_b92_impl.py', 'w', encoding='utf-8') as f:
        f.write(fixed_code)
    
    get_ipython().run_cell(fixed_code)
    
    try:
        import notebook_tracker
        notebook_tracker.track_b92(validate=False)
    except Exception as e:
        print(f"Tracking error: {e}")


def load_magic():
    """Load the magic commands"""
    pass

