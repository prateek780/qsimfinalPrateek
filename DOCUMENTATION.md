# Quantum Key Distribution Lab - Student Guide

> **Welcome!** This guide will walk you through setting up and completing your quantum networking lab assignment. Your work will be automatically tracked and saved to Firebase.

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

---

## Installation

### Step 1: Install Required Software

<table>
<thead>
<tr>
<th width="20%">Operating System</th>
<th width="40%">Command</th>
<th width="40%">What It Installs</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Windows</strong></td>
<td><code>install.bat</code></td>
<td>Python 3.8+, Jupyter, Docker, Dependencies</td>
</tr>
<tr>
<td><strong>Linux</strong></td>
<td><code>chmod +x install_linux.sh && ./install_linux.sh</code></td>
<td>Python 3.8+, Jupyter, Docker, Dependencies</td>
</tr>
<tr>
<td><strong>macOS</strong></td>
<td><code>chmod +x install_mac.sh && ./install_mac.sh</code></td>
<td>Python 3.8+, Jupyter, Docker, Dependencies</td>
</tr>
</tbody>
</table>

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

<table>
<thead>
<tr>
<th width="10%">Step</th>
<th width="90%">Action</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>1</strong></td>
<td>Open VS Code or Cursor IDE</td>
</tr>
<tr>
<td><strong>2</strong></td>
<td>File → Open Folder</td>
</tr>
<tr>
<td><strong>3</strong></td>
<td>Select <code>qsimnotebookfinal</code> folder</td>
</tr>
<tr>
<td><strong>4</strong></td>
<td>Locate <code>qsimnotebook.ipynb</code> file in the folder</td>
</tr>
<tr>
<td><strong>5</strong></td>
<td>Click on the notebook file to open it</td>
</tr>
</tbody>
</table>

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

<table>
<thead>
<tr>
<th width="30%">Action</th>
<th width="70%">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Creates Account</strong></td>
<td>Sets up your student record in Firebase cloud database</td>
</tr>
<tr>
<td><strong>Starts Session</strong></td>
<td>Begins a new coding session with unique timestamp ID</td>
</tr>
<tr>
<td><strong>Enables Tracking</strong></td>
<td>Starts recording all your code changes with timestamps</td>
</tr>
<tr>
<td><strong>Background Monitor</strong></td>
<td>Automatically watches for file changes every 3 seconds</td>
</tr>
</tbody>
</table>

---

## Implementing BB84 Protocol

### The 4 Methods You'll Implement

<table>
<thead>
<tr>
<th width="30%">Method</th>
<th width="25%">Purpose</th>
<th width="45%">What It Does</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>bb84_send_qubits</code></td>
<td>Prepare qubits</td>
<td>Generate random bits and bases, encode qubits, send to Bob</td>
</tr>
<tr>
<td><code>process_received_qbit</code></td>
<td>Measure qubits</td>
<td>Receive qubit, measure in random basis, store result</td>
</tr>
<tr>
<td><code>bb84_reconcile_bases</code></td>
<td>Compare bases</td>
<td>Find matching measurement bases between Alice and Bob</td>
</tr>
<tr>
<td><code>bb84_estimate_error_rate</code></td>
<td>Check security</td>
<td>Calculate error rate to detect eavesdropping</td>
</tr>
</tbody>
</table>

---

### Complete Workflow for EACH Method

#### Step-by-Step Process

<table>
<thead>
<tr>
<th width="10%">Step</th>
<th width="30%">Action</th>
<th width="60%">Details</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>1</strong></td>
<td><strong>Read Prompt</strong></td>
<td>Review cell instructions - each cell has detailed explanation of what to implement</td>
</tr>
<tr>
<td><strong>2</strong></td>
<td><strong>Generate Code</strong></td>
<td>Use AI assistant (Copilot/Cursor) to help write implementation</td>
</tr>
<tr>
<td><strong>3</strong></td>
<td><strong>Save Code</strong></td>
<td><code>%save -f student_bb84_impl.py &lt;cell_number&gt;</code></td>
</tr>
<tr>
<td><strong>4</strong></td>
<td><strong>Track Code</strong></td>
<td><code>notebook_tracker.track_bb84()</code> - uploads to Firebase with timestamp</td>
</tr>
<tr>
<td><strong>5</strong></td>
<td><strong>Wait</strong></td>
<td>Pause 5 seconds - let background watcher capture changes</td>
</tr>
</tbody>
</table>

---

#### Detailed Example

**STEP 1: READ THE PROMPT**

```python
# PROMPT: Implement the bb84_send_qubits method
# This method should:
# 1. Generate random bits (0 or 1) for each qubit
# 2. Generate random bases (rectilinear or diagonal)
# 3. Encode bits in qubits using the chosen bases
# 4. Send qubits to Bob through quantum channel
```

**STEP 2: WRITE CODE WITH AI HELP**

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

**STEP 3: SAVE YOUR CODE**

In a new cell, run:

```python
# Find your cell number (e.g., [8]) and run:
%save -f student_bb84_impl.py 8
```

**STEP 4: TRACK IN FIREBASE**

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

**STEP 5: WAIT 5 SECONDS** before moving to the next method

---

### Progress Tracker

Use this checklist as you implement:

<table>
<thead>
<tr>
<th width="35%">Method</th>
<th width="15%">Cell #</th>
<th width="15%">Saved</th>
<th width="15%">Tracked</th>
<th width="20%">Notes</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>bb84_send_qubits</code></td>
<td>___</td>
<td>☐</td>
<td>☐</td>
<td>Alice prepares qubits</td>
</tr>
<tr>
<td><code>process_received_qbit</code></td>
<td>___</td>
<td>☐</td>
<td>☐</td>
<td>Bob measures qubits</td>
</tr>
<tr>
<td><code>bb84_reconcile_bases</code></td>
<td>___</td>
<td>☐</td>
<td>☐</td>
<td>Compare bases</td>
</tr>
<tr>
<td><code>bb84_estimate_error_rate</code></td>
<td>___</td>
<td>☐</td>
<td>☐</td>
<td>Calculate errors</td>
</tr>
</tbody>
</table>

---

## Implementing B92 Protocol

### The 4 Methods You'll Implement

<table>
<thead>
<tr>
<th width="35%">Method</th>
<th width="25%">Purpose</th>
<th width="40%">What It Does</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>b92_send_qubits</code></td>
<td>Prepare qubits</td>
<td>Encode bits using only |0⟩ or |+⟩ states</td>
</tr>
<tr>
<td><code>b92_process_received_qbit</code></td>
<td>Measure qubits</td>
<td>Measure in random basis, store results</td>
</tr>
<tr>
<td><code>b92_sifting</code></td>
<td>Filter results</td>
<td>Keep only conclusive measurements</td>
</tr>
<tr>
<td><code>b92_estimate_error_rate</code></td>
<td>Check security</td>
<td>Calculate error rate from sample</td>
</tr>
</tbody>
</table>

---

### Complete Workflow (Same as BB84)

<table>
<thead>
<tr>
<th width="15%">Step</th>
<th width="40%">BB84 Command</th>
<th width="40%">B92 Command</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Save</strong></td>
<td><code>%save -f student_bb84_impl.py &lt;cell#&gt;</code></td>
<td><code>%save -f student_b92_impl.py &lt;cell#&gt;</code></td>
</tr>
<tr>
<td><strong>Track</strong></td>
<td><code>notebook_tracker.track_bb84()</code></td>
<td><code>notebook_tracker.track_b92()</code></td>
</tr>
</tbody>
</table>

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

<table>
<thead>
<tr>
<th width="40%">Method</th>
<th width="15%">Cell #</th>
<th width="15%">Saved</th>
<th width="15%">Tracked</th>
<th width="15%">Notes</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>b92_send_qubits</code></td>
<td>___</td>
<td>☐</td>
<td>☐</td>
<td>Alice prepares</td>
</tr>
<tr>
<td><code>b92_process_received_qbit</code></td>
<td>___</td>
<td>☐</td>
<td>☐</td>
<td>Bob measures</td>
</tr>
<tr>
<td><code>b92_sifting</code></td>
<td>___</td>
<td>☐</td>
<td>☐</td>
<td>Filter results</td>
</tr>
<tr>
<td><code>b92_estimate_error_rate</code></td>
<td>___</td>
<td>☐</td>
<td>☐</td>
<td>Calculate errors</td>
</tr>
</tbody>
</table>

---

## Visualizing Your Implementation

### Running the Simulation

After completing all methods for a protocol:

<table>
<thead>
<tr>
<th width="15%">Step</th>
<th width="85%">Action</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>1</strong></td>
<td>Scroll to the <strong>last cell</strong> in the notebook</td>
</tr>
<tr>
<td><strong>2</strong></td>
<td>Run the cell - this launches the QKD visualization</td>
</tr>
<tr>
<td><strong>3</strong></td>
<td>Watch your implementation execute in real-time</td>
</tr>
<tr>
<td><strong>4</strong></td>
<td>View qubit transmission, measurement, and key generation</td>
</tr>
</tbody>
</table>

### What You'll See

<table>
<thead>
<tr>
<th width="30%">Visualization Element</th>
<th width="70%">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Qubit Transmission</strong></td>
<td>Visual representation of qubits being sent from Alice to Bob</td>
</tr>
<tr>
<td><strong>Measurement Process</strong></td>
<td>Shows basis selection and measurement results</td>
</tr>
<tr>
<td><strong>Basis Reconciliation</strong></td>
<td>Displays which bases matched between Alice and Bob</td>
</tr>
<tr>
<td><strong>Key Generation</strong></td>
<td>Shows the final shared key after error estimation</td>
</tr>
<tr>
<td><strong>Statistics</strong></td>
<td>Error rate, key length, protocol efficiency metrics</td>
</tr>
</tbody>
</table>

### Switching Between Protocols

To visualize a different protocol:

<table>
<thead>
<tr>
<th width="25%">To Switch To</th>
<th width="40%">Command</th>
<th width="35%">Then</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>BB84</strong></td>
<td><code>python switch_to_bb84.py</code></td>
<td>Run last cell to visualize BB84</td>
</tr>
<tr>
<td><strong>B92</strong></td>
<td><code>python switch_to_b92.py</code></td>
<td>Run last cell to visualize B92</td>
</tr>
</tbody>
</table>

> **Note:** Run the switch command in terminal/command prompt, not in notebook cells

---

## How Tracking Works

### What Gets Tracked in Firebase

<table>
<thead>
<tr>
<th width="30%">Data Type</th>
<th width="40%">Description</th>
<th width="30%">Example</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Code Snapshots</strong></td>
<td>Every version of your code</td>
<td>Full class implementation</td>
</tr>
<tr>
<td><strong>Timestamps</strong></td>
<td>When you wrote each method</td>
<td><code>2024-10-14T12:35:00</code></td>
</tr>
<tr>
<td><strong>Lines Added</strong></td>
<td>New code you added</td>
<td><code>+25 lines</code></td>
</tr>
<tr>
<td><strong>Lines Removed</strong></td>
<td>Code you deleted</td>
<td><code>-3 lines</code></td>
</tr>
<tr>
<td><strong>Time Spent</strong></td>
<td>Duration per method</td>
<td><code>8 minutes on bb84_send_qubits</code></td>
</tr>
<tr>
<td><strong>Method Evolution</strong></td>
<td>Changes to individual methods</td>
<td>Method-level snapshots</td>
</tr>
</tbody>
</table>

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

<table>
<thead>
<tr>
<th width="30%">Field</th>
<th width="70%">Value</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Student ID</strong></td>
<td><code>your_student_id</code></td>
</tr>
<tr>
<td><strong>Session ID</strong></td>
<td><code>20241014_123456</code></td>
</tr>
<tr>
<td><strong>Protocol</strong></td>
<td><code>BB84</code> or <code>B92</code></td>
</tr>
<tr>
<td><strong>Method</strong></td>
<td><code>bb84_send_qubits</code></td>
</tr>
<tr>
<td><strong>Lines</strong></td>
<td><code>25</code></td>
</tr>
<tr>
<td><strong>Characters</strong></td>
<td><code>687</code></td>
</tr>
<tr>
<td><strong>Time Spent</strong></td>
<td><code>8 minutes</code></td>
</tr>
<tr>
<td><strong>Timestamp</strong></td>
<td><code>2024-10-14T12:35:00</code></td>
</tr>
</tbody>
</table>

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Tracker Not Initialized

<table>
<thead>
<tr>
<th width="40%">Symptom</th>
<th width="60%">Solution</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>Tracker not initialized</code> error</td>
<td>Run Cell 1 (tracking setup) first</td>
</tr>
<tr>
<td>No Firebase connection message</td>
<td>Enter your student ID when prompted</td>
</tr>
<tr>
<td>Session ID missing</td>
<td>Restart kernel and re-run Cell 1</td>
</tr>
</tbody>
</table>

**Fix:**
```python
import notebook_tracker
notebook_tracker.init_tracker(student_id, use_firebase=True)
```

---

#### Issue 2: Firebase Connection Slow

<table>
<thead>
<tr>
<th width="25%">Phase</th>
<th width="25%">Normal Time</th>
<th width="50%">Action If Slow</th>
</tr>
</thead>
<tbody>
<tr>
<td>Step 1: Init Firebase</td>
<td>5-10 sec</td>
<td>Wait up to 30 sec (normal on first connection)</td>
</tr>
<tr>
<td>Step 2: Student setup</td>
<td>3-5 sec</td>
<td>Check internet connection</td>
</tr>
<tr>
<td>Step 3: Session create</td>
<td>2-5 sec</td>
<td>Restart if > 1 min</td>
</tr>
</tbody>
</table>

> **Note:** First connection can take 10-30 seconds. This is normal.

---

#### Issue 3: File Not Found Error

<table>
<thead>
<tr>
<th width="40%">Error</th>
<th width="30%">Cause</th>
<th width="30%">Solution</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>student_bb84_impl.py not found</code></td>
<td>Forgot to save</td>
<td>Run <code>%save -f student_bb84_impl.py &lt;cell#&gt;</code></td>
</tr>
<tr>
<td><code>student_b92_impl.py not found</code></td>
<td>Forgot to save</td>
<td>Run <code>%save -f student_b92_impl.py &lt;cell#&gt;</code></td>
</tr>
<tr>
<td>Wrong cell number</td>
<td>Cell number changed</td>
<td>Check current cell number <code>[##]</code></td>
</tr>
</tbody>
</table>

**Always save BEFORE tracking:**
```python
# 1. Save first
%save -f student_bb84_impl.py 8

# 2. Then track
notebook_tracker.track_bb84()
```

---

#### Issue 4: Docker Container Conflicts

<table>
<thead>
<tr>
<th width="60%">Error Message</th>
<th width="40%">Command to Fix</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>container name "/redis" is already in use</code></td>
<td><code>docker rm -f redis</code></td>
</tr>
<tr>
<td><code>container name "/python-server" is already in use</code></td>
<td><code>docker rm -f python-server</code></td>
</tr>
<tr>
<td><code>container name "/celery" is already in use</code></td>
<td><code>docker rm -f celery</code></td>
</tr>
<tr>
<td>Multiple conflicts</td>
<td><code>docker rm -f redis python-server celery caddy redis-commander</code></td>
</tr>
</tbody>
</table>

**Complete fix:**
```bash
# Remove all conflicting containers
docker rm -f redis python-server celery caddy redis-commander

# Start fresh
docker-compose up -d
```

---

#### Issue 5: Wrong Protocol Showing

<table>
<thead>
<tr>
<th width="25%">You Want</th>
<th width="25%">But Seeing</th>
<th width="50%">Solution</th>
</tr>
</thead>
<tbody>
<tr>
<td>BB84 logs</td>
<td>B92 logs</td>
<td><code>python switch_to_bb84.py</code></td>
</tr>
<tr>
<td>B92 logs</td>
<td>BB84 logs</td>
<td><code>python switch_to_b92.py</code></td>
</tr>
</tbody>
</table>

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

<table>
<thead>
<tr>
<th width="40%">Error</th>
<th width="30%">Cause</th>
<th width="30%">Solution</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>Line magic function %save not found</code></td>
<td>Not in Jupyter</td>
<td>Must run in notebook cell</td>
</tr>
<tr>
<td><code>UsageError</code></td>
<td>Wrong syntax</td>
<td>Use: <code>%save -f filename.py &lt;cell#&gt;</code></td>
</tr>
</tbody>
</table>

**Correct usage:**
```python
# In Jupyter notebook cell (not terminal!)
%save -f student_bb84_impl.py 8
```

---

## Quick Reference

### Complete Workflow Checklist

<table>
<thead>
<tr>
<th width="10%">#</th>
<th width="40%">Task</th>
<th width="40%">Command/Action</th>
<th width="10%">Done</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>1</strong></td>
<td>Install software</td>
<td><code>install.bat</code> or <code>install_*.sh</code></td>
<td>☐</td>
</tr>
<tr>
<td><strong>2</strong></td>
<td>Clone repository</td>
<td><code>git clone ...</code></td>
<td>☐</td>
</tr>
<tr>
<td><strong>3</strong></td>
<td>Start Docker</td>
<td><code>docker-compose up -d</code></td>
<td>☐</td>
</tr>
<tr>
<td><strong>4</strong></td>
<td>Open in VS Code/Cursor</td>
<td>File → Open Folder</td>
<td>☐</td>
</tr>
<tr>
<td><strong>5</strong></td>
<td>Open notebook file</td>
<td>Click on <code>qsimnotebook.ipynb</code></td>
<td>☐</td>
</tr>
<tr>
<td><strong>6</strong></td>
<td>Run tracking setup</td>
<td>Cell 1 → Enter student ID</td>
<td>☐</td>
</tr>
<tr>
<td><strong>7</strong></td>
<td>Implement BB84 (4 methods)</td>
<td>Write, save, track each method</td>
<td>☐</td>
</tr>
<tr>
<td><strong>8</strong></td>
<td>Visualize BB84</td>
<td>Run last cell in notebook</td>
<td>☐</td>
</tr>
<tr>
<td><strong>9</strong></td>
<td>Switch to B92</td>
<td><code>python switch_to_b92.py</code></td>
<td>☐</td>
</tr>
<tr>
<td><strong>10</strong></td>
<td>Implement B92 (4 methods)</td>
<td>Write, save, track each method</td>
<td>☐</td>
</tr>
<tr>
<td><strong>11</strong></td>
<td>Visualize B92</td>
<td>Run last cell in notebook</td>
<td>☐</td>
</tr>
</tbody>
</table>

---

### Essential Commands Reference

#### Docker Commands

<table>
<thead>
<tr>
<th width="40%">Task</th>
<th width="60%">Command</th>
</tr>
</thead>
<tbody>
<tr>
<td>Start containers</td>
<td><code>docker-compose up -d</code></td>
</tr>
<tr>
<td>Stop containers</td>
<td><code>docker-compose down</code></td>
</tr>
<tr>
<td>View running containers</td>
<td><code>docker ps</code></td>
</tr>
<tr>
<td>View logs</td>
<td><code>docker-compose logs -f</code></td>
</tr>
<tr>
<td>Rebuild containers</td>
<td><code>docker-compose up --build</code></td>
</tr>
<tr>
<td>Remove specific container</td>
<td><code>docker rm -f &lt;container_name&gt;</code></td>
</tr>
<tr>
<td>Remove all containers</td>
<td><code>docker rm -f redis python-server celery caddy redis-commander</code></td>
</tr>
</tbody>
</table>

---

#### Protocol Switching

<table>
<thead>
<tr>
<th width="40%">Task</th>
<th width="60%">Command</th>
</tr>
</thead>
<tbody>
<tr>
<td>Switch to BB84</td>
<td><code>python switch_to_bb84.py</code></td>
</tr>
<tr>
<td>Switch to B92</td>
<td><code>python switch_to_b92.py</code></td>
</tr>
<tr>
<td>Check current protocol</td>
<td><code>python -c "from protocol_detection_utils import detect_active_protocol; print(detect_active_protocol())"</code></td>
</tr>
</tbody>
</table>

---

#### Notebook Operations

<table>
<thead>
<tr>
<th width="40%">Task</th>
<th width="40%">Command</th>
<th width="20%">Notes</th>
</tr>
</thead>
<tbody>
<tr>
<td>Save BB84 code</td>
<td><code>%save -f student_bb84_impl.py &lt;cell#&gt;</code></td>
<td>In notebook cell</td>
</tr>
<tr>
<td>Save B92 code</td>
<td><code>%save -f student_b92_impl.py &lt;cell#&gt;</code></td>
<td>In notebook cell</td>
</tr>
<tr>
<td>Track BB84</td>
<td><code>notebook_tracker.track_bb84()</code></td>
<td>After saving</td>
</tr>
<tr>
<td>Track B92</td>
<td><code>notebook_tracker.track_b92()</code></td>
<td>After saving</td>
</tr>
<tr>
<td>Visualize protocol</td>
<td>Run last cell in notebook</td>
<td>Shows QKD simulation</td>
</tr>
</tbody>
</table>

---

### Tips for Success

<table>
<thead>
<tr>
<th width="25%">Category</th>
<th width="75%">Tip</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Setup</strong></td>
<td>Always run tracking setup (Cell 1) before coding</td>
</tr>
<tr>
<td><strong>Saving</strong></td>
<td>Use <code>%save</code> immediately after completing each method</td>
</tr>
<tr>
<td><strong>Tracking</strong></td>
<td>Run tracking cell after every save</td>
</tr>
<tr>
<td><strong>Timing</strong></td>
<td>Wait 5 seconds between methods for background watcher</td>
</tr>
<tr>
<td><strong>AI Usage</strong></td>
<td>Review and understand AI-generated code before saving</td>
</tr>
<tr>
<td><strong>Testing</strong></td>
<td>Run visualization (last cell) after completing all methods</td>
</tr>
<tr>
<td><strong>Switching</strong></td>
<td>Use <code>python switch_to_*.py</code> commands to change protocols</td>
</tr>
<tr>
<td><strong>Debugging</strong></td>
<td>Check troubleshooting section if errors occur</td>
</tr>
</tbody>
</table>

---

## Frequently Asked Questions

<table>
<thead>
<tr>
<th width="50%">Question</th>
<th width="50%">Answer</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Do I need internet connection?</strong></td>
<td>Yes, Firebase requires internet to save your work</td>
</tr>
<tr>
<td><strong>What if I make a mistake?</strong></td>
<td>Firebase tracks all versions - your instructor can see your progress</td>
</tr>
<tr>
<td><strong>Can I work on BB84 and B92 simultaneously?</strong></td>
<td>No, complete BB84 first, then switch to B92 using <code>python switch_to_b92.py</code></td>
</tr>
<tr>
<td><strong>How do I know tracking is working?</strong></td>
<td>You'll see "Tracked BB84 cell: X lines" message</td>
</tr>
<tr>
<td><strong>What if cell numbers change?</strong></td>
<td>Always check current cell number in <code>[brackets]</code> before using <code>%save</code></td>
</tr>
<tr>
<td><strong>Can I edit after tracking?</strong></td>
<td>Yes, background watcher captures all changes automatically</td>
</tr>
<tr>
<td><strong>How do I visualize my implementation?</strong></td>
<td>Run the last cell in the notebook</td>
</tr>
<tr>
<td><strong>What if Firebase connection is slow?</strong></td>
<td>First connection takes 10-30 seconds - this is normal</td>
</tr>
</tbody>
</table>

---

## Summary

### Your Complete Journey

<table>
<thead>
<tr>
<th width="10%">Step</th>
<th width="90%">Action</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>1</strong></td>
<td>Install → Run platform-specific installer</td>
</tr>
<tr>
<td><strong>2</strong></td>
<td>Clone → Get the code repository</td>
</tr>
<tr>
<td><strong>3</strong></td>
<td>Docker → Start backend services</td>
</tr>
<tr>
<td><strong>4</strong></td>
<td>Open → Open notebook file in VS Code/Cursor</td>
</tr>
<tr>
<td><strong>5</strong></td>
<td>Setup → Initialize tracking with student ID</td>
</tr>
<tr>
<td><strong>6</strong></td>
<td>Implement → Write BB84 methods (4 total)</td>
</tr>
<tr>
<td><strong>7</strong></td>
<td>Track → Save and upload each method to Firebase</td>
</tr>
<tr>
<td><strong>8</strong></td>
<td>Visualize → Run last cell to see BB84 in action</td>
</tr>
<tr>
<td><strong>9</strong></td>
<td>Switch → Run <code>python switch_to_b92.py</code></td>
</tr>
<tr>
<td><strong>10</strong></td>
<td>Implement → Write B92 methods (4 total)</td>
</tr>
<tr>
<td><strong>11</strong></td>
<td>Track → Save and upload each method to Firebase</td>
</tr>
<tr>
<td><strong>12</strong></td>
<td>Visualize → Run last cell to see B92 in action</td>
</tr>
<tr>
<td><strong>13</strong></td>
<td>Complete → All work automatically tracked in Firebase</td>
</tr>
</tbody>
</table>

---

### What Makes This Lab Special

<table>
<thead>
<tr>
<th width="30%">Feature</th>
<th width="70%">Benefit</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Automatic Tracking</strong></td>
<td>No need to manually submit - everything saves automatically to Firebase</td>
</tr>
<tr>
<td><strong>Version History</strong></td>
<td>All code versions preserved with timestamps</td>
</tr>
<tr>
<td><strong>Time Analytics</strong></td>
<td>See how long you spent on each method</td>
</tr>
<tr>
<td><strong>AI-Assisted</strong></td>
<td>Use Copilot/Cursor to help write code</td>
</tr>
<tr>
<td><strong>Real-Time Monitoring</strong></td>
<td>Instructor can see your progress live</td>
</tr>
<tr>
<td><strong>Fair Assessment</strong></td>
<td>Your learning process is visible, not just final code</td>
</tr>
<tr>
<td><strong>Interactive Visualization</strong></td>
<td>See your QKD implementation in action</td>
</tr>
</tbody>
</table>

---

**Good luck with your quantum networking lab!**

> Remember: It's not just about the final code - your learning journey is tracked and valued!
