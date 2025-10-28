# Quantum Key Distribution Lab - Student Guide

> **Welcome!** This guide will walk you through setting up and completing your quantum networking lab assignment. Your work will be automatically tracked and saved to Firebase.

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/prateek780/qsimnotebookfinal)
[![Python](https://img.shields.io/badge/Python-3.9+-green?logo=python)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green?logo=nodedotjs)](https://nodejs.org/)
[![Docker](https://img.shields.io/badge/Docker-Optional-blue?logo=docker)](https://www.docker.com/)
[![JupyterLab](https://img.shields.io/badge/JupyterLab-4.4+-orange?logo=jupyter)](https://jupyter.org/)

---

## Table of Contents

- [Quick Start (3 Options)](#quick-start-3-options)
- [Installation Methods](#installation-methods)
  - [Option 1: Docker (Easiest - Recommended)](#option-1-docker-easiest---recommended)
  - [Option 2: Auto-Installer (With AI Extension)](#option-2-auto-installer-with-ai-extension)
  - [Option 3: Manual Installation](#option-3-manual-installation)
- [Getting Started](#getting-started)
- [Using the AI Code Assistant (edu_agents)](#using-the-ai-code-assistant-edu_agents)
- [Implementing BB84 Protocol](#implementing-bb84-protocol)
- [Implementing B92 Protocol](#implementing-b92-protocol)
- [Visualizing Your Implementation](#visualizing-your-implementation)
- [How Tracking Works](#how-tracking-works)
- [Troubleshooting](#troubleshooting)
- [Quick Reference](#quick-reference)
- [FAQ](#frequently-asked-questions)

---

## Quick Start (3 Options)

Choose the method that works best for you:

### 🐳 Option 1: Docker (Fastest - 5 Minutes)
```bash
docker-compose -f docker-compose.jupyter.yaml up --build
```
**Then open:** http://localhost:8888
- ✅ Everything included (Python, Node.js, JupyterLab, AI extension)
- ✅ No manual installation needed
- ✅ Works on Windows, Mac, Linux

### 🔧 Option 2: Auto-Installer (10 Minutes)
**Windows:** `install.bat`  
**Linux:** `chmod +x install_linux.sh && ./install_linux.sh`  
**Mac:** `chmod +x install_mac.sh && ./install_mac.sh`
- ✅ Installs Python, Node.js, Docker
- ✅ Builds AI extension automatically
- ✅ Platform-specific optimization

### 💻 Option 3: Manual (Advanced Users)
```bash
pip install -r quantum_requirements.txt
python -m jupyter lab
```
- ⚠️ Requires Python 3.9+ and Node.js 18+
- ⚠️ AI extension requires manual build
- ✅ Full control over setup

---

## Installation Methods

### Option 1: Docker (Easiest - Recommended)

Perfect for students who want to start immediately without installing dependencies.

#### Requirements
- Docker Desktop installed ([Download here](https://www.docker.com/products/docker-desktop))
- 4 GB RAM available
- 10 GB disk space

#### Quick Start

**Single Command:**
```bash
docker-compose -f docker-compose.jupyter.yaml up --build
```

**What This Does:**
- ✅ Installs Python 3.13
- ✅ Installs Node.js 24.x
- ✅ Installs all quantum libraries (qutip, qiskit)
- ✅ Builds edu_agents AI extension automatically
- ✅ Starts JupyterLab on port 8888

**Access:**
- JupyterLab: http://localhost:8888
- No password required
- AI assistant in left sidebar

**First build:** 5-10 minutes (downloads and builds everything)  
**Subsequent starts:** ~10 seconds

#### Docker Management

**Stop the container:**
```bash
docker-compose -f docker-compose.jupyter.yaml down
```

**View logs:**
```bash
docker-compose -f docker-compose.jupyter.yaml logs -f jupyter
```

**Restart (after code changes):**
```bash
docker-compose -f docker-compose.jupyter.yaml restart
```

**Rebuild completely:**
```bash
docker-compose -f docker-compose.jupyter.yaml up --build --force-recreate
```

#### Full Stack Docker (Backend + Redis + Jupyter)

If you need the complete simulation backend:

```bash
docker-compose up --build
```

**Access points:**
- JupyterLab: http://localhost:8888
- Python API: http://localhost:8000
- Redis Commander: http://localhost:8081
- Caddy Proxy: http://localhost:8001

---

### Option 2: Auto-Installer (With AI Extension)

Automated installers that set up everything including the AI coding assistant.

#### What Gets Installed

All platforms install:
- ✅ **Python 3.9+** (3.13 on Windows/Mac, 3.11+ on Linux)
- ✅ **Node.js 18+** (24.x LTS) - **NEW!** Required for AI extension
- ✅ **Docker Desktop** (optional, for backend services)
- ✅ **JupyterLab 4.4+** with extensions
- ✅ **edu_agents extension** - AI coding assistant (built automatically)
- ✅ **All quantum libraries** (qutip, qiskit, numpy, scipy, matplotlib)
- ✅ **faiss-cpu** - Vector database for AI features

#### Windows Installation

**Method 1: Run installer (Recommended)**
```cmd
install.bat
```

Or with PowerShell:
```powershell
.\install.ps1
```

**Method 2: Direct installer**
```cmd
auto_installer_windows.bat
```

**What It Does:**
1. Checks for winget (Windows Package Manager)
2. Installs Python 3.13 if not present
3. Installs Node.js 24.x LTS if not present
4. Installs Docker Desktop if not present
5. Installs all Python dependencies
6. Navigates to `.plugins/edu_agent_plugin`
7. Runs `npm install` (extension dependencies)
8. Runs `pip install -e .` (Python package)
9. Installs `faiss-cpu` (AI vector database)
10. Builds extension: `jupyter labextension build .`
11. Enables extension: `jupyter server extension enable edu_agents`
12. Verifies all installations

**Time:** 15-20 minutes on first run

#### Linux Installation

```bash
chmod +x install_linux.sh
./install_linux.sh
```

**Supported distributions:**
- Ubuntu 18.04+
- Debian 10+
- Fedora 35+
- CentOS 8+
- Arch Linux
- Manjaro

**What It Does:**
1. Detects your Linux distribution
2. Updates system packages
3. Installs Python 3.11+ via package manager
4. Installs Node.js 24.x from NodeSource repository
5. Installs Docker + Docker Compose from official repo
6. Adds user to docker group
7. Installs all Python dependencies
8. Builds and installs edu_agents extension
9. Verifies installations

**Time:** 15-25 minutes depending on distribution

**Important:** After installation, log out and log back in for docker group changes to take effect.

#### Mac Installation

```bash
chmod +x install_mac.sh
./install_mac.sh
```

**Supports:**
- macOS 10.15 (Catalina) or later
- Intel Macs
- Apple Silicon (M1/M2/M3)

**What It Does:**
1. Checks/installs Homebrew
2. Updates Homebrew
3. Installs Python 3.13 via Homebrew
4. Installs Node.js 24.x via Homebrew
5. Installs Docker Desktop via Homebrew Cask
6. Prompts to start Docker Desktop
7. Installs all Python dependencies
8. Builds and installs edu_agents extension
9. Verifies installations

**Time:** 15-30 minutes (Homebrew installation takes time)

---

### Option 3: Manual Installation

For advanced users who want full control.

#### Prerequisites

Install these manually:
- Python 3.9 or higher
- Node.js 18 or higher (24.x LTS recommended)
- Docker Desktop (optional, for backend services)

#### Step 1: Clone Repository

```bash
git clone https://github.com/prateek780/qsimnotebookfinal
cd qsimnotebookfinal
```

#### Step 2: Install Python Dependencies

```bash
# Install quantum computing dependencies
pip install -r quantum_requirements.txt

# Install additional dependencies
pip install -r requirements.txt

# Install AI extension dependencies
pip install faiss-cpu
```

#### Step 3: Build AI Extension (Optional but Recommended)

```bash
# Navigate to extension directory
cd .plugins/edu_agent_plugin

# Install Node.js dependencies
npm install

# Install Python package
pip install -e .

# Build JupyterLab extension
python -m jupyter labextension build .

# Enable server extension
python -m jupyter server extension enable edu_agents

# Return to project root
cd ../..
```

#### Step 4: Verify Installation

```bash
# Check JupyterLab extensions
python -m jupyter labextension list
# Should show: edu_agents v0.1.0 enabled ok

# Check server extensions
python -m jupyter server extension list
# Should show: edu_agents 0.1.0 ok
```

#### Step 5: Start JupyterLab

```bash
# If jupyter command is available
jupyter lab

# Or use Python module syntax
python -m jupyter lab
```

---

## Getting Started

### Option A: Using Docker (Simplest)

**Step 1: Start JupyterLab**
```bash
docker-compose -f docker-compose.jupyter.yaml up -d
```

**Step 2: Open Browser**
- Navigate to: http://localhost:8888
- JupyterLab interface will load

**Step 3: Open Notebook**
- In file browser (left sidebar), double-click `qsimnotebook.ipynb`

**Step 4: Activate AI Assistant**
- Look for **edu_agents** icon in left sidebar
- Click to open AI coding assistant panel

---

### Option B: Using Local Installation

#### Step 1: Start Backend Services (Optional)

If using the full simulation backend:

```bash
# Make sure Docker Desktop is running
docker-compose up -d
```

Wait for: `Student BB84 implementation detected and ready`

**Or skip this if only using notebooks.**

#### Step 2: Start JupyterLab

Open terminal in project directory:

```bash
# Windows
python -m jupyter lab

# Linux/Mac
python3 -m jupyter lab
```

**What Happens:**
- JupyterLab starts on `http://localhost:8888`
- Browser automatically opens
- JupyterLab interface appears

#### Step 3: Open the Notebook

1. In the **file browser** (left sidebar), locate `qsimnotebook.ipynb`
2. **Double-click** the file to open it
3. Notebook opens in the main area

#### Step 4: Activate the AI Code Assistant

Look at the **left sidebar** of JupyterLab. You should see:

**edu_agents icon** (chat/assistant icon)

Click it to open the AI assistant panel.

**QKD Code Assistant** panel features:
- Chat interface
- Input box at the bottom
- "Ask me to generate BB84/B92 code or explain concepts..." placeholder
- Context-aware help for quantum concepts

**If you don't see it:**
1. Click the **edu_agents icon** in the left sidebar
2. Or check: View → Show edu_agents
3. Verify extension is installed: `jupyter labextension list`

---

## Using the AI Code Assistant (edu_agents)

### What is edu_agents?

The **edu_agents** extension is a JupyterLab plugin that provides:
- 🤖 **AI Coding Assistant** - Context-aware code generation
- 💬 **Interactive Chat** - Ask questions while coding
- 📚 **Concept Explanations** - Understand quantum networking
- 🔍 **Code Analysis** - Debug and improve your implementations
- 🎯 **Lab Guidance** - Hints for exercises
- ☁️ **Firebase-backed** - Cloud-connected AI features

### How to Use the AI Assistant

#### Step 1: Load the Magic Extension

**IMPORTANT:** Run this cell FIRST before any `%%vibe_code` cells:

```python
# Load vibe_magic extension
import vibe_magic
from IPython import get_ipython
ipython = get_ipython()
vibe_magic.load_ipython_extension(ipython)
print("✅ Vibe Code Magic: Loaded")
```

**You should see:** `✅ Vibe Code Magic: Loaded`

#### Step 2: Using %%vibe_code Cells

The `%%vibe_code` magic automatically:
- ✅ Validates your syntax
- ✅ Executes the code
- ✅ Saves to `student_bb84_impl.py` or `student_b92_impl.py`
- ✅ Tracks in Firebase
- ✅ Monitors for changes

**Important Rules:**
1. `%%vibe_code` **MUST be the first line** of the cell
2. **No comments or code before it**
3. Load the magic extension first (see Step 1)

**Example:**

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

**Output:**
```
VIBE CODE: Automatic Save & Track
============================================================
[1/4] Checking tracker...
Student ID: your_id
[2/4] Validating syntax...
Syntax valid
Protocol detected: BB84
[3/4] Executing code...
StudentQuantumHost 'Alice' initialized successfully!
Execution successful
[4/4] Saving and tracking...
Saved: 12 lines, 2 methods
File: student_bb84_impl.py
BB84 code tracked and saved to Firebase
============================================================
SUCCESS: Code executed, saved, and tracked
============================================================
```

#### Step 3: Ask AI for Help

In the **edu_agents** panel (left sidebar):

**Generate Code:**
```
write the __init__ method for BB84

def __init__(self, name):
```

**Explain Concepts:**
```
explain how BB84 works
```

```
explain the code for bb84_send_qubits
```

**Debug Code:**
```
why is my error rate so high?
```

```
what's wrong with my measurement logic?
```

**Get Hints:**
```
give me a hint for implementing bb84_reconcile_bases
```

#### Step 4: Initialize Student Tracking

> **CRITICAL:** Run this FIRST before doing anything else!

Find the **"STUDENT ACTIVITY TRACKING SETUP"** cell (usually Cell 1) and run it.

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
- **Creates Account** - Sets up your student record in Firebase
- **Starts Session** - Begins a new session with unique timestamp
- **Enables Code Tracking** - Records all your code changes
- **Enables AI Tracking** - Logs every AI assistant interaction
- **Background Monitor** - Watches for file changes every 3 seconds

---

## Implementing BB84 Protocol

### The 4 Methods You'll Implement

| Method | Purpose | What It Does |
|--------|---------|--------------|
| `__init__` | Initialize | Set up instance variables and lists |
| `bb84_send_qubits` | Prepare qubits | Generate random bits and bases, encode qubits |
| `process_received_qbit` | Measure qubits | Receive qubit, measure in random basis |
| `bb84_reconcile_bases` | Compare bases | Find matching measurement bases |
| `bb84_estimate_error_rate` | Check security | Calculate error rate to detect eavesdropping |

---

### Complete Workflow for EACH Method

#### Using %%vibe_code (Recommended)

| Step | Action | Details |
|------|--------|---------|
| **1** | **Load Magic** | Run the vibe_magic loader cell FIRST |
| **2** | **Read Prompt** | Review cell instructions |
| **3** | **Generate Code** | Use AI assistant in sidebar OR your IDE's AI |
| **4** | **Add to Cell** | Paste code into `%%vibe_code` cell |
| **5** | **Run Cell** | Execute - automatically saves and tracks |
| **6** | **Verify** | Check output for success message |

**Critical Rule:** 
```python
%%vibe_code   # ← MUST be first line, nothing before it!
import random  # ← Your code starts here

class StudentQuantumHost:
    # ... your implementation
```

❌ **WRONG:**
```python
# coding: utf-8   # ← Don't put this before %%vibe_code
%%vibe_code
```

✅ **CORRECT:**
```python
%%vibe_code
# coding: utf-8   # ← Put comments AFTER %%vibe_code
import random
```

---

### Example: Implementing Constructor

**Step 1: Read the prompt in notebook**

**Step 2: Ask AI (in edu_agents panel):**
```
Create a constructor that accepts a name parameter.
Store it as instance variable. Initialize 5 empty lists:
random_bits, measurement_bases, quantum_states, 
received_bases, measurement_outcomes.
Print confirmation message.

def __init__(self, name):
```

**Step 3: AI generates code - copy it**

**Step 4: Put in %%vibe_code cell:**

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

**Step 5: Run the cell** → Automatic save + track!

---

### Constructor Requirements

**Critical Fix:** Use `__init__` with **DOUBLE underscores**!

✅ **CORRECT:**
```python
def __init__(self, name):  # ← Double underscores before and after
```

❌ **WRONG:**
```python
def _init_(self, name):   # ← Single underscores - won't work!
def __init(self, name):   # ← Missing trailing underscores
def init__(self, name):   # ← Missing leading underscores
```

**Why it matters:** Python only recognizes `__init__` (with double underscores) as the constructor. Any other spelling creates a regular method that doesn't get called when creating objects.

---

## Implementing B92 Protocol

### The 5 Methods You'll Implement

| Method | Purpose | What It Does |
|--------|---------|--------------|
| `__init__` | Initialize | Set up instance variables for B92 |
| `b92_prepare_qubit` | Encode bit | Map bit to quantum state (0→\|0⟩, 1→\|+⟩) |
| `b92_measure_qubit` | Measure qubit | Randomly measure in Z or X basis |
| `b92_sifting` | Filter results | Keep only conclusive measurements (outcome=1) |
| `b92_send_qubits` | Send qubits | Generate bits and prepare qubits |
| `b92_process_received_qbit` | Receive qubit | Measure and store result |
| `b92_estimate_error_rate` | Check security | Calculate error rate |

---

### B92 Implementation Template

```python
%%vibe_code
import random


class StudentB92Host:
    def __init__(self, name):
        self.name = name
        self.sent_bits = []
        self.prepared_qubits = []
        self.received_measurements = []
        self.sifted_key = []
        self.random_bits = []
        self.measurement_outcomes = []
        self.received_bases = []
        print(f"StudentB92Host '{self.name}' initialized successfully!")
    
    def b92_prepare_qubit(self, bit):
        """Encode bit as quantum state"""
        if bit == 0:
            return '|0⟩'
        else:
            return '|+⟩'
    
    def b92_measure_qubit(self, qubit):
        """Measure in random basis"""
        basis = random.choice(["Z", "X"])
        # ... measurement logic
        return outcome, basis
    
    def b92_sifting(self, sent_bits, received_measurements):
        """Keep only conclusive results (outcome=1)"""
        # ... sifting logic
        return sifted_indices, sifted_key
    
    def b92_send_qubits(self, num_qubits):
        """Generate and prepare qubits"""
        # ... preparation logic
        return self.prepared_qubits
    
    def b92_process_received_qbit(self, qbit, from_channel=None):
        """Process received qubit"""
        # ... processing logic
        return True
    
    def b92_estimate_error_rate(self, sample_positions, reference_bits):
        """Calculate error rate"""
        # ... error calculation
        return error_rate
```

---

### Complete Workflow (Same as BB84)

| Step | BB84 | B92 |
|------|------|-----|
| **Magic Cell** | `%%vibe_code` at top | `%%vibe_code` at top |
| **Class Name** | `StudentQuantumHost` | `StudentB92Host` |
| **Saved To** | `student_bb84_impl.py` | `student_b92_impl.py` |
| **Auto-Track** | Yes, if using `%%vibe_code` | Yes, if using `%%vibe_code` |

---

## Visualizing Your Implementation

### Running the Simulation

After completing all methods for a protocol:

1. Scroll to the **last cell** in the notebook
2. Run the cell - launches the QKD visualization
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

All simulation runs are automatically saved to `simulation_logs/` folder.

**Log Location:**
```
qsimnotebookfinal/simulation_logs/
├── simulation_log_Untitled_Topology_20251028_143052.txt
├── simulation_log_Untitled_Topology_20251028_150234.txt
└── ...
```

**Log File Naming:**
- Format: `simulation_log_Untitled_Topology_YYYYMMDD_HHMMSS.txt`
- Date/Time: Timestamp when simulation started
- Protocol: BB84 or B92 indicated in file content

**What's Logged:**
- Protocol type and simulation start time
- Qubit generation and encoding details
- Basis selection for each qubit
- Measurement outcomes with timestamps
- Basis reconciliation results and efficiency
- Error rate calculations
- Final key generation statistics
- All network events during simulation

### Ask the AI Assistant About Your Logs

Use the **edu_agents** panel (left sidebar) to analyze results.

**Example Prompts:**

**Basic Analysis:**
```
What was my error rate in the last BB84 simulation?
Show me the key generation statistics from my recent run
How many qubits did I send in the last simulation?
```

**Debugging Help:**
```
Why is my error rate higher than expected?
Which methods failed in my last simulation?
What went wrong with basis reconciliation?
```

**Comparison:**
```
Compare my last two BB84 simulations
What's the difference between my BB84 and B92 performance?
```

---

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
| **Timestamps** | When you wrote each method | `2024-10-28T12:35:00` |
| **Lines Added** | New code you added | `+25 lines` |
| **Lines Removed** | Code you deleted | `-3 lines` |
| **Time Spent** | Duration per method | `8 minutes on bb84_send_qubits` |
| **Method Evolution** | Changes to individual methods | Method-level snapshots |

#### AI Interaction Tracking (With edu_agents)

| Data Type | Description | Example |
|-----------|-------------|---------|
| **Query Text** | Your full question to AI | Full prompt + skeleton function |
| **Query Lines** | Question split into array | Each line stored separately |
| **Response Text** | AI's full response | Generated code or explanation |
| **Response Lines** | Response split into array | Each line stored separately |
| **Request Type** | Code generation or explanation | `CODE` or `EXPLANATION` |
| **Protocol** | Which protocol you asked about | `BB84` or `B92` |
| **Lines Generated** | How many lines AI wrote | `15 lines` |
| **Timestamp** | When you asked | `2024-10-28T12:35:00` |

**What This Means:**
- Every question you ask the AI is saved
- Every code snippet the AI generates is saved
- Your instructor can see how you used AI assistance
- This helps evaluate your learning process, not just final code

---

### Tracking Timeline

```
You write code → %%vibe_code executes → Auto-save & Track
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

## Troubleshooting

### Installation Issues

#### Issue: Node.js Not Found

**Symptoms:**
```
'node' is not recognized as the name of a cmdlet
npm install fails
Extension build fails
```

**Solutions:**

**Windows:**
```cmd
winget install -e --id OpenJS.NodeJS.LTS
# Or download from: https://nodejs.org/
```

**Linux:**
```bash
curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**Mac:**
```bash
brew install node@24
```

**Verify:**
```bash
node --version  # Should show v24.x.x
npm --version   # Should show 10.x.x
```

---

#### Issue: edu_agents Extension Not Appearing

**Symptoms:**
- No AI assistant icon in JupyterLab sidebar
- Extension not listed in `jupyter labextension list`

**Solutions:**

**1. Verify extension is installed:**
```bash
python -m jupyter labextension list
# Should show: edu_agents v0.1.0 enabled ok
```

**2. Rebuild extension:**
```bash
cd .plugins/edu_agent_plugin
npm install
pip install -e .
pip install faiss-cpu
python -m jupyter labextension build .
python -m jupyter server extension enable edu_agents
cd ../..
```

**3. Clear JupyterLab cache:**
```bash
jupyter lab clean
jupyter lab build
```

**4. Restart JupyterLab:**
```bash
# Stop current instance (Ctrl+C)
# Start again
python -m jupyter lab
```

---

#### Issue: Docker Container Conflicts

| Error Message | Command to Fix |
|---------------|----------------|
| `container name "/redis" is already in use` | `docker rm -f redis` |
| `container name "/python-server" is already in use` | `docker rm -f python-server` |
| `container name "/jupyter-lab-quantum" is already in use` | `docker rm -f jupyter-lab-quantum` |
| Multiple conflicts | `docker rm -f redis python-server celery caddy redis-commander jupyter-lab-quantum` |

**Complete fix:**

```bash
# Remove all conflicting containers
docker-compose down

# Remove containers forcefully
docker rm -f redis python-server celery caddy redis-commander jupyter-lab-quantum

# Start fresh
docker-compose up -d

# Or for JupyterLab only
docker-compose -f docker-compose.jupyter.yaml up --build
```

---

#### Issue: Port 8888 Already in Use

**Symptoms:**
```
Port 8888 is already allocated
Address already in use
```

**Solutions:**

**Option 1: Stop existing Jupyter instance**
```bash
# Windows
taskkill /F /IM jupyter-lab.exe

# Linux/Mac
pkill -f jupyter-lab
```

**Option 2: Use different port**

Edit `docker-compose.jupyter.yaml`:
```yaml
ports:
  - "9999:8888"  # Change 9999 to any free port
```

Then access at: http://localhost:9999

**Option 3: Find and kill process**
```bash
# Windows
netstat -ano | findstr :8888
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8888 | xargs kill -9
```

---

#### Issue: %%vibe_code Magic Not Found

**Symptoms:**
```
UsageError: Line magic function `%%vibe_code` not found
UsageError: Cell magic %%vibe_code not found
```

**Solutions:**

**1. Load the magic FIRST:**
```python
import vibe_magic
from IPython import get_ipython
ipython = get_ipython()
vibe_magic.load_ipython_extension(ipython)
print("✅ Vibe Code Magic: Loaded")
```

**2. Verify it's loaded:**
```python
# Check available magics
ipython = get_ipython()
print('vibe_code' in ipython.magics_manager.magics['cell'])
# Should print: True
```

**3. Make sure %%vibe_code is FIRST line:**

❌ Wrong:
```python
# coding: utf-8
%%vibe_code
```

✅ Correct:
```python
%%vibe_code
# coding: utf-8
```

**4. Restart kernel and run all cells:**
- Kernel → Restart Kernel and Run All Cells
- Magic will load automatically

---

#### Issue: Constructor Not Working

**Symptoms:**
```
StudentQuantumHost() takes no arguments
TypeError: __init__() missing required positional argument: 'name'
```

**Cause:** Constructor name typo

❌ **Wrong:**
```python
def _init_(self, name):    # Single underscores
def __init(self, name):    # Missing trailing underscores
def init__(self, name):    # Missing leading underscores
```

✅ **Correct:**
```python
def __init__(self, name):  # DOUBLE underscores before AND after
```

**Fix:** Update your code with double underscores and re-run the `%%vibe_code` cell.

---

#### Issue: Firebase Connection Slow

| Phase | Normal Time | Action If Slow |
|-------|-------------|----------------|
| Step 1: Init Firebase | 5-10 sec | Wait up to 30 sec (normal on first connection) |
| Step 2: Student setup | 3-5 sec | Check internet connection |
| Step 3: Session create | 2-5 sec | Restart if > 1 min |

> **Note:** First connection can take 10-30 seconds. This is normal.

---

#### Issue: Docker Build Fails

**Symptoms:**
```
Error building image
npm install failed
Extension build failed
```

**Solutions:**

**1. Check Docker has enough resources:**
- Open Docker Desktop → Settings → Resources
- RAM: Minimum 4GB, recommended 8GB
- Disk: Minimum 10GB free space

**2. Clean Docker cache:**
```bash
docker system prune -a
```

**3. Rebuild with no cache:**
```bash
docker-compose -f docker-compose.jupyter.yaml build --no-cache
docker-compose -f docker-compose.jupyter.yaml up
```

**4. Check internet connection:**
- Docker needs to download packages
- npm needs to download dependencies
- First build downloads ~2GB

**5. Check logs:**
```bash
docker-compose -f docker-compose.jupyter.yaml logs jupyter
```

---

## Quick Reference

### Complete Workflow Checklist

| # | Task | Command/Action | Done |
|---|------|----------------|------|
| **1** | Install software | See [Installation Methods](#installation-methods) | ☐ |
| **2** | Clone repository | `git clone <repo-url>` | ☐ |
| **3** | Choose setup method | Docker (easiest) or Local | ☐ |
| **4A** | Docker: Start JupyterLab | `docker-compose -f docker-compose.jupyter.yaml up -d` | ☐ |
| **4B** | Local: Start backend (optional) | `docker-compose up -d` | ☐ |
| **4C** | Local: Start JupyterLab | `python -m jupyter lab` | ☐ |
| **5** | Open in browser | http://localhost:8888 | ☐ |
| **6** | Open notebook | Double-click `qsimnotebook.ipynb` | ☐ |
| **7** | Check AI Assistant | Look for edu_agents icon in left sidebar | ☐ |
| **8** | Load vibe_magic | Run magic loader cell | ☐ |
| **9** | Initialize tracking | Run Cell 1 → Enter student ID | ☐ |
| **10** | Implement BB84 | Use `%%vibe_code` cells + AI assistant | ☐ |
| **11** | Visualize BB84 | Run last cell in notebook | ☐ |
| **12** | Switch to B92 | `python switch_to_b92.py` | ☐ |
| **13** | Implement B92 | Use `%%vibe_code` cells + AI assistant | ☐ |
| **14** | Visualize B92 | Run last cell in notebook | ☐ |

---

### Essential Commands Reference

#### JupyterLab Commands

| Task | Command | Notes |
|------|---------|-------|
| Start JupyterLab | `python -m jupyter lab` | Opens browser automatically |
| Start (if path works) | `jupyter lab` | Shorter command if available |
| Stop JupyterLab | `Ctrl+C` in terminal (twice) | Or close terminal window |
| Check if running | Open `http://localhost:8888` | Should show JupyterLab interface |
| Check extensions | `jupyter labextension list` | Shows installed extensions |
| Rebuild extensions | `jupyter lab build` | After extension changes |

---

#### Docker Commands

**JupyterLab Only:**
| Task | Command |
|------|---------|
| Build and start | `docker-compose -f docker-compose.jupyter.yaml up --build` |
| Start (detached) | `docker-compose -f docker-compose.jupyter.yaml up -d` |
| Stop | `docker-compose -f docker-compose.jupyter.yaml down` |
| View logs | `docker-compose -f docker-compose.jupyter.yaml logs -f jupyter` |
| Restart | `docker-compose -f docker-compose.jupyter.yaml restart` |
| Rebuild (no cache) | `docker-compose -f docker-compose.jupyter.yaml build --no-cache` |

**Full Stack:**
| Task | Command |
|------|---------|
| Start all services | `docker-compose up -d` |
| Stop all services | `docker-compose down` |
| View running containers | `docker ps` |
| View logs | `docker-compose logs -f` |
| Rebuild containers | `docker-compose up --build` |
| Remove all containers | `docker rm -f redis python-server celery caddy redis-commander jupyter-lab-quantum` |

---

#### Protocol Switching

| Task | Command |
|------|---------|
| Switch to BB84 | `python switch_to_bb84.py` |
| Switch to B92 | `python switch_to_b92.py` |
| Check current protocol | `python -c "from protocol_detection_utils import detect_active_protocol; print(detect_active_protocol())"` |

---

#### Notebook Operations

**Using %%vibe_code (Recommended):**

| Task | Command | Notes |
|------|---------|-------|
| Load magic | Run vibe_magic loader cell | FIRST, before any %%vibe_code |
| Auto-save & track code | `%%vibe_code` at top of cell | Automatic save + track |
| Ask AI for help | Type in edu_agents panel | Left sidebar |
| Visualize protocol | Run last cell in notebook | Shows QKD simulation |
| View simulation logs | Check `simulation_logs/` folder | Automatic after each run |

**Manual Method (If not using %%vibe_code):**

| Task | Command | Notes |
|------|---------|-------|
| Save BB84 code | `%save -f student_bb84_impl.py <cell#>` | In notebook cell |
| Save B92 code | `%save -f student_b92_impl.py <cell#>` | In notebook cell |
| Track BB84 | `notebook_tracker.track_bb84()` | After saving |
| Track B92 | `notebook_tracker.track_b92()` | After saving |

---

### Tips for Success

| Category | Tip |
|----------|-----|
| **Setup** | Choose Docker for easiest setup - everything included! |
| **Installation** | Use auto-installers - they install Python + Node.js + extension |
| **Environment** | Use JupyterLab for access to edu_agents AI Assistant |
| **Extension** | Look for edu_agents icon in left sidebar (not right) |
| **Magic Loading** | Always load vibe_magic FIRST before using %%vibe_code |
| **Magic Syntax** | %%vibe_code must be THE FIRST LINE (no comments before it) |
| **Constructor** | Use `__init__` with DOUBLE underscores (not single!) |
| **Auto-Save** | Use `%%vibe_code` cells - they save and track automatically |
| **AI Questions** | Copy prompt + skeleton function to AI panel for best results |
| **AI Tracking** | All your AI questions/answers are saved to Firebase |
| **AI Usage** | Review and understand AI-generated code before using it |
| **Testing** | Run visualization (last cell) after completing all methods |
| **Switching** | Use `python switch_to_*.py` commands to change protocols |
| **Debugging** | Check troubleshooting section if errors occur |
| **Logs** | Check `simulation_logs/` for detailed run information |

---

## Frequently Asked Questions

### General Questions

| Question | Answer |
|----------|--------|
| **What's the easiest way to start?** | Use Docker! Just run: `docker-compose -f docker-compose.jupyter.yaml up --build` |
| **Do I need to install Python manually?** | Not with Docker! With auto-installer, it's automatic. Only manual installation requires it. |
| **Do I need Node.js?** | Only if installing locally and want the AI extension. Docker includes it. Auto-installer installs it. |
| **Do I need internet connection?** | Yes, for Firebase tracking and AI features |
| **What if I make a mistake?** | Firebase tracks all versions - instructor can see your progress |
| **Can I work on BB84 and B92 simultaneously?** | No, complete BB84 first, then switch to B92 |
| **How do I know tracking is working?** | See "SUCCESS: Code executed, saved, and tracked" after running %%vibe_code |
| **Can I edit after tracking?** | Yes, background watcher captures all changes automatically |
| **How do I visualize my implementation?** | Run the last cell in the notebook |
| **Where are my simulation logs saved?** | In `simulation_logs/` folder in project directory |

### Docker Questions

| Question | Answer |
|----------|--------|
| **Do I need Docker?** | No, but highly recommended! Makes setup much easier. |
| **What if Docker is slow?** | First build takes 5-10 minutes. Increase Docker memory to 8GB in settings. |
| **Can I use Docker for just JupyterLab?** | Yes! Use `docker-compose.jupyter.yaml` for standalone JupyterLab |
| **What about the backend services?** | Use full `docker-compose.yaml` if you need Redis and API server |
| **How do I update the Docker image?** | Run: `docker-compose up --build --force-recreate` |
| **Are my notebooks saved?** | Yes! They're mounted from your host directory - all changes persist |
| **Can I access notebooks from outside Docker?** | Yes, they're in your project directory, shared with container |

### JupyterLab & AI Extension Questions

| Question | Answer |
|----------|--------|
| **Do I have to use JupyterLab?** | No, but recommended for edu_agents AI Assistant |
| **Where is the AI Assistant?** | Left sidebar in JupyterLab → edu_agents icon |
| **Can I use AI in VS Code?** | No, edu_agents only works in JupyterLab. Use Copilot/Cursor instead |
| **Are my AI questions tracked?** | Yes! Every question and response saved to Firebase |
| **Can instructor see my AI questions?** | Yes, all AI interactions are logged with your student ID |
| **What if AI doesn't give good code?** | Review and fix the code - your edits are also tracked |
| **How do I ask AI for code?** | Copy prompt + skeleton from notebook, paste in AI panel |
| **Can I ask AI to explain things?** | Yes! Ask "explain how BB84 works" or "explain this code" |
| **What if AI panel doesn't appear?** | Click edu_agents icon in left sidebar |
| **Does AI work offline?** | No, needs internet connection |
| **What if extension build fails?** | Check Node.js is installed: `node --version` |

### %%vibe_code Magic Questions

| Question | Answer |
|----------|--------|
| **What is %%vibe_code?** | IPython cell magic that auto-saves and tracks your code |
| **Do I have to use it?** | No, but it makes life easier - auto-save + auto-track in one step |
| **Why "magic not found" error?** | You need to load the extension first - run the vibe_magic loader cell |
| **Where should %%vibe_code go?** | THE FIRST LINE of the cell, nothing before it |
| **Can I put comments before it?** | NO! Comments go AFTER %%vibe_code, not before |
| **What about # coding: utf-8?** | Put it AFTER %%vibe_code, not before |
| **Does it work in VS Code?** | Yes, if running Jupyter kernel in VS Code |
| **What if it doesn't save?** | Check you have write permissions in project directory |
| **Can I use it for B92?** | Yes! Works for both BB84 and B92 |

### Code Issues

| Question | Answer |
|----------|--------|
| **Why "takes no arguments" error?** | Constructor must be `__init__` with DOUBLE underscores, not `_init_` |
| **What's the difference between `__init__` and `_init_`?** | `__init__` is Python constructor (double underscore). `_init_` is just a method name. |
| **How do I know if my code is correct?** | Run %%vibe_code cell - it validates syntax before executing |
| **What if my implementation doesn't work?** | Check simulation logs in `simulation_logs/` folder for error details |
| **Can I test my code before visualizing?** | Yes, create test cells and call your methods directly |

---

## Installation Comparison

| Feature | Docker | Auto-Installer | Manual |
|---------|--------|----------------|--------|
| **Time to Setup** | 5-10 min (first time) | 15-20 min | 30+ min |
| **Python Install** | Automatic | Automatic | Manual |
| **Node.js Install** | Automatic | Automatic | Manual |
| **Extension Build** | Automatic | Automatic | Manual |
| **Difficulty** | ⭐ Easy | ⭐⭐ Medium | ⭐⭐⭐ Advanced |
| **Best For** | Everyone | Students | Developers |
| **AI Extension** | ✅ Included | ✅ Included | ⚠️ Manual setup |
| **Updates** | `docker-compose up --build` | Re-run installer | Manual |
| **Isolation** | ✅ Containerized | ❌ System-wide | ❌ System-wide |
| **Requirements** | Docker only | Internet | Python + Node.js |

---

## Summary

### Your Complete Journey

| Step | Action |
|------|--------|
| **1** | **Install** → Choose: Docker (easiest) or Auto-installer or Manual |
| **2** | **Start** → Docker: `docker-compose up` or Local: `jupyter lab` |
| **3** | **Open** → Browser: http://localhost:8888 |
| **4** | **Notebook** → Double-click `qsimnotebook.ipynb` |
| **5** | **AI** → Click edu_agents icon in left sidebar |
| **6** | **Magic** → Run vibe_magic loader cell |
| **7** | **Tracking** → Run Cell 1, enter student ID |
| **8** | **BB84** → Implement 4 methods using `%%vibe_code` + AI |
| **9** | **Visualize** → Run last cell to see BB84 simulation |
| **10** | **Switch** → Run `python switch_to_b92.py` |
| **11** | **B92** → Implement 5 methods using `%%vibe_code` + AI |
| **12** | **Visualize** → Run last cell to see B92 simulation |
| **13** | **Complete** → All code + AI interactions tracked in Firebase! |

---

### What Makes This Lab Special

| Feature | Benefit |
|---------|---------|
| **Docker Support** | One-command deployment - no dependency installation needed |
| **Auto-Installers** | Platform-specific installers handle Python + Node.js + extensions |
| **AI Code Assistant (edu_agents)** | Integrated AI panel helps generate and explain QKD code |
| **Automatic Tracking** | No manual submission - everything saves to Firebase automatically |
| **AI Interaction Tracking** | Every AI question/answer logged - shows how you learn |
| **Version History** | All code versions preserved with timestamps |
| **Time Analytics** | See how long you spent on each method |
| **Real-Time Monitoring** | Instructor can see your progress live |
| **Fair Assessment** | Your learning process is visible, not just final code |
| **Interactive Visualization** | See your QKD implementation in action |
| **Vibe Coding** | `%%vibe_code` cells auto-save and track in one step |
| **Cross-Platform** | Works on Windows, Mac, Linux with Docker or installers |

---

## Additional Resources

### Documentation Files

- **INSTALLATION_GUIDE.md** - Detailed installation instructions for all platforms
- **INSTALLER_SUMMARY.md** - Technical details about auto-installers
- **docker-compose.jupyter.yaml** - Simplified Docker config for JupyterLab only
- **docker-compose.yaml** - Full stack Docker config with all services
- **README.md** - Project overview and quick links

### Testing & Verification

- **test-docker-build.sh** - Test Docker setup (Linux/Mac)
- **test-docker-build.bat** - Test Docker setup (Windows)

### Helper Scripts

- **switch_to_bb84.py** - Switch simulation to BB84 protocol
- **switch_to_b92.py** - Switch simulation to B92 protocol
- **start-jupyter-docker.sh** - Quick-start JupyterLab in Docker (Linux/Mac)
- **start-jupyter-docker.bat** - Quick-start JupyterLab in Docker (Windows)
- **start-jupyter-docker.ps1** - Quick-start JupyterLab in Docker (PowerShell)

---

**Good luck with your quantum networking lab!**

> Remember: It's not just about the final code - your learning journey (including AI interactions) is tracked and valued!

---

## Need Help?

1. **Check Troubleshooting section** above
2. **Read INSTALLATION_GUIDE.md** for detailed setup help
3. **Check Docker logs:** `docker-compose logs jupyter`
4. **Verify extensions:** `jupyter labextension list`
5. **Ask the AI assistant** in JupyterLab sidebar
6. **Review simulation logs** in `simulation_logs/` folder

**Still stuck?** Check that:
- ✅ Docker Desktop is running (if using Docker)
- ✅ vibe_magic is loaded (run loader cell first)
- ✅ `%%vibe_code` is THE FIRST LINE (nothing before it)
- ✅ Constructor uses `__init__` with DOUBLE underscores
- ✅ edu_agents extension is installed: `jupyter labextension list`
