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
  - [Understanding Your Simulation Logs](#understanding-your-simulation-logs)
  - [Ask the Vibe Coding Agent](#ask-the-vibe-coding-agent-about-your-logs)
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

### Option 1: Using JupyterLab (Recommended with AI Assistant)

#### Step 1: Start JupyterLab

Open your terminal/command prompt in the project directory and run:

```bash
jupyter lab
```

**What Happens:**
- JupyterLab will start on `http://localhost:8888`
- Your browser will automatically open
- You'll see the JupyterLab interface with file browser on the left

#### Step 2: Open the Notebook

1. In the **file browser** (left sidebar), locate `qsimnotebook.ipynb`
2. **Double-click** the file to open it
3. The notebook will open in the main area

#### Step 3: Activate the AI Code Assistant

Look at the **right sidebar** of JupyterLab. You should see:

**QKD Code Assistant** panel with:
- Chat interface
- Input box at the bottom
- "Ask me to generate BB84/B92 code or explain concepts..." placeholder

**If you don't see it:**
1. Click the **puzzle piece icon** (🧩) on the right sidebar
2. The AI assistant panel should appear

#### Step 4: Using the AI Assistant

The AI assistant can help you with:

**✅ Generate Code:**
```
write the __init__ method for BB84

def __init__(self, name):
```

**✅ Explain Concepts:**
```
explain how BB84 works
```

```
explain the code for bb84_send_qubits
```

**✅ Analyze Simulation Logs:**
```
summarize my QKD simulation logs
```

**What Gets Tracked:**
- Every question you ask the AI
- Every code snippet the AI generates
- Whether you requested code or explanation
- All stored in Firebase under your student ID

---

### Option 2: Using VS Code or Cursor

1. Open VS Code or Cursor IDE
2. **File** → **Open Folder**
3. Select `qsimnotebookfinal` folder
4. Locate `qsimnotebook.ipynb` file in the folder
5. Click on the notebook file to open it

> **Note:** The AI Code Assistant is only available in JupyterLab (Option 1)

---

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

Tracking initialized for your_student_id (Session: abc123...)
AI agent interactions will now be tracked in Firebase

TRACKING STARTED FOR STUDENT: your_student_id
```

**What This Does:**

- **Creates Account** - Sets up your student record in Firebase cloud database
- **Starts Session** - Begins a new coding session with unique timestamp ID
- **Enables Code Tracking** - Records all your code changes with timestamps
- **Enables AI Tracking** - Logs every AI assistant interaction (questions + responses)
- **Background Monitor** - Automatically watches for file changes every 3 seconds

> **Important:** After running this cell, the AI Code Assistant in JupyterLab will automatically link to your student ID

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
| **2** | **Generate Code** | Use **QKD Code Assistant** in JupyterLab sidebar (recommended) OR your IDE's AI (Copilot/Cursor) |
| **3** | **Save Code** | Use `%%vibe_code` magic command (auto-saves) OR manual `%save` |
| **4** | **Track Code** | Automatic with `%%vibe_code` OR manual `notebook_tracker.track_bb84()` |
| **5** | **Verify** | Run the visualization cell to test your implementation |

---

### Method 1: Using JupyterLab AI Assistant (Recommended)

This method automatically saves and tracks your code!

#### STEP 1: Read the Prompt in the Notebook

Each method cell contains a detailed prompt explaining what to implement.

#### STEP 2: Ask the AI Assistant

In the **QKD Code Assistant** panel (right sidebar), paste your prompt + skeleton function:

**Example for `__init__` method:**
```
Create a constructor that accepts a single parameter for the host's identifier.
Store this identifier as an instance variable. Initialize five empty list attributes:
one for storing random binary values, one for preparation bases, one for encoded states,
one for measurement bases, one for measurement results.

def __init__(self, name):
```

**The AI will generate:**
```python
def __init__(self, name):
    self.name = name
    self.random_bits = []
    self.measurement_bases = []
    self.quantum_states = []
    self.received_bases = []
    self.measurement_outcomes = []
    print(f"StudentQuantumHost '{self.name}' initialized successfully!")
```

#### STEP 3: Copy and Run Code in Vibe Code Cell

Paste the generated code into the `%%vibe_code` cell:

```python
%%vibe_code
import random

class StudentQuantumHost:
    def __init__(self, name):
        self.name = name
        self.random_bits = []
        self.measurement_bases = []
        self.quantum_states = []
        self.received_bases = []
        self.measurement_outcomes = []
        print(f"StudentQuantumHost '{self.name}' initialized successfully!")
```

**Run the cell** - it will:
- ✅ Validate syntax
- ✅ Execute code
- ✅ Save to `student_bb84_impl.py`
- ✅ Track in Firebase automatically

**Terminal will show:**
```
[AI Tracking] Using student: test123, session: abc123
[AI Tracking] Successfully logged: xyz789
```

---

### Method 2: Manual Method (VS Code/Cursor)

#### STEP 1: Read the Prompt

```python
# PROMPT: Implement the bb84_send_qubits method
# This method should:
# 1. Generate random bits (0 or 1) for each qubit
# 2. Generate random bases (rectilinear or diagonal)
# 3. Encode bits in qubits using the chosen bases
# 4. Send qubits to Bob through quantum channel
```

#### STEP 2: Write Code with Your IDE's AI

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

### Understanding Your Simulation Logs

All simulation runs are automatically saved to your local machine in the `simulation_logs/` folder. Each log file contains detailed information about your QKD protocol execution, including timestamps and event details.

**Log Location:**
```
qsimnotebookfinal/simulation_logs/
├── simulation_log_Untitled_Topology_20251020_143052.txt
├── simulation_log_Untitled_Topology_20251020_150234.txt
└── ...
```

**Log File Naming:**
- Format: `simulation_log_Untitled_Topology_YYYYMMDD_HHMMSS.txt`
- Date/Time: Timestamp when simulation started
- Protocol: BB84 or B92 is indicated inside the log file content

**What's Logged:**
- Protocol type (BB84 or B92) and simulation start time
- Qubit generation and encoding details
- Basis selection for each qubit
- Measurement outcomes with timestamps
- Basis reconciliation results and efficiency
- Error rate calculations
- Final key generation statistics
- All network events during simulation

### Ask the QKD Code Assistant About Your Logs

Use the **QKD Code Assistant** panel in JupyterLab (right sidebar) to analyze your simulation results.

**📍 Location:** Right sidebar of JupyterLab → QKD Code Assistant panel

**How to Use:**

1. Type your question in the chat input
2. The AI will analyze your logs and respond
3. All interactions are automatically tracked in Firebase

**Example Prompts:**

**Basic Analysis:**
```
What was my error rate in the last BB84 simulation?
```
```
Show me the key generation statistics from my recent run
```
```
How many qubits did I send in the last simulation?
```

**Debugging Help:**
```
Why is my error rate higher than expected?
```
```
Which methods failed in my last simulation?
```
```
What went wrong with basis reconciliation?
```

**Explaining Code:**
```
explain the code for bb84_send_qubits
```
```
explain how BB84 basis reconciliation works
```

**Learning and Understanding:**
```
"Explain the measurement outcomes in my last B92 run"
"What percentage of my bases matched with Bob?"
"How efficient was my key generation process?"
```

**Comparison and Improvement:**
```
"Compare my last two BB84 simulations"
"How can I improve my error rate?"
"What's the difference between my BB84 and B92 performance?"
```

**Detailed Investigation:**
```
"Show me the first 10 qubits from my last simulation"
"What were the basis choices for unsuccessful measurements?"
"Analyze the pattern in my measurement errors"
```

To access your logs programmatically in the notebook:

```python
# View available log files
import os
log_files = sorted(os.listdir('simulation_logs'))
print(f"Total logs: {len(log_files)}")
for log in log_files[-5:]:  # Show last 5 logs
    print(f"  - {log}")

# Read the most recent log
latest_log = sorted(os.listdir('simulation_logs'))[-1]
with open(f'simulation_logs/{latest_log}', 'r') as f:
    log_content = f.read()
    
# Check which protocol was used
if 'BB84' in log_content:
    print("Protocol: BB84")
elif 'B92' in log_content:
    print("Protocol: B92")
    
# Display first 20 lines
print('\n'.join(log_content.split('\n')[:20]))
```

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

#### Code Activity Tracking

| Data Type | Description | Example |
|-----------|-------------|---------|
| **Code Snapshots** | Every version of your code | Full class implementation |
| **Timestamps** | When you wrote each method | `2024-10-14T12:35:00` |
| **Lines Added** | New code you added | `+25 lines` |
| **Lines Removed** | Code you deleted | `-3 lines` |
| **Time Spent** | Duration per method | `8 minutes on bb84_send_qubits` |
| **Method Evolution** | Changes to individual methods | Method-level snapshots |

#### AI Interaction Tracking (JupyterLab Only)

| Data Type | Description | Example |
|-----------|-------------|---------|
| **Query Text** | Your full question to AI | Full prompt + skeleton function |
| **Query Lines** | Question split into array | Each line stored separately |
| **Response Text** | AI's full response | Generated code or explanation |
| **Response Lines** | Response split into array | Each line stored separately |
| **Request Type** | Code generation or explanation | `CODE` or `EXPLANATION` |
| **Protocol** | Which protocol you asked about | `BB84` or `B92` |
| **Lines Generated** | How many lines AI wrote | `15 lines` |
| **Timestamp** | When you asked | `2024-10-14T12:35:00` |

**What This Means:**
- Every question you ask the AI is saved
- Every code snippet the AI generates is saved
- Your instructor can see how you used AI assistance
- This helps evaluate your learning process, not just final code

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
| **4** | Start JupyterLab (recommended) | `jupyter lab` in terminal | ☐ |
| **5** | Open notebook file | Double-click `qsimnotebook.ipynb` in file browser | ☐ |
| **6** | Run tracking setup | Cell 1 → Enter student ID | ☐ |
| **7** | Check AI Assistant | Look for "QKD Code Assistant" in right sidebar | ☐ |
| **8** | Implement BB84 (4 methods) | Use AI assistant + `%%vibe_code` cells | ☐ |
| **9** | Visualize BB84 | Run last cell in notebook | ☐ |
| **10** | Switch to B92 | `python switch_to_b92.py` | ☐ |
| **11** | Implement B92 (4 methods) | Use AI assistant + `%%vibe_code` cells | ☐ |
| **12** | Visualize B92 | Run last cell in notebook | ☐ |

---

### Essential Commands Reference

#### JupyterLab Commands

| Task | Command | Notes |
|------|---------|-------|
| Start JupyterLab | `jupyter lab` | Opens browser automatically |
| Stop JupyterLab | `Ctrl+C` in terminal (twice) | Or close terminal window |
| Restart JupyterLab | Stop, then `jupyter lab` again | Needed after extension updates |
| Check if running | Open `http://localhost:8888/lab` | Should show JupyterLab interface |

---

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

**JupyterLab Method (Automatic):**

| Task | Command | Notes |
|------|---------|-------|
| Auto-save & track code | `%%vibe_code` | At top of cell with your code |
| Ask AI for help | Type in "QKD Code Assistant" panel | Right sidebar |
| Visualize protocol | Run last cell in notebook | Shows QKD simulation |
| View simulation logs | Check `simulation_logs/` folder | Automatic after each run |

**Manual Method (VS Code/Cursor):**

| Task | Command | Notes |
|------|---------|-------|
| Save BB84 code | `%save -f student_bb84_impl.py <cell#>` | In notebook cell |
| Save B92 code | `%save -f student_b92_impl.py <cell#>` | In notebook cell |
| Track BB84 | `notebook_tracker.track_bb84()` | After saving |
| Track B92 | `notebook_tracker.track_b92()` | After saving |
| Visualize protocol | Run last cell in notebook | Shows QKD simulation |
| View simulation logs | Check `simulation_logs/` folder | Automatic after each run |

---

### Tips for Success

| Category | Tip |
|----------|-----|
| **Setup** | Always run tracking setup (Cell 1) before coding |
| **Environment** | Use JupyterLab for access to AI Code Assistant |
| **AI Assistant** | Check right sidebar for "QKD Code Assistant" panel |
| **Auto-Save** | Use `%%vibe_code` cells - they save and track automatically |
| **AI Questions** | Copy prompt + skeleton function to AI panel for best results |
| **AI Tracking** | All your AI questions/answers are saved to Firebase |
| **AI Usage** | Review and understand AI-generated code before using it |
| **Testing** | Run visualization (last cell) after completing all methods |
| **Switching** | Use `python switch_to_*.py` commands to change protocols |
| **Debugging** | Check troubleshooting section if errors occur |

---

## Frequently Asked Questions

### General Questions

| Question | Answer |
|----------|--------|
| **Do I need internet connection?** | Yes, Firebase requires internet to save your work |
| **What if I make a mistake?** | Firebase tracks all versions - your instructor can see your progress |
| **Can I work on BB84 and B92 simultaneously?** | No, complete BB84 first, then switch to B92 using `python switch_to_b92.py` |
| **How do I know tracking is working?** | You'll see "Tracked BB84 cell: X lines" message or Terminal shows "[AI Tracking] Successfully logged" |
| **What if cell numbers change?** | With `%%vibe_code`, no need to track cell numbers - it auto-saves |
| **Can I edit after tracking?** | Yes, background watcher captures all changes automatically |
| **How do I visualize my implementation?** | Run the last cell in the notebook |
| **What if Firebase connection is slow?** | First connection takes 10-30 seconds - this is normal |
| **Where are my simulation logs saved?** | In `simulation_logs/` folder in your project directory |
| **Can I delete old simulation logs?** | Yes, they're local files - but keep recent ones for analysis |

### JupyterLab & AI Assistant Questions

| Question | Answer |
|----------|--------|
| **Do I have to use JupyterLab?** | No, but it's recommended for access to the AI Code Assistant |
| **Where is the AI Assistant?** | Right sidebar in JupyterLab → "QKD Code Assistant" panel |
| **Can I use the AI in VS Code?** | No, the AI assistant only works in JupyterLab. Use Copilot/Cursor instead |
| **Are my AI questions tracked?** | Yes! Every question and response is saved to Firebase |
| **Can the instructor see my AI questions?** | Yes, all AI interactions are logged with your student ID |
| **What if AI doesn't give good code?** | Review and fix the code - your edits are also tracked |
| **How do I ask the AI for code?** | Copy the prompt + skeleton function from notebook, paste in AI panel |
| **Can I ask AI to explain things?** | Yes! Ask "explain how BB84 works" or "explain this code" |
| **What if AI panel doesn't appear?** | Click puzzle icon (🧩) on right sidebar to show it |
| **Does AI work offline?** | No, it needs connection to Ollama server (runs on lab server) |

---

## Summary

### Your Complete Journey

| Step | Action |
|------|--------|
| **1** | Install → Run platform-specific installer |
| **2** | Clone → Get the code repository |
| **3** | Docker → Start backend services |
| **4** | JupyterLab → Start with `jupyter lab` |
| **5** | Open → Double-click `qsimnotebook.ipynb` |
| **6** | Setup → Initialize tracking with student ID |
| **7** | AI Assistant → Check right sidebar for "QKD Code Assistant" |
| **8** | Implement → Use AI + `%%vibe_code` for BB84 methods (4 total) |
| **9** | Track → Automatic with each `%%vibe_code` run |
| **10** | Visualize → Run last cell to see BB84 in action |
| **11** | Switch → Run `python switch_to_b92.py` |
| **12** | Implement → Use AI + `%%vibe_code` for B92 methods (4 total) |
| **13** | Track → Automatic with each `%%vibe_code` run |
| **14** | Visualize → Run last cell to see B92 in action |
| **15** | Complete → All code + AI interactions tracked in Firebase |

---

### What Makes This Lab Special

| Feature | Benefit |
|---------|---------|
| **Automatic Tracking** | No need to manually submit - everything saves automatically to Firebase |
| **AI Code Assistant** | Integrated AI panel helps generate and explain QKD code |
| **AI Tracking** | Every AI interaction logged - shows how you learn |
| **Version History** | All code versions preserved with timestamps |
| **Time Analytics** | See how long you spent on each method |
| **Real-Time Monitoring** | Instructor can see your progress live |
| **Fair Assessment** | Your learning process is visible, not just final code |
| **Interactive Visualization** | See your QKD implementation in action |
| **Vibe Coding** | `%%vibe_code` cells auto-save and track in one step |

---

**Good luck with your quantum networking lab!**

> Remember: It's not just about the final code - your learning journey is tracked and valued!
