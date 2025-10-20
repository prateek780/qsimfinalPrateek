# Quantum Key Distribution Lab - Student Guide

> **Welcome!** This guide will walk you through setting up and completing your quantum networking lab assignment. Your work will be automatically tracked and saved to Firebase.

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/prateek780/qsimnotebookfinal)
[![Python](https://img.shields.io/badge/Python-3.8+-green?logo=python)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Required-blue?logo=docker)](https://www.docker.com/)

---

## Table of Contents

- [Installation](#installation)
- [Getting Started](#getting-started)
- [Implementing BB84 Protocol](#implementing-bb84-protocol)
- [Implementing B92 Protocol](#implementing-b92-protocol)
- [Visualizing Your Implementation](#visualizing-your-implementation)
- [How Tracking Works](#how-tracking-works)
- [Troubleshooting](#troubleshooting)
- [Quick Reference](#quick-reference)
- [FAQ](#frequently-asked-questions)

---

## Installation

### Step 1: Install Required Software

| Operating System | Command | What It Installs |
|-----------------|---------|------------------|
| **Windows** | `install.bat` | Python 3.8+, Jupyter, Docker, Dependencies |
| **Linux** | `chmod +x install_linux.sh && ./install_linux.sh` | Python 3.8+, Jupyter, Docker, Dependencies |
| **macOS** | `chmod +x install_mac.sh && ./install_mac.sh` | Python 3.8+, Jupyter, Docker, Dependencies |

### Step 2: Clone the Repository

```bash
git clone https://github.com/prateek780/qsimnotebookfinal
cd qsimnotebookfinal
```

### Step 3: Start Docker Backend

> **Important:** Make sure Docker Desktop is running first!

```bash
docker-compose up -d
```

**Wait for:** `Student BB84 implementation detected and ready`

---

## Getting Started

### Open Project in VS Code or Cursor

1. Open VS Code or Cursor IDE
2. **File** → **Open Folder**
3. Select `qsimnotebookfinal` folder
4. Locate `qsimnotebook.ipynb` file in the folder
5. Click on the notebook file to open it

### Initialize Student Tracking

> **CRITICAL:** Run this FIRST before doing anything else!

Find the **"STUDENT ACTIVITY TRACKING SETUP"** cell (Cell 1) and run it.

**What You'll See:**

```
Enter your Student ID: ___________
```

**After entering your ID:**

```
Step 1/3: Initializing Firebase connection...
Firebase connected: qsimnotebookfinal
Step 2/3: Setting up student record (your_student_id)...
  > Student record ready
Step 3/3: Creating session...
SUCCESS: Firebase fully connected - Session ID: abc123...

TRACKING STARTED FOR STUDENT: your_student_id
```

**What This Does:**

- **Creates Account** - Sets up your student record in Firebase cloud database
- **Starts Session** - Begins a new coding session with unique timestamp ID
- **Enables Tracking** - Starts recording all your code changes with timestamps
- **Background Monitor** - Automatically watches for file changes every 3 seconds

---

## Implementing BB84 Protocol

### The 4 Methods You'll Implement

| Method | Purpose | What It Does |
|--------|---------|--------------|
| `bb84_send_qubits` | Prepare qubits | Generate random bits and bases, encode qubits, send to Bob |
| `process_received_qbit` | Measure qubits | Receive qubit, measure in random basis, store result |
| `bb84_reconcile_bases` | Compare bases | Find matching measurement bases between Alice and Bob |
| `bb84_estimate_error_rate` | Check security | Calculate error rate to detect eavesdropping |

---

### Complete Workflow for EACH Method

#### Step-by-Step Process

| Step | Action | Details |
|------|--------|---------|
| **1** | **Read Prompt** | Review cell instructions - each cell has detailed explanation |
| **2** | **Generate Code** | Use AI assistant (Copilot/Cursor) to help write implementation |
| **3** | **Save Code** | `%save -f student_bb84_impl.py <cell_number>` | (cell number changes for each run so make sure to notice and change it for every run.)
| **4** | **Track Code** | `notebook_tracker.track_bb84()` - uploads to Firebase with timestamp |
| **5** | **Wait** | Pause 5 seconds - let background watcher capture changes |

---

### Detailed Example

#### STEP 1: Read the Prompt

```python
# PROMPT: Implement the bb84_send_qubits method
# This method should:
# 1. Generate random bits (0 or 1) for each qubit
# 2. Generate random bases (rectilinear or diagonal)
# 3. Encode bits in qubits using the chosen bases
# 4. Send qubits to Bob through quantum channel
```

#### STEP 2: Write Code with AI Help

```python
class StudentQuantumHost:
    def __init__(self, name):
        self.name = name
        self.sent_bits = []
        self.sent_bases = []
    
    def bb84_send_qubits(self, num_qubits):
        """Send qubits encoded with random bits and bases"""
        import random
        from quantum_network import Qubit
        
        qubits = []
        for i in range(num_qubits):
            # Generate random bit and basis
            bit = random.randint(0, 1)
            basis = random.choice(['rectilinear', 'diagonal'])
            
            # Store for later comparison
            self.sent_bits.append(bit)
            self.sent_bases.append(basis)
            
            # Create and encode qubit
            qubit = Qubit(bit, basis)
            qubits.append(qubit)
        
        return qubits
```

#### STEP 3: Save Your Code

In a new cell, run:

```python
# Find your cell number (e.g., [8]) and run:
%save -f student_bb84_impl.py 8
This cell number changes every time you run the vibe code cell , make sure to update the cell number here.
Make sure the vibe code is saved to your impl.py file.
Restart the kernel and start over if you face any isssues.
```

#### STEP 4: Track in Firebase

In the next cell:

```python
import notebook_tracker
notebook_tracker.track_bb84()
```

**Expected Output:**

```
Tracked BB84 cell: 25 lines, 687 chars
Creating method-level snapshots for BB84:
  > bb84_send_qubits: 18 lines
Total methods tracked: 1
```

#### STEP 5: Wait 5 Seconds

Wait before moving to the next method to allow background tracking to complete.

---

### Progress Tracker

Use this checklist as you implement:

| Method | Cell # | Saved | Tracked | Notes |
|--------|--------|-------|---------|-------|
| `bb84_send_qubits` | ___ | ☐ | ☐ | Alice prepares qubits |
| `process_received_qbit` | ___ | ☐ | ☐ | Bob measures qubits |
| `bb84_reconcile_bases` | ___ | ☐ | ☐ | Compare bases |
| `bb84_estimate_error_rate` | ___ | ☐ | ☐ | Calculate errors |

---

## Implementing B92 Protocol

### The 4 Methods You'll Implement

| Method | Purpose | What It Does |
|--------|---------|--------------|
| `b92_send_qubits` | Prepare qubits | Encode bits using only \|0⟩ or \|+⟩ states |
| `b92_process_received_qbit` | Measure qubits | Measure in random basis, store results |
| `b92_sifting` | Filter results | Keep only conclusive measurements |
| `b92_estimate_error_rate` | Check security | Calculate error rate from sample |

---

### Complete Workflow (Same as BB84)

| Step | BB84 Command | B92 Command |
|------|--------------|-------------|
| **Save** | `%save -f student_bb84_impl.py <cell#>` | `%save -f student_b92_impl.py <cell#>` |
| **Track** | `notebook_tracker.track_bb84()` | `notebook_tracker.track_b92()` |

---

### B92 Implementation Template

```python
class StudentB92Host:
    def __init__(self, name):
        self.name = name
        self.sent_bits = []
        self.received_measurements = []
    
    def b92_send_qubits(self, num_qubits):
        """Send qubits using B92 protocol (|0⟩ or |+⟩ only)"""
        # Your implementation here
        pass
    
    def b92_process_received_qbit(self, qbit, from_channel):
        """Measure received qubit"""
        # Your implementation here
        pass
    
    def b92_sifting(self, sent_bits, received_measurements):
        """Keep only conclusive measurements"""
        # Your implementation here
        pass
    
    def b92_estimate_error_rate(self, sample_positions, reference_bits):
        """Calculate error rate"""
        # Your implementation here
        pass
```

---

### Progress Tracker

| Method | Cell # | Saved | Tracked | Notes |
|--------|--------|-------|---------|-------|
| `b92_send_qubits` | ___ | ☐ | ☐ | Alice prepares |
| `b92_process_received_qbit` | ___ | ☐ | ☐ | Bob measures |
| `b92_sifting` | ___ | ☐ | ☐ | Filter results |
| `b92_estimate_error_rate` | ___ | ☐ | ☐ | Calculate errors |

---

## Visualizing Your Implementation

### Running the Simulation

After completing all methods for a protocol:

1. Scroll to the **last cell** in the notebook
2. Run the cell - this launches the QKD visualization
3. Watch your implementation execute in real-time
4. View qubit transmission, measurement, and key generation

### What You'll See

| Visualization Element | Description |
|----------------------|-------------|
| **Qubit Transmission** | Visual representation of qubits being sent from Alice to Bob |
| **Measurement Process** | Shows basis selection and measurement results |
| **Basis Reconciliation** | Displays which bases matched between Alice and Bob |
| **Key Generation** | Shows the final shared key after error estimation |
| **Statistics** | Error rate, key length, protocol efficiency metrics |

### Switching Between Protocols

To visualize a different protocol:

| To Switch To | Command | Then |
|--------------|---------|------|
| **BB84** | `python switch_to_bb84.py` | Run last cell to visualize BB84 |
| **B92** | `python switch_to_b92.py` | Run last cell to visualize B92 |

> **Note:** Run the switch command in terminal/command prompt, not in notebook cells

---

## How Tracking Works

### What Gets Tracked in Firebase

| Data Type | Description | Example |
|-----------|-------------|---------|
| **Code Snapshots** | Every version of your code | Full class implementation |
| **Timestamps** | When you wrote each method | `2024-10-14T12:35:00` |
| **Lines Added** | New code you added | `+25 lines` |
| **Lines Removed** | Code you deleted | `-3 lines` |
| **Time Spent** | Duration per method | `8 minutes on bb84_send_qubits` |
| **Method Evolution** | Changes to individual methods | Method-level snapshots |

---

### Tracking Timeline

```
You write code → Save file → Track in Firebase
                                    ↓
                    ┌───────────────────────────────┐
                    │   FIREBASE DATABASE           │
                    │                               │
                    │  ✓ Code snapshot saved        │
                    │  ✓ Timestamp recorded         │
                    │  ✓ Line count calculated      │
                    │  ✓ Method changes detected    │
                    └───────────────────────────────┘
                                    ↓
            Background watcher (every 3 seconds)
                    ↓
    Creates automatic snapshots of file changes
```

---

### Firebase Data Structure

**What your instructor sees:**

| Field | Value |
|-------|-------|
| **Student ID** | `your_student_id` |
| **Session ID** | `20241014_123456` |
| **Protocol** | `BB84` or `B92` |
| **Method** | `bb84_send_qubits` |
| **Lines** | `25` |
| **Characters** | `687` |
| **Time Spent** | `8 minutes` |
| **Timestamp** | `2024-10-14T12:35:00` |

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Tracker Not Initialized

| Symptom | Solution |
|---------|----------|
| `Tracker not initialized` error | Run Cell 1 (tracking setup) first |
| No Firebase connection message | Enter your student ID when prompted |
| Session ID missing | Restart kernel and re-run Cell 1 |

**Fix:**

```python
import notebook_tracker
notebook_tracker.init_tracker(student_id, use_firebase=True)
```

---

#### Issue 2: Firebase Connection Slow

| Phase | Normal Time | Action If Slow |
|-------|-------------|----------------|
| Step 1: Init Firebase | 5-10 sec | Wait up to 30 sec (normal on first connection) |
| Step 2: Student setup | 3-5 sec | Check internet connection |
| Step 3: Session create | 2-5 sec | Restart if > 1 min |

> **Note:** First connection can take 10-30 seconds. This is normal.

---

#### Issue 3: File Not Found Error

| Error | Cause | Solution |
|-------|-------|----------|
| `student_bb84_impl.py not found` | Forgot to save | Run `%save -f student_bb84_impl.py <cell#>` |
| `student_b92_impl.py not found` | Forgot to save | Run `%save -f student_b92_impl.py <cell#>` |
| Wrong cell number | Cell number changed | Check current cell number `[##]` |

**Always save BEFORE tracking:**

```python
# 1. Save first
%save -f student_bb84_impl.py 8

# 2. Then track
notebook_tracker.track_bb84()
```

---

#### Issue 4: Docker Container Conflicts

| Error Message | Command to Fix |
|---------------|----------------|
| `container name "/redis" is already in use` | `docker rm -f redis` |
| `container name "/python-server" is already in use` | `docker rm -f python-server` |
| `container name "/celery" is already in use` | `docker rm -f celery` |
| Multiple conflicts | `docker rm -f redis python-server celery caddy redis-commander` |

**Complete fix:**

```bash
# Remove all conflicting containers
docker rm -f redis python-server celery caddy redis-commander

# Start fresh
docker-compose up -d
```

---

#### Issue 5: Wrong Protocol Showing

| You Want | But Seeing | Solution |
|----------|------------|----------|
| BB84 logs | B92 logs | `python switch_to_bb84.py` |
| B92 logs | BB84 logs | `python switch_to_b92.py` |

**To switch protocols:**

```bash
# Switch to BB84
python switch_to_bb84.py

# Switch to B92
python switch_to_b92.py
```

Then run the last cell in notebook to visualize the selected protocol.

---

#### Issue 6: %save Command Not Working

| Error | Cause | Solution |
|-------|-------|----------|
| `Line magic function %save not found` | Not in Jupyter | Must run in notebook cell |
| `UsageError` | Wrong syntax | Use: `%save -f filename.py <cell#>` |

**Correct usage:**

```python
# In Jupyter notebook cell (not terminal!)
%save -f student_bb84_impl.py 8
```

---

## Quick Reference

### Complete Workflow Checklist

| # | Task | Command/Action | Done |
|---|------|----------------|------|
| **1** | Install software | `install.bat` or `install_*.sh` | ☐ |
| **2** | Clone repository | `git clone ...` | ☐ |
| **3** | Start Docker | `docker-compose up -d` | ☐ |
| **4** | Open in VS Code/Cursor | File → Open Folder | ☐ |
| **5** | Open notebook file | Click on `qsimnotebook.ipynb` | ☐ |
| **6** | Run tracking setup | Cell 1 → Enter student ID | ☐ |
| **7** | Implement BB84 (4 methods) | Write, save, track each method | ☐ |
| **8** | Visualize BB84 | Run last cell in notebook | ☐ |
| **9** | Switch to B92 | `python switch_to_b92.py` | ☐ |
| **10** | Implement B92 (4 methods) | Write, save, track each method | ☐ |
| **11** | Visualize B92 | Run last cell in notebook | ☐ |

---

### Essential Commands Reference

#### Docker Commands

| Task | Command |
|------|---------|
| Start containers | `docker-compose up -d` |
| Stop containers | `docker-compose down` |
| View running containers | `docker ps` |
| View logs | `docker-compose logs -f` |
| Rebuild containers | `docker-compose up --build` |
| Remove specific container | `docker rm -f <container_name>` |
| Remove all containers | `docker rm -f redis python-server celery caddy redis-commander` |

---

#### Protocol Switching

| Task | Command |
|------|---------|
| Switch to BB84 | `python switch_to_bb84.py` |
| Switch to B92 | `python switch_to_b92.py` |
| Check current protocol | `python -c "from protocol_detection_utils import detect_active_protocol; print(detect_active_protocol())"` |

---

#### Notebook Operations

| Task | Command | Notes |
|------|---------|-------|
| Save BB84 code | `%save -f student_bb84_impl.py <cell#>` | In notebook cell |
| Save B92 code | `%save -f student_b92_impl.py <cell#>` | In notebook cell |
| Track BB84 | `notebook_tracker.track_bb84()` | After saving |
| Track B92 | `notebook_tracker.track_b92()` | After saving |
| Visualize protocol | Run last cell in notebook | Shows QKD simulation |

---

### Tips for Success

| Category | Tip |
|----------|-----|
| **Setup** | Always run tracking setup (Cell 1) before coding |
| **Saving** | Use `%save` immediately after completing each method |
| **Tracking** | Run tracking cell after every save |
| **Timing** | Wait 5 seconds between methods for background watcher |
| **AI Usage** | Review and understand AI-generated code before saving |
| **Testing** | Run visualization (last cell) after completing all methods |
| **Switching** | Use `python switch_to_*.py` commands to change protocols |
| **Debugging** | Check troubleshooting section if errors occur |

---

## Frequently Asked Questions

| Question | Answer |
|----------|--------|
| **Do I need internet connection?** | Yes, Firebase requires internet to save your work |
| **What if I make a mistake?** | Firebase tracks all versions - your instructor can see your progress |
| **Can I work on BB84 and B92 simultaneously?** | No, complete BB84 first, then switch to B92 using `python switch_to_b92.py` |
| **How do I know tracking is working?** | You'll see "Tracked BB84 cell: X lines" message |
| **What if cell numbers change?** | Always check current cell number in `[brackets]` before using `%save` |
| **Can I edit after tracking?** | Yes, background watcher captures all changes automatically |
| **How do I visualize my implementation?** | Run the last cell in the notebook |
| **What if Firebase connection is slow?** | First connection takes 10-30 seconds - this is normal |

---

## Summary

### Your Complete Journey

| Step | Action |
|------|--------|
| **1** | Install → Run platform-specific installer |
| **2** | Clone → Get the code repository |
| **3** | Docker → Start backend services |
| **4** | Open → Open notebook file in VS Code/Cursor |
| **5** | Setup → Initialize tracking with student ID |
| **6** | Implement → Write BB84 methods (4 total) |
| **7** | Track → Save and upload each method to Firebase |
| **8** | Visualize → Run last cell to see BB84 in action |
| **9** | Switch → Run `python switch_to_b92.py` |
| **10** | Implement → Write B92 methods (4 total) |
| **11** | Track → Save and upload each method to Firebase |
| **12** | Visualize → Run last cell to see B92 in action |
| **13** | Complete → All work automatically tracked in Firebase |

---

### What Makes This Lab Special

| Feature | Benefit |
|---------|---------|
| **Automatic Tracking** | No need to manually submit - everything saves automatically to Firebase |
| **Version History** | All code versions preserved with timestamps |
| **Time Analytics** | See how long you spent on each method |
| **AI-Assisted** | Use Copilot/Cursor to help write code |
| **Real-Time Monitoring** | Instructor can see your progress live |
| **Fair Assessment** | Your learning process is visible, not just final code |
| **Interactive Visualization** | See your QKD implementation in action |

---

**Good luck with your quantum networking lab!**

> Remember: It's not just about the final code - your learning journey is tracked and valued!
