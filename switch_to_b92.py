#!/usr/bin/env python3
"""
Force Switch to B92 Protocol
=============================
This script ensures ONLY B92 is active by:
1. Enabling B92 status file
2. Disabling BB84 status file
3. Providing instructions to restart backend
"""

import os
import json
from datetime import datetime

def force_switch_to_b92():
    """Forcefully switch to B92 and disable BB84"""
    
    print("=" * 60)
    print("SWITCHING TO B92 PROTOCOL")
    print("=" * 60)
    
    # 1. Create/Update B92 status file
    b92_status = {
        "student_implementation_ready": True,
        "protocol": "b92",
        "completion_timestamp": datetime.now().isoformat(),
        "source": "notebook_vibe_code",
        "message": "Student B92 implementation completed successfully!",
        "required_methods": [
            "b92_send_qubits",
            "b92_process_received_qbit",
            "b92_sifting",
            "b92_estimate_error_rate"
        ],
        "status": "completed",
        "implementation_file": "student_b92_impl.py",
        "bridge_file": "enhanced_student_bridge_b92.py"
    }
    
    # Re-enable B92 if it was disabled
    if os.path.exists("student_b92_implementation_status.json.disabled"):
        os.rename("student_b92_implementation_status.json.disabled",
                  "student_b92_implementation_status.json")
        print("[OK] Re-enabled student_b92_implementation_status.json")
    
    with open("student_b92_implementation_status.json", "w") as f:
        json.dump(b92_status, f, indent=2)
    print("[OK] Created/Updated student_b92_implementation_status.json (B92)")
    
    # 2. Disable BB84 by renaming to .disabled
    if os.path.exists("student_implementation_status.json"):
        if os.path.exists("student_implementation_status.json.disabled"):
            os.remove("student_implementation_status.json.disabled")
        os.rename("student_implementation_status.json", 
                  "student_implementation_status.json.disabled")
        print("[OK] Disabled student_implementation_status.json")
    else:
        print("[INFO] BB84 status file doesn't exist (already disabled)")
    
    # 3. Verify the changes
    print("\n" + "=" * 60)
    print("VERIFICATION")
    print("=" * 60)
    print(f"BB84 file exists: {os.path.exists('student_implementation_status.json')}")
    print(f"BB84 disabled: {os.path.exists('student_implementation_status.json.disabled')}")
    print(f"B92 file exists: {os.path.exists('student_b92_implementation_status.json')}")
    
    # Read and verify B92 status
    with open("student_b92_implementation_status.json", "r") as f:
        b92 = json.load(f)
    print(f"\nB92 Protocol: {b92.get('protocol')}")
    print(f"B92 Ready: {b92.get('student_implementation_ready')}")
    
    print("\n" + "=" * 60)
    print("NEXT STEPS - IMPORTANT!")
    print("=" * 60)
    print("[WARNING] You MUST restart the Docker backend for changes to take effect!")
    print("\nIn a terminal, run:")
    print("  docker-compose restart")
    print("\nOR stop and start:")
    print("  docker-compose down")
    print("  docker-compose up")
    print("\n[SUCCESS] After restart, the simulation will show B92 logs!")
    print("=" * 60)

if __name__ == "__main__":
    force_switch_to_b92()

