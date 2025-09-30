# Protocol Switching Guide

## Problem You Had
You were seeing **B92 logs** even though you wanted to run **BB84 protocol**. This happened because both protocol status files were active simultaneously.

## The Solution

### Understanding Protocol Detection

The system has **two protocol detection files**:

1. **`protocol_detection_utils.py`** - Used by the backend/server to detect which protocol is active
2. **`protocol_helpers.py`** - Helper functions for students to switch protocols from notebooks

Both files check for status files:
- `student_implementation_status.json` → BB84 protocol
- `student_b92_implementation_status.json` → B92 protocol

**IMPORTANT:** Only ONE protocol can be active at a time!

### How to Switch Protocols

I've created two scripts to make switching easy:

#### Switch to BB84:
```bash
python switch_to_bb84.py
docker-compose restart
```

This will:
- ✓ Enable `student_implementation_status.json` (BB84)
- ✓ Disable `student_b92_implementation_status.json` → `.disabled`
- ✓ Show BB84 logs in simulation

#### Switch to B92:
```bash
python switch_to_b92.py
docker-compose restart
```

This will:
- ✓ Enable `student_b92_implementation_status.json` (B92)
- ✓ Disable `student_implementation_status.json` → `.disabled`
- ✓ Show B92 logs in simulation

### From Jupyter Notebook

You can also use the helper functions in your notebook:

```python
# For BB84
from protocol_helpers import switch_to_bb84
switch_to_bb84()
# Then restart Docker backend manually

# For B92
from protocol_helpers import switch_to_b92
switch_to_b92()
# Then restart Docker backend manually
```

### Why You MUST Restart Backend

The backend loads the protocol detection **when it starts**. If you change the status files while the backend is running, it won't pick up the changes until you restart:

```bash
docker-compose restart
```

Or full restart:
```bash
docker-compose down
docker-compose up
```

### Verify Current Protocol

Check which protocol is active:

```bash
python -c "from protocol_detection_utils import detect_active_protocol; print('Active:', detect_active_protocol())"
```

Or check status files:
```bash
# Check which files exist
python -c "import os; print('BB84:', os.path.exists('student_implementation_status.json')); print('B92:', os.path.exists('student_b92_implementation_status.json'))"
```

### Implementation Files

Make sure you have the correct implementation files:

**For BB84:**
- `student_bb84_impl.py` - Your BB84 implementation (StudentQuantumHost class)
- `enhanced_student_bridge.py` - Bridge that connects your code to the simulator

**For B92:**
- `student_b92_impl.py` - Your B92 implementation (StudentB92Host class)
- `enhanced_student_bridge_b92.py` - Bridge for B92

### Common Issues

**Issue:** Still seeing wrong protocol logs after switching
**Solution:** Make sure you restarted the Docker backend:
```bash
docker-compose restart
```

**Issue:** Both protocols appear active
**Solution:** Use the switch scripts which ensure only one is active:
```bash
python switch_to_bb84.py  # or switch_to_b92.py
docker-compose restart
```

**Issue:** No logs showing at all
**Solution:** Check that your implementation file exists and the status file has correct paths:
- For BB84: Check `student_bb84_impl.py` exists
- For B92: Check `student_b92_impl.py` exists

### Quick Reference

| Task | Command |
|------|---------|
| Switch to BB84 | `python switch_to_bb84.py && docker-compose restart` |
| Switch to B92 | `python switch_to_b92.py && docker-compose restart` |
| Check active protocol | `python -c "from protocol_detection_utils import detect_active_protocol; print(detect_active_protocol())"` |
| Restart backend | `docker-compose restart` |
| Full restart | `docker-compose down && docker-compose up` |

### What Fixed Your Issue

1. ✓ Created `switch_to_bb84.py` script
2. ✓ Disabled B92 status file (renamed to `.disabled`)
3. ✓ Ensured only BB84 status file is active
4. ✓ Restarted Docker backend
5. ✓ Now you see BB84 logs when running BB84!

---

**Remember:** Always restart the Docker backend after switching protocols!

