# Quantum Networking Simulation - Complete Documentation

Welcome to the Quantum Networking Simulation! This document provides a complete step-by-step guide to set up, run, and work with both BB84 and B92 quantum key distribution protocols.

## Table of Contents

1. [System Overview](#system-overview)
2. [Prerequisites](#prerequisites)
3. [Initial Setup](#initial-setup)
4. [Running the Simulation](#running-the-simulation)
5. [Protocol Switching (BB84 ↔ B92)](#protocol-switching-bb84--b92)
6. [Understanding Protocol Detection](#understanding-protocol-detection)
7. [Working with the Notebook](#working-with-the-notebook)
8. [Troubleshooting](#troubleshooting)
9. [File Structure](#file-structure)

---

## System Overview

This is a **quantum networking simulation platform** that allows you to:
- Implement quantum key distribution protocols (BB84 and B92)
- Visualize quantum communication in real-time
- Learn about quantum cryptography through hands-on coding
- Switch between different QKD protocols seamlessly

### Architecture

```
┌─────────────────┐
│ Jupyter Notebook│  ← Your code and interactions
└────────┬────────┘
         │
    ┌────▼────────────────────┐
    │   Docker Backend        │
    │  ┌──────────────────┐   │
    │  │ Python Server    │   │
    │  │ Redis Cache      │   │
    │  │ Caddy Proxy      │   │
    │  └──────────────────┘   │
    └────┬────────────────────┘
         │
    ┌────▼────────────────────┐
    │ Web UI (React)          │  ← Visualization
    └─────────────────────────┘
```

---

## Prerequisites

### Required Software

1. **Docker Desktop** (latest version)
   - Download: https://www.docker.com/products/docker-desktop
   - Make sure it's running before starting

2. **Python 3.8+** (for notebook)
   - Check: `python --version`

3. **Jupyter Notebook or JupyterLab**
   - Install: `pip install jupyter notebook`

### System Requirements

- **RAM:** 4GB minimum (8GB recommended)
- **Disk Space:** 5GB free
- **OS:** Windows 10/11, macOS, or Linux
- **Network:** Internet connection for initial Docker image download

---

## Initial Setup

### Step 1: Clone/Download the Repository

```bash
cd qsimforb92
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Start Docker Backend

**Important:** Make sure Docker Desktop is running first!

```bash
docker-compose up --build
```

This will:
- Build all Docker containers
- Start the backend server
- Start Redis cache
- Start the web interface
- Set up networking between containers

**Wait for:** "All services started successfully" message

### Step 4: Verify Backend is Running

Open a browser and visit:
- **Main UI:** http://localhost:8001
- **API Health:** http://localhost:8001/api/health

If you see the UI, you're ready to go!

---

## Running the Simulation

### Step 1: Choose Your Protocol

You can work with either BB84 or B92 protocol. By default, BB84 is active.

**To verify current protocol:**
```bash
python -c "from protocol_detection_utils import detect_active_protocol; print('Active:', detect_active_protocol())"
```

### Step 2: Open the Notebook

```bash
jupyter notebook qsimnotebook.ipynb
```

### Step 3: Run Through the Notebook Cells

The notebook guides you through:

1. **Import Libraries** - Set up the environment
2. **Understand Quantum Basics** - Learn about qubits
3. **Implement Protocol** - Write your BB84 or B92 code
4. **Run Simulation** - See your code in action
5. **Analyze Results** - View logs and statistics

### Step 4: View Results

The last cell in the notebook displays an embedded web interface showing:
- Real-time quantum state transmission
- Protocol execution steps
- Your implementation method calls
- Error rates and key generation statistics

---

## Protocol Switching (BB84 ↔ B92)

### Understanding Protocol Switching

**IMPORTANT:** Only ONE protocol can be active at a time!

The system uses status files to determine which protocol to use:
- `student_implementation_status.json` → **BB84 protocol**
- `student_b92_implementation_status.json` → **B92 protocol**

When you see the wrong protocol logs (e.g., B92 logs when you want BB84), it means both files are active.

### Quick Protocol Switch

I've created automated scripts for easy switching:

#### Switch to BB84

```bash
python switch_to_bb84.py
docker-compose restart
```

**What this does:**
- ✓ Enables `student_implementation_status.json` (BB84)
- ✓ Disables `student_b92_implementation_status.json` (renamed to `.disabled`)
- ✓ Updates protocol status
- ✓ Shows verification

**You'll see BB84 logs like:**
- "STUDENT BB84: Starting with X qubits"
- "BB84 protocol detected"
- "bb84_send_qubits", "bb84_reconcile_bases", etc.

#### Switch to B92

```bash
python switch_to_b92.py
docker-compose restart
```

**What this does:**
- ✓ Enables `student_b92_implementation_status.json` (B92)
- ✓ Disables `student_implementation_status.json` (renamed to `.disabled`)
- ✓ Updates protocol status
- ✓ Shows verification

**You'll see B92 logs like:**
- "STUDENT B92: Starting with X qubits"
- "B92 protocol detected"
- "b92_send_qubits", "b92_sifting", etc.

### From Jupyter Notebook

You can also switch protocols from within the notebook:

```python
# Switch to BB84
from protocol_helpers import switch_to_bb84
switch_to_bb84()
# Then manually restart: docker-compose restart

# Switch to B92
from protocol_helpers import switch_to_b92
switch_to_b92()
# Then manually restart: docker-compose restart

# Check current protocol
from protocol_helpers import check_current_protocol
check_current_protocol()
```

### Why Restart is Required

The Docker backend loads protocol detection **when it starts**. Changes to status files won't take effect until you restart:

```bash
docker-compose restart
```

This is **mandatory** - without restart, you'll continue seeing the old protocol!

---

## Understanding Protocol Detection

### The Detection System

There are **two protocol detection files** that work together:

#### 1. `protocol_detection_utils.py` (Backend)

- Used by the Docker backend/server
- Detects which protocol is active based on status files
- **Detection priority:**
  1. Check `student_implementation_status.json` for BB84
  2. Check `student_b92_implementation_status.json` for B92 (if not disabled)
  3. Default to BB84 if unclear

#### 2. `protocol_helpers.py` (Notebook)

- Used by notebook cells
- Provides helper functions for students
- Functions available:
  - `create_bb84_status_file()` - Enable BB84
  - `create_b92_status_file()` - Enable B92
  - `switch_to_bb84()` - Switch to BB84 (disables B92)
  - `switch_to_b92()` - Switch to B92 (disables BB84)
  - `check_current_protocol()` - See what's active
  - `disable_bb84()` - Disable BB84
  - `disable_b92()` - Disable B92

### Status File Format

**BB84 Status (`student_implementation_status.json`):**
```json
{
  "student_implementation_ready": true,
  "protocol": "bb84",
  "required_methods": [
    "bb84_send_qubits",
    "process_received_qbit",
    "bb84_reconcile_bases",
    "bb84_estimate_error_rate"
  ],
  "implementation_file": "student_bb84_impl.py",
  "bridge_file": "enhanced_student_bridge.py"
}
```

**B92 Status (`student_b92_implementation_status.json`):**
```json
{
  "student_implementation_ready": true,
  "protocol": "b92",
  "required_methods": [
    "b92_send_qubits",
    "b92_process_received_qbit",
    "b92_sifting",
    "b92_estimate_error_rate"
  ],
  "implementation_file": "student_b92_impl.py",
  "bridge_file": "enhanced_student_bridge_b92.py"
}
```

### Verification Commands

**Check active protocol:**
```bash
python -c "from protocol_detection_utils import detect_active_protocol; print('Active:', detect_active_protocol())"
```

**Check which files exist:**
```bash
python -c "import os; print('BB84:', os.path.exists('student_implementation_status.json')); print('B92:', os.path.exists('student_b92_implementation_status.json'))"
```

**See detailed status:**
```bash
python -c "from protocol_detection_utils import print_protocol_status; print_protocol_status()"
```

---

## Working with the Notebook

### Notebook Structure

The `qsimnotebook.ipynb` contains:

1. **Introduction** - Overview of quantum networking
2. **Section 1: Quantum Fundamentals** - Qubit basics
3. **Section 2: BB84 Protocol** - BB84 implementation
4. **Section 3: BB84 Status** - Enable BB84 simulation
5. **Section 4: B92 Protocol** - B92 implementation
6. **Section 5: B92 Status** - Enable B92 simulation
7. **Final Section: Run Simulation** - Execute and visualize

### Implementing Your Protocol

#### For BB84:

Create the `StudentQuantumHost` class with these methods:

```python
class StudentQuantumHost:
    def __init__(self, name):
        # Initialize host
        pass
    
    def bb84_send_qubits(self, num_qubits):
        # Prepare and send qubits
        pass
    
    def process_received_qbit(self, qbit, from_channel):
        # Measure received qubit
        pass
    
    def bb84_reconcile_bases(self, alice_bases, bob_bases):
        # Compare bases and find matches
        pass
    
    def bb84_estimate_error_rate(self, sample_positions, reference_bits):
        # Calculate error rate
        pass
```

The notebook provides detailed prompts and examples for each method!

#### For B92:

Create the `StudentB92Host` class with these methods:

```python
class StudentB92Host:
    def __init__(self, name):
        # Initialize host
        pass
    
    def b92_send_qubits(self, num_qubits):
        # Prepare qubits (|0⟩ or |+⟩)
        pass
    
    def b92_process_received_qbit(self, qbit, from_channel):
        # Measure qubit in random basis
        pass
    
    def b92_sifting(self, sent_bits, received_measurements):
        # Keep only conclusive measurements
        pass
    
    def b92_estimate_error_rate(self, sample_positions, reference_bits):
        # Calculate error rate
        pass
```

### Saving Your Implementation

After completing your protocol implementation in the notebook, save it to a Python file:

```python
# For BB84
%save -f student_bb84_impl.py <cell_number>

# For B92
%save -f student_b92_impl.py <cell_number>
```

Replace `<cell_number>` with the cell containing your implementation.

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: Seeing Wrong Protocol Logs

**Problem:** Running BB84 but seeing B92 logs (or vice versa)

**Solution:**
```bash
# For BB84
python switch_to_bb84.py
docker-compose restart

# For B92
python switch_to_b92.py
docker-compose restart
```

**Cause:** Both protocol status files are active simultaneously.

---

#### Issue: Docker Containers Won't Start

**Problem:** `docker-compose up` fails with container name conflicts

**Solution:**
```bash
# Stop and remove existing containers
docker-compose down

# Remove the conflicting container
docker rm -f redis

# Start fresh
docker-compose up --build
```

**Alternative:**
```bash
# Remove all containers and start clean
docker-compose down -v
docker-compose up --build
```

---

#### Issue: Backend Not Reachable

**Problem:** Notebook says "Backend proxy not reachable"

**Solution:**

1. Check Docker is running:
   ```bash
   docker ps
   ```
   You should see containers: `redis`, `python-server`, `caddy`, etc.

2. Check if port 8001 is available:
   ```bash
   # Windows
   netstat -ano | findstr :8001
   
   # Mac/Linux
   lsof -i :8001
   ```

3. Restart backend:
   ```bash
   docker-compose restart
   ```

4. Try accessing directly:
   - Open browser: http://localhost:8001

---

#### Issue: No Logs Showing in Simulation

**Problem:** Simulation runs but no logs appear

**Solution:**

1. Verify your implementation file exists:
   ```bash
   # For BB84
   python -c "import os; print('BB84 impl exists:', os.path.exists('student_bb84_impl.py'))"
   
   # For B92
   python -c "import os; print('B92 impl exists:', os.path.exists('student_b92_impl.py'))"
   ```

2. Check status file is correct:
   ```bash
   # View BB84 status
   python -c "import json; print(json.dumps(json.load(open('student_implementation_status.json')), indent=2))"
   ```

3. Ensure implementation file path matches status file:
   - Status file should point to correct implementation file
   - Bridge file should exist

4. Restart backend:
   ```bash
   docker-compose restart
   ```

---

#### Issue: Protocol Switch Not Taking Effect

**Problem:** Switched protocols but still seeing old protocol

**Cause:** Forgot to restart Docker backend

**Solution:**
```bash
docker-compose restart
```

**Remember:** Protocol changes ONLY take effect after restart!

---

#### Issue: Import Errors in Notebook

**Problem:** `ImportError` or `ModuleNotFoundError`

**Solution:**

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure you're in the correct directory:
   ```bash
   python -c "import os; print('Current dir:', os.getcwd())"
   ```

3. Add current directory to path (in notebook):
   ```python
   import sys
   sys.path.append('.')
   ```

---

#### Issue: Redis Connection Errors

**Problem:** "Could not connect to Redis"

**Solution:**

1. Check Redis container is running:
   ```bash
   docker ps | findstr redis
   ```

2. Restart Redis:
   ```bash
   docker-compose restart redis
   ```

3. Check Redis logs:
   ```bash
   docker logs redis
   ```

---

#### Issue: Port Already in Use

**Problem:** "Port 8001 is already allocated"

**Solution:**

1. Find what's using the port:
   ```bash
   # Windows
   netstat -ano | findstr :8001
   
   # Mac/Linux
   lsof -i :8001
   ```

2. Stop the process or change port in `docker-compose.yaml`

3. Restart:
   ```bash
   docker-compose down
   docker-compose up
   ```

---

## File Structure

### Key Files You'll Work With

```
qsimforb92/
├── qsimnotebook.ipynb           # Main notebook - YOUR WORKSPACE
├── student_bb84_impl.py         # Your BB84 implementation
├── student_b92_impl.py          # Your B92 implementation
│
├── Protocol Switching:
├── switch_to_bb84.py            # Switch to BB84 protocol
├── switch_to_b92.py             # Switch to B92 protocol
├── protocol_helpers.py          # Notebook helper functions
├── protocol_detection_utils.py  # Backend detection logic
│
├── Status Files (auto-generated):
├── student_implementation_status.json       # BB84 status
├── student_b92_implementation_status.json   # B92 status
│
├── Backend Bridge Files:
├── enhanced_student_bridge.py       # BB84 bridge
├── enhanced_student_bridge_b92.py   # B92 bridge
│
├── Configuration:
├── docker-compose.yaml          # Docker services
├── requirements.txt             # Python dependencies
│
└── Documentation:
    ├── DOCUMENTATION.md         # This file
    ├── PROTOCOL_SWITCHING_GUIDE.md
    └── PROTOCOL_FIX_SUMMARY.md
```

### Important Directories

```
quantum_network/          # Core quantum networking code
├── channel.py           # Quantum channel implementation
├── node.py              # Quantum node implementation
└── ...

server/                   # Backend API server
├── api/                 # REST API endpoints
├── student_status.py    # Protocol detection endpoint
└── ...

ui/                      # React frontend
└── src/                 # UI source code

core/                    # Core simulation engine
├── world.py            # BB84 simulation world
├── world_b92.py        # B92 simulation world
└── ...
```

---

## Quick Reference Commands

### Docker Management

```bash
# Start backend
docker-compose up

# Start in background
docker-compose up -d

# Restart (use after protocol switch!)
docker-compose restart

# Stop
docker-compose down

# View logs
docker-compose logs -f

# Rebuild (after code changes)
docker-compose up --build
```

### Protocol Switching

```bash
# Switch to BB84
python switch_to_bb84.py && docker-compose restart

# Switch to B92
python switch_to_b92.py && docker-compose restart

# Check current protocol
python -c "from protocol_detection_utils import detect_active_protocol; print(detect_active_protocol())"
```

### Notebook Operations

```bash
# Start Jupyter
jupyter notebook qsimnotebook.ipynb

# Save cell to file (in notebook)
%save -f student_bb84_impl.py <cell_number>
```

### Verification

```bash
# Check Docker containers
docker ps

# Check backend health
curl http://localhost:8001/api/health

# Check protocol status
python -c "from protocol_detection_utils import print_protocol_status; print_protocol_status()"
```

---

## Getting Help

### Resources

1. **Notebook Prompts** - Each cell has detailed instructions
2. **This Documentation** - Complete reference
3. **Protocol Switching Guide** - `PROTOCOL_SWITCHING_GUIDE.md`
4. **Protocol Fix Summary** - `PROTOCOL_FIX_SUMMARY.md`

### Common Questions

**Q: Do I need to restart Docker every time?**  
A: Only when switching protocols or changing backend code.

**Q: Can I run both BB84 and B92 simultaneously?**  
A: No, only one protocol can be active at a time.

**Q: How do I know which protocol is active?**  
A: Run: `python -c "from protocol_detection_utils import detect_active_protocol; print(detect_active_protocol())"`

**Q: Where do I write my protocol implementation?**  
A: In the notebook cells, then save to `.py` files using `%save` command.

**Q: Why am I seeing B92 logs when I want BB84?**  
A: Both protocols are active. Run `python switch_to_bb84.py` and restart Docker.

---

## Next Steps

1. ✓ Setup complete? Start with the notebook
2. ✓ Read through the quantum fundamentals section
3. ✓ Implement BB84 protocol first (simpler)
4. ✓ Test your implementation
5. ✓ Switch to B92 and implement it
6. ✓ Compare the two protocols
7. ✓ Experiment with different parameters

---

**Happy Quantum Networking! 🚀⚛️**

For issues or questions, check the troubleshooting section or review the protocol switching guide.

