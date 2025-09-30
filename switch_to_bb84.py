#!/usr/bin/env python3
"""
Force Switch to BB84 Protocol
==============================
This script ensures ONLY BB84 is active by:
1. Enabling BB84 status file
2. Disabling B92 status file
3. Providing instructions to restart backend
"""

import os
import json
from datetime import datetime

def force_switch_to_bb84():
    """Forcefully switch to BB84 and disable B92"""
    
    print("=" * 60)
    print("SWITCHING TO BB84 PROTOCOL")
    print("=" * 60)
    
    # 1. Create/Update BB84 status file
    bb84_status = {
        "student_implementation_ready": True,
        "protocol": "bb84",
        "completion_timestamp": datetime.now().isoformat(),
        "source": "notebook_vibe_code",
        "message": "Student BB84 implementation completed successfully!",
        "required_methods": [
            "bb84_send_qubits",
            "process_received_qbit",
            "bb84_reconcile_bases",
            "bb84_estimate_error_rate"
        ],
        "status": "completed",
        "implementation_file": "student_bb84_impl.py",
        "bridge_file": "enhanced_student_bridge.py"
    }
    
    with open("student_implementation_status.json", "w") as f:
        json.dump(bb84_status, f, indent=2)
    print("[OK] Created/Updated student_implementation_status.json (BB84)")
    
    # 2. Disable B92 by renaming to .disabled
    if os.path.exists("student_b92_implementation_status.json"):
        if os.path.exists("student_b92_implementation_status.json.disabled"):
            os.remove("student_b92_implementation_status.json.disabled")
        os.rename("student_b92_implementation_status.json", 
                  "student_b92_implementation_status.json.disabled")
        print("[OK] Disabled student_b92_implementation_status.json")
    else:
        print("[INFO] B92 status file doesn't exist (already disabled)")
    
    # 3. Verify the changes
    print("\n" + "=" * 60)
    print("VERIFICATION")
    print("=" * 60)
    print(f"BB84 file exists: {os.path.exists('student_implementation_status.json')}")
    print(f"B92 file exists: {os.path.exists('student_b92_implementation_status.json')}")
    print(f"B92 disabled: {os.path.exists('student_b92_implementation_status.json.disabled')}")
    
    # Read and verify BB84 status
    with open("student_implementation_status.json", "r") as f:
        bb84 = json.load(f)
    print(f"\nBB84 Protocol: {bb84.get('protocol')}")
    print(f"BB84 Ready: {bb84.get('student_implementation_ready')}")
    
    print("\n" + "=" * 60)
    print("NEXT STEPS - IMPORTANT!")
    print("=" * 60)
    print("[WARNING] You MUST restart the Docker backend for changes to take effect!")
    print("\nIn a terminal, run:")
    print("  docker-compose restart")
    print("\nOR stop and start:")
    print("  docker-compose down")
    print("  docker-compose up")
    print("\n[SUCCESS] After restart, the simulation will show BB84 logs!")
    print("=" * 60)

if __name__ == "__main__":
    force_switch_to_bb84()

