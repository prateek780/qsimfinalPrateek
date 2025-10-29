# Quantum Key Distribution Lab - Student Guide

Welcome to the Quantum Key Distribution (QKD) lab. This guide provides step-by-step instructions to set up your environment, implement BB84 and B92 protocols, and complete your assignment. All your work is automatically tracked and saved to Firebase.

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/prateek780/qsimnotebookfinal)
[![Python](https://img.shields.io/badge/Python-3.9+-green?logo=python)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green?logo=nodedotjs)](https://nodejs.org/)
[![Docker](https://img.shields.io/badge/Docker-Required-blue?logo=docker)](https://www.docker.com/)

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step 1: Clone the Repository](#step-1-clone-the-repository)
3. [Step 2: Run the Auto-Installer](#step-2-run-the-auto-installer)
4. [Step 3: Start Docker Desktop](#step-3-start-docker-desktop)
5. [Step 4: Launch JupyterLab with Docker](#step-4-launch-jupyterlab-with-docker)
6. [Step 5: Open the Notebook](#step-5-open-the-notebook)
7. [Step 6: Initialize Student Tracking](#step-6-initialize-student-tracking)
8. [Step 7: Load the Magic Extension](#step-7-load-the-magic-extension)
9. [Step 8: Understand the AI Code Assistant](#step-8-understand-the-ai-code-assistant)
10. [Step 9: Implement BB84 Protocol](#step-9-implement-bb84-protocol)
11. [Step 10: Visualize BB84 Implementation](#step-10-visualize-bb84-implementation)
12. [Step 11: Switch to B92 Protocol](#step-11-switch-to-b92-protocol)
13. [Step 12: Implement B92 Protocol](#step-12-implement-b92-protocol)
14. [Step 13: Visualize B92 Implementation](#step-13-visualize-b92-implementation)
15. [Understanding Tracking](#understanding-tracking)
16. [Troubleshooting](#troubleshooting)
17. [Quick Reference](#quick-reference)

---

## Prerequisites

Before starting, ensure you have:

- A computer running Windows, macOS, or Linux
- Administrator/sudo privileges (to install software)
- Internet connection (for Firebase tracking and AI features)
- At least 8 GB RAM and 15 GB free disk space

---

## Step 1: Clone the Repository

### Open Terminal or Command Prompt

**Windows:**
- Press `Win + R`, type `cmd`, press Enter
- Or search for "Command Prompt" in Start menu

**macOS:**
- Press `Cmd + Space`, type "Terminal", press Enter

**Linux:**
- Press `Ctrl + Alt + T`
- Or search for "Terminal" in applications

### Clone the Repository

In your terminal, run:

```bash
git clone https://github.com/prateek780/qsimnotebookfinal
cd qsimnotebookfinal
```

**What this does:**
- Downloads all project files to your computer
- Creates a folder called `qsimnotebookfinal`
- Changes directory into the project folder

**If git is not installed:**
- Windows: Download and install from https://git-scm.com/
- macOS: Run `xcode-select --install` in Terminal
- Linux: Run `sudo apt install git` (Ubuntu/Debian) or `sudo yum install git` (Fedora/CentOS)

---

## Step 2: Run the Auto-Installer

The auto-installer will download and install all required software:
- Python 3.9+ (Python 3.13 on Windows/Mac, 3.11+ on Linux)
- Node.js 18+ (version 24.x LTS)
- Docker Desktop
- JupyterLab with all quantum computing libraries
- edu_agents AI extension

### Windows

In the same Command Prompt window (inside `qsimnotebookfinal` folder):

```cmd
install.bat
```

Or with PowerShell:

```powershell
.\install.ps1
```

### macOS

In Terminal:

```bash
chmod +x install_mac.sh
./install_mac.sh
```

**Note:** The installer will use Homebrew. If Homebrew is not installed, the script will install it for you.

### Linux

In Terminal:

```bash
chmod +x install_linux.sh
./install_linux.sh
```

**Supported distributions:** Ubuntu, Debian, Fedora, CentOS, Arch Linux, Manjaro

### What Happens During Installation

The installer will:

1. Check if Python is installed (install if missing)
2. Check if Node.js is installed (install if missing)
3. Check if Docker is installed (install if missing)
4. Install Python packages from `quantum_requirements.txt`
5. Navigate to `.plugins/edu_agent_plugin` folder
6. Install Node.js dependencies with `npm install`
7. Install Python package with `pip install -e .`
8. Install `faiss-cpu` (AI vector database)
9. Build JupyterLab extension with `jupyter labextension build .`
10. Enable server extension with `jupyter server extension enable edu_agents`
11. Verify all installations

**Installation time:** 15-25 minutes (depending on your internet speed and system)

### After Installation Completes

You should see messages indicating successful installation:

```
Python 3.13 installed successfully
Node.js 24.x installed successfully
Docker Desktop installed successfully
All Python dependencies installed
edu_agents extension built successfully
Extension enabled in JupyterLab
Installation complete!
```

**Linux users:** Log out and log back in for docker group changes to take effect.

---

## Step 3: Start Docker Desktop

### Windows and macOS

1. Find "Docker Desktop" in your applications
2. Double-click to launch it
3. Wait for Docker to start (Docker icon in system tray will stop animating)
4. You should see "Docker Desktop is running" notification

### Linux

Docker Engine starts automatically after installation. Verify it's running:

```bash
sudo systemctl status docker
```

You should see "active (running)" in green.

If not running:

```bash
sudo systemctl start docker
```

### Verify Docker is Running

In your terminal, run:

```bash
docker --version
docker ps
```

You should see:
- Docker version information
- A list of running containers (may be empty)

**Important:** Docker must be running before proceeding to the next step.

---

## Step 4: Launch JupyterLab with Docker

Now that Docker is running, you'll start JupyterLab in a Docker container. This ensures all dependencies are correctly configured and isolated.

### Start JupyterLab Container

In your terminal (make sure you're in the `qsimnotebookfinal` folder):

```bash
docker-compose -f docker-compose.jupyter.yaml up --build
```

**What this command does:**
- `-f docker-compose.jupyter.yaml` uses the JupyterLab-specific configuration
- `up` starts the container
- `--build` rebuilds the image with latest changes

### Wait for Startup

The first time you run this, it will:
1. Download Python base image (~500 MB)
2. Download Node.js (~100 MB)
3. Install all Python packages
4. Install Node.js dependencies
5. Build the edu_agents extension
6. Start JupyterLab

**First build time:** 5-10 minutes

**Look for this message:**
```
jupyter-lab-quantum  | [I 2024-10-29 12:00:00.000 ServerApp] Jupyter Server is running at:
jupyter-lab-quantum  | [I 2024-10-29 12:00:00.000 ServerApp] http://localhost:8888/lab
```

### Access JupyterLab

Open your web browser and go to:

```
http://localhost:8888
```

You should see the JupyterLab interface with:
- File browser on the left showing project files
- Main work area in the center
- No password required

**If port 8888 is already in use:**
- Edit `docker-compose.jupyter.yaml`
- Change `"8888:8888"` to `"9999:8888"` (or any free port)
- Access at `http://localhost:9999`

### Stopping JupyterLab

When you're done working:

1. Go back to your terminal
2. Press `Ctrl + C` twice
3. Wait for container to stop

Or run in a new terminal:

```bash
docker-compose -f docker-compose.jupyter.yaml down
```

### Restarting JupyterLab (Subsequent Times)

After the first build, starting JupyterLab is much faster (~10 seconds):

```bash
docker-compose -f docker-compose.jupyter.yaml up
```

Remove `--build` flag since everything is already built.

---

## Step 5: Open the Notebook

With JupyterLab running in your browser:

1. Look at the **left sidebar** (File Browser)
2. Locate the file named `qsimnotebook.ipynb`
3. **Double-click** the file to open it

The notebook will open in the main area showing:
- Multiple cells with instructions and code
- Markdown cells with explanations
- Code cells (with gray backgrounds)
- A toolbar at the top

### Notebook Structure

The notebook is organized as follows:

| Section | Cell Numbers | Content |
|---------|--------------|---------|
| Tracking Setup | Cell 1 | Initialize Firebase tracking with your student ID |
| Magic Extension | Cell 2 | Load vibe_magic for auto-save and tracking |
| BB84 Methods | Cells 3-7 | Implement 5 BB84 methods (constructor + 4 protocol methods) |
| B92 Methods | Cells 8-12 | Implement 5 B92 methods (constructor + 4 protocol methods) |
| Visualization | Last cell | Run simulation to see your implementation |

---

## Step 6: Initialize Student Tracking

**CRITICAL: Do this BEFORE implementing any code!**

### Find Cell 1

Scroll to the very first code cell in the notebook. It should be labeled:

```
STUDENT ACTIVITY TRACKING SETUP
```

### Run the Cell

1. Click inside the cell to select it
2. Press `Shift + Enter` to run
3. Or click the "Run" button (play icon) in the toolbar

### Enter Your Student ID

You'll be prompted:

```
Enter your Student ID: _
```

Type your student ID (provided by your instructor) and press Enter.

### Verify Tracking Initialized

You should see output like this:

```
Step 1/3: Initializing Firebase connection...
Firebase connected: qsimnotebookfinal

Step 2/3: Setting up student record (your_student_id)...
  > Student record ready

Step 3/3: Creating session...
SUCCESS: Firebase fully connected - Session ID: 20241029_123456

Tracking initialized for your_student_id (Session: 20241029_123456)
AI agent interactions will now be tracked in Firebase

TRACKING STARTED FOR STUDENT: your_student_id
```

### What This Does

- Creates your student record in Firebase cloud database
- Starts a new session with unique timestamp
- Enables automatic code tracking
- Enables AI interaction tracking
- Starts background file watcher (checks every 3 seconds)

**Important:** All your subsequent work will be automatically linked to this student ID and session.

---

## Step 7: Load the Magic Extension

The `%%vibe_code` magic extension enables automatic code saving and tracking.

### Find Cell 2

Locate the cell containing:

```python
# Load vibe_magic extension
import vibe_magic
from IPython import get_ipython
ipython = get_ipython()
vibe_magic.load_ipython_extension(ipython)
print("✅ Vibe Code Magic: Loaded")
```

### Run the Cell

1. Click inside the cell
2. Press `Shift + Enter`

### Verify Magic Loaded

You should see:

```
✅ Vibe Code Magic: Loaded
```

### What This Enables

The `%%vibe_code` magic allows you to:
- Write code in a cell starting with `%%vibe_code`
- Automatically save to the correct file (`student_bb84_impl.py` or `student_b92_impl.py`)
- Automatically track in Firebase
- Validate syntax before execution
- All in one step!

**Important:** You must load this extension BEFORE using any `%%vibe_code` cells.

---

## Step 8: Understand the AI Code Assistant

The `edu_agents` extension provides an AI assistant integrated into JupyterLab.

### Locate the Assistant

Look at the **left sidebar** of JupyterLab. You should see several icons:
- Folder icon (File Browser)
- Running terminals icon
- Command palette icon
- **edu_agents icon** (puzzle or chat icon)

Click the **edu_agents icon** to open the AI assistant panel.

### AI Assistant Panel

The panel shows:
- **Title:** "QKD Code Assistant" or "edu_agents"
- **Chat history:** Previous questions and answers
- **Input box:** At the bottom with placeholder text
- **Send button:** To submit your question

### What the AI Can Do

| Task | Example Prompt |
|------|----------------|
| Generate code | `write the __init__ method for BB84` followed by skeleton function |
| Explain concepts | `explain how BB84 basis reconciliation works` |
| Debug issues | `why is my error rate higher than expected?` |
| Analyze logs | `what was my error rate in the last simulation?` |
| Provide hints | `give me a hint for implementing bb84_send_qubits` |

### AI Tracking

**Everything is logged:**
- Your full question (every line stored separately)
- AI's full response (every line stored separately)
- Request type (CODE or EXPLANATION)
- Protocol (BB84 or B92)
- Number of lines generated
- Timestamp

Your instructor can see:
- How you used the AI assistant
- What questions you asked
- What code the AI generated
- Whether you understood the AI's responses

**This is part of your assessment** - it shows your learning process, not just final code.

---

## Step 9: Implement BB84 Protocol

You will implement 5 methods for the BB84 protocol:

1. `__init__` - Constructor (initialize instance variables)
2. `bb84_send_qubits` - Alice prepares and sends qubits
3. `process_received_qbit` - Bob receives and measures qubits
4. `bb84_reconcile_bases` - Alice and Bob compare measurement bases
5. `bb84_estimate_error_rate` - Calculate error rate to detect eavesdropping

### Method Implementation Workflow

For EACH method, follow these steps:

#### Step 9.1: Read the Cell Instructions

Each method has a dedicated cell with:
- **Detailed prompt** explaining what the method should do
- **Skeleton function** showing the method signature
- **Expected behavior** description
- **Example usage** (sometimes)

Read this carefully before asking the AI for help.

#### Step 9.2: Ask the AI Assistant

1. **Copy the prompt and skeleton** from the notebook cell
2. **Open the edu_agents panel** (left sidebar)
3. **Paste into the input box** at the bottom
4. **Press Enter** or click Send

**Example for `__init__` method:**

```
Create a constructor that accepts a name parameter.
Store it as instance variable. Initialize 5 empty lists:
random_bits, measurement_bases, quantum_states, 
received_bases, measurement_outcomes.
Print confirmation message.

def __init__(self, name):
```

#### Step 9.3: Review AI-Generated Code

The AI will respond with code. **Review it carefully:**
- Does it match the requirements?
- Do you understand what each line does?
- Are there any syntax errors?
- Does it use the correct variable names?

**Do NOT blindly copy code without understanding it.**

#### Step 9.4: Use the %%vibe_code Cell

Find the `%%vibe_code` cell for this method. It looks like:

```python
%%vibe_code
# Your code will go here
```

**CRITICAL RULES:**
- `%%vibe_code` MUST be the FIRST line (nothing before it)
- No comments or code above `%%vibe_code`
- Comments go AFTER `%%vibe_code`, not before

**Correct format:**

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

**Incorrect format (DO NOT DO THIS):**

```python
# coding: utf-8
%%vibe_code    # WRONG - nothing should come before %%vibe_code
```

#### Step 9.5: Run the Cell

1. Click inside the cell
2. Press `Shift + Enter` to execute

### What Happens When You Run %%vibe_code

You'll see output like this:

```
VIBE CODE: Automatic Save & Track
============================================================
[1/4] Checking tracker...
Student ID: your_student_id
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

**What this did:**
1. Validated your Python syntax
2. Executed your code
3. Saved to `student_bb84_impl.py` file
4. Uploaded snapshot to Firebase with timestamp
5. Detected which methods were added/modified
6. Recorded line counts and file size

### BB84 Methods Details

#### Method 1: Constructor (`__init__`)

**Purpose:** Initialize the quantum host with a name and empty lists for storing protocol data.

**Key Requirements:**
- Accept `name` parameter
- Store as `self.name`
- Initialize 5 empty lists:
  - `self.random_bits` - stores random 0s and 1s
  - `self.measurement_bases` - stores basis choices (rectilinear or diagonal)
  - `self.quantum_states` - stores encoded quantum states
  - `self.received_bases` - stores Bob's basis choices
  - `self.measurement_outcomes` - stores measurement results
- Print confirmation message

**Critical:** Use `__init__` with DOUBLE underscores before and after, not single underscores.

#### Method 2: Send Qubits (`bb84_send_qubits`)

**Purpose:** Alice generates random bits and bases, encodes qubits, and sends them to Bob.

**Key Steps:**
1. Generate `num_qubits` random bits (0 or 1)
2. Generate random bases for each bit (rectilinear or diagonal)
3. Encode each bit as a quantum state based on the basis
4. Store bits and bases for later comparison
5. Return list of encoded qubits

**Encoding Rules:**
- Rectilinear basis: 0 → |0⟩, 1 → |1⟩
- Diagonal basis: 0 → |+⟩, 1 → |-⟩

#### Method 3: Process Received Qubit (`process_received_qbit`)

**Purpose:** Bob receives a qubit and measures it in a randomly chosen basis.

**Key Steps:**
1. Receive qubit from quantum channel
2. Choose random measurement basis (rectilinear or diagonal)
3. Measure qubit in chosen basis
4. Store measurement basis and outcome
5. Return success status

#### Method 4: Reconcile Bases (`bb84_reconcile_bases`)

**Purpose:** Alice and Bob publicly compare their basis choices and keep only matching ones.

**Key Steps:**
1. Compare Alice's preparation bases with Bob's measurement bases
2. Find positions where bases match
3. Keep only the bits where bases matched
4. Discard all others (even if measurement was correct)
5. Return list of matching positions and sifted key

#### Method 5: Estimate Error Rate (`bb84_estimate_error_rate`)

**Purpose:** Calculate error rate from a sample to detect eavesdropping.

**Key Steps:**
1. Select sample positions from sifted key
2. Compare Alice's original bits with Bob's measurements at those positions
3. Count mismatches
4. Calculate error rate = mismatches / sample_size
5. Return error rate as percentage

**Security threshold:** If error rate > 11%, eavesdropping is suspected.

### Repeat for All 5 Methods

Follow Steps 9.1 through 9.5 for each of the 5 BB84 methods. Take your time and understand each implementation before moving to the next.

---

## Step 10: Visualize BB84 Implementation

After implementing all 5 BB84 methods, you can see your implementation in action.

### Find the Visualization Cell

Scroll to the **last cell** in the notebook. It should contain code like:

```python
# Run QKD Simulation
from quantum_network import run_simulation
run_simulation()
```

### Run the Cell

1. Click inside the cell
2. Press `Shift + Enter`

### What You'll See

The simulation will:
1. Create Alice and Bob using your `StudentQuantumHost` class
2. Call `bb84_send_qubits` to generate qubits
3. Transmit qubits through quantum channel
4. Call `process_received_qbit` for Bob to measure
5. Call `bb84_reconcile_bases` to compare bases
6. Call `bb84_estimate_error_rate` to check security
7. Display results and statistics

**Output includes:**
- Number of qubits sent
- Number of bases matched
- Sifted key length
- Error rate percentage
- Final shared key (if error rate is acceptable)

### Check Simulation Logs

All simulation runs are saved to `simulation_logs/` folder:

```
qsimnotebookfinal/
└── simulation_logs/
    ├── simulation_log_Untitled_Topology_20241029_120000.txt
    ├── simulation_log_Untitled_Topology_20241029_123000.txt
    └── ...
```

**Log file contents:**
- Protocol type (BB84)
- Simulation start timestamp
- Qubit generation details
- Basis choices for each qubit
- Measurement outcomes
- Basis reconciliation results
- Error rate calculations
- Final key generation statistics

### Analyze Results with AI

Open the **edu_agents panel** and ask:

```
What was my error rate in the last BB84 simulation?
```

```
How many bases matched in my last run?
```

```
Why is my error rate higher than expected?
```

The AI will read your simulation logs and provide analysis.

---

## Step 11: Switch to B92 Protocol

Before implementing B92, you need to switch the active protocol.

### Open Terminal in Docker Container

You have two options:

**Option A: Use a new terminal on your host machine**

In a new terminal window (NOT the one running docker-compose):

```bash
cd qsimnotebookfinal
docker exec -it jupyter-lab-quantum /bin/bash
```

This gives you a bash shell inside the container.

**Option B: Use JupyterLab's terminal**

In JupyterLab:
1. Click "File" menu → "New" → "Terminal"
2. A terminal opens in JupyterLab

### Run the Switch Command

In the terminal (inside container or JupyterLab terminal):

```bash
python switch_to_b92.py
```

**Output:**

```
Switched to B92 protocol
Updated configuration files
Ready to implement B92 methods
```

### What This Does

- Updates protocol configuration
- Changes active implementation file detection
- Prepares system to track B92 code instead of BB84

---

## Step 12: Implement B92 Protocol

The B92 protocol is similar to BB84 but uses only 2 quantum states instead of 4.

You will implement 5 methods:

1. `__init__` - Constructor
2. `b92_send_qubits` - Alice prepares qubits
3. `b92_process_received_qbit` - Bob measures qubits
4. `b92_sifting` - Filter out inconclusive measurements
5. `b92_estimate_error_rate` - Calculate error rate

### Implementation Workflow

Follow the SAME workflow as BB84:

1. Read cell instructions
2. Ask AI assistant (copy prompt + skeleton to edu_agents panel)
3. Review generated code
4. Paste into `%%vibe_code` cell
5. Run cell (automatic save + track)

### B92 Key Differences from BB84

| Aspect | BB84 | B92 |
|--------|------|-----|
| States used | 4 states (&#124;0⟩, &#124;1⟩, &#124;+⟩, &#124;-⟩) | 2 states (&#124;0⟩, &#124;+⟩) |
| Encoding | Bit 0 or 1 determines state | Only &#124;0⟩ for bit 0, &#124;+⟩ for bit 1 |
| Bases | Alice chooses basis | Alice uses fixed states |
| Measurement | Bob measures in matching basis | Bob measures in random basis |
| Sifting | Keep only matching bases | Keep only conclusive results (outcome = 1) |
| Efficiency | ~50% key retention | ~25% key retention |

### B92 Methods Details

#### Method 1: Constructor (`__init__`)

**Same as BB84 but with B92-specific variable names:**
- `self.sent_bits` - bits Alice sent
- `self.prepared_qubits` - qubits Alice prepared
- `self.received_measurements` - Bob's measurement results
- `self.sifted_key` - key after sifting
- `self.random_bits` - Bob's random bits for measurement
- `self.measurement_outcomes` - Bob's outcomes
- `self.received_bases` - Bob's basis choices

#### Method 2: Send Qubits (`b92_send_qubits`)

**Purpose:** Alice generates random bits and encodes them as |0⟩ or |+⟩ only.

**Encoding Rules:**
- Bit 0 → |0⟩ state
- Bit 1 → |+⟩ state

**No basis choice** - the bit value determines the state directly.

#### Method 3: Process Received Qubit (`b92_process_received_qbit`)

**Purpose:** Bob measures in a random basis and records the result.

**Key Points:**
- Bob chooses Z (rectilinear) or X (diagonal) basis randomly
- Measures the qubit
- Records both the basis and outcome
- Does NOT know if measurement is conclusive yet

#### Method 4: Sifting (`b92_sifting`)

**Purpose:** Keep only measurements where Bob got outcome = 1 (conclusive results).

**Logic:**
- If Bob measures |0⟩ in Z basis and gets 0 → inconclusive (discard)
- If Bob measures |0⟩ in Z basis and gets 1 → impossible (discard)
- If Bob measures |0⟩ in X basis and gets 1 → conclusive! Alice sent 0
- If Bob measures |+⟩ in Z basis and gets 1 → conclusive! Alice sent 1
- Only keep positions where outcome = 1

This is the key difference from BB84 - B92 uses measurement outcomes, not basis matching.

#### Method 5: Estimate Error Rate (`b92_estimate_error_rate`)

**Same concept as BB84:**
- Sample some positions from sifted key
- Compare with Alice's original bits
- Calculate error rate
- Return percentage

### Repeat for All 5 Methods

Follow the same workflow as BB84 for each B92 method.

---

## Step 13: Visualize B92 Implementation

After implementing all 5 B92 methods, visualize your implementation.

### Run the Last Cell

Scroll to the **last cell** and run it:

1. Click inside the cell
2. Press `Shift + Enter`

### What You'll See

The simulation runs your B92 implementation:
1. Alice generates random bits
2. Alice encodes as |0⟩ or |+⟩ qubits
3. Bob measures in random basis
4. Sifting keeps only conclusive measurements
5. Error rate calculated
6. Final key generated (if secure)

**Key difference from BB84:**
- Lower efficiency (~25% instead of ~50%)
- No public basis comparison
- Sifting based on measurement outcomes

### Check Simulation Logs

Same as BB84, logs are in `simulation_logs/`:

```
simulation_log_Untitled_Topology_20241029_150000.txt
```

**Log shows:**
- Protocol: B92
- Prepared states (|0⟩ or |+⟩)
- Bob's random basis choices
- Measurement outcomes
- Sifting results (which measurements were conclusive)
- Error rate
- Final key

### Compare BB84 vs B92

Ask the AI assistant:

```
Compare my BB84 and B92 simulation results
```

```
Which protocol was more efficient?
```

```
What was the difference in error rates?
```

---

## Understanding Tracking

### What Gets Tracked Automatically

#### Code Activity

Every time you run a `%%vibe_code` cell:

| Data | Description |
|------|-------------|
| Full code snapshot | Complete code with all methods |
| Timestamp | Exact date and time you ran the cell |
| Protocol | BB84 or B92 detected automatically |
| Methods detected | Which methods are in the code |
| Lines added | New lines compared to previous version |
| Lines removed | Deleted lines compared to previous version |
| Total lines | Current total line count |
| File size | Characters in file |

#### AI Interactions

Every time you ask the AI assistant:

| Data | Description |
|------|-------------|
| Query text | Your full question |
| Query lines | Each line of your question (stored as array) |
| Response text | AI's full answer |
| Response lines | Each line of AI's response (stored as array) |
| Request type | CODE or EXPLANATION |
| Protocol | BB84 or B92 (detected from context) |
| Lines generated | Number of code lines in AI response |
| Timestamp | When you asked |

### Firebase Data Structure

Your data in Firebase is organized as:

```
firebase/
└── students/
    └── your_student_id/
        ├── sessions/
        │   └── 20241029_123456/
        │       ├── protocol: "BB84"
        │       ├── start_time: "2024-10-29T12:34:56"
        │       └── status: "active"
        ├── code_activity/
        │   └── BB84/
        │       ├── snapshot_1/
        │       │   ├── timestamp: "2024-10-29T12:40:00"
        │       │   ├── code: "class StudentQuantumHost..."
        │       │   ├── lines: 45
        │       │   └── methods: ["__init__", "bb84_send_qubits"]
        │       ├── snapshot_2/
        │       └── ...
        └── ai_interactions/
            ├── interaction_1/
            │   ├── timestamp: "2024-10-29T12:38:00"
            │   ├── query: "write the __init__ method..."
            │   ├── response: "def __init__(self, name)..."
            │   ├── type: "CODE"
            │   └── protocol: "BB84"
            ├── interaction_2/
            └── ...
```

### What Your Instructor Sees

Your instructor has access to:

1. **All code versions** with timestamps
2. **Method-by-method evolution** (how each method changed over time)
3. **Time spent** on each method (calculated from timestamps)
4. **All AI questions** you asked
5. **All AI responses** you received
6. **Whether you modified AI code** (by comparing AI response to your final code)
7. **Simulation results** (from logs)

### Why This Matters

Traditional assessment only sees final code. This lab sees:
- Your learning process
- How you used AI assistance
- Whether you understood the AI's responses
- How many attempts it took to get working code
- Which concepts you struggled with

**This is a LEARNING assessment, not just a CODE assessment.**

---

## Troubleshooting

### Issue 1: Docker Container Won't Start

**Symptoms:**
```
Error: port 8888 already in use
Error: container name already exists
```

**Solution 1 - Port Conflict:**

Edit `docker-compose.jupyter.yaml`:

```yaml
ports:
  - "9999:8888"  # Change 9999 to any free port
```

Then access at `http://localhost:9999`

**Solution 2 - Container Exists:**

```bash
docker rm -f jupyter-lab-quantum
docker-compose -f docker-compose.jupyter.yaml up --build
```

**Solution 3 - Clean Everything:**

```bash
docker-compose -f docker-compose.jupyter.yaml down
docker system prune -a
docker-compose -f docker-compose.jupyter.yaml up --build
```

---

### Issue 2: %%vibe_code Magic Not Found

**Symptoms:**
```
UsageError: Cell magic %%vibe_code not found
```

**Cause:** Magic extension not loaded.

**Solution:**

1. Find Cell 2 (vibe_magic loader)
2. Run it again
3. Then try your `%%vibe_code` cell

**Verify magic is loaded:**

```python
from IPython import get_ipython
ipython = get_ipython()
print('vibe_code' in ipython.magics_manager.magics['cell'])
```

Should print `True`.

---

### Issue 3: Constructor Not Working

**Symptoms:**
```
TypeError: StudentQuantumHost() takes no arguments
TypeError: __init__() missing 1 required positional argument: 'name'
```

**Cause:** Constructor name is wrong.

**Wrong:**
```python
def _init_(self, name):     # Single underscores
def __init(self, name):     # Missing trailing underscores
def init__(self, name):     # Missing leading underscores
```

**Correct:**
```python
def __init__(self, name):   # DOUBLE underscores before AND after
```

**Solution:** Fix the method name and re-run the `%%vibe_code` cell.

---

### Issue 4: edu_agents Panel Not Visible

**Symptoms:**
- No AI assistant icon in left sidebar
- Can't find QKD Code Assistant

**Solution 1 - Check Left Sidebar:**

Look for icons in the left sidebar. Click the **edu_agents icon** (may look like puzzle piece or chat icon).

**Solution 2 - Verify Extension Installed:**

In JupyterLab terminal or your host terminal:

```bash
jupyter labextension list
```

Should show:
```
edu_agents v0.1.0 enabled ok
```

If not listed:

```bash
cd .plugins/edu_agent_plugin
npm install
pip install -e .
jupyter labextension build .
jupyter server extension enable edu_agents
```

Then restart JupyterLab.

**Solution 3 - Clear Cache:**

```bash
jupyter lab clean
jupyter lab build
```

Restart Docker container:

```bash
docker-compose -f docker-compose.jupyter.yaml restart
```

---

### Issue 5: Tracking Not Initializing

**Symptoms:**
```
Tracker not initialized
No student ID found
Firebase connection failed
```

**Solution:**

1. Make sure you ran Cell 1 (STUDENT ACTIVITY TRACKING SETUP)
2. Entered your student ID when prompted
3. Saw "SUCCESS: Firebase fully connected" message

If you missed this:
1. Scroll to Cell 1
2. Click inside the cell
3. Run it with `Shift + Enter`
4. Enter student ID

**Verify tracking is active:**

```python
import notebook_tracker
print(f"Student: {notebook_tracker.STUDENT_ID}")
print(f"Session: {notebook_tracker.SESSION_ID}")
```

Should print your student ID and session ID.

---

### Issue 6: File Not Saved

**Symptoms:**
```
Error: student_bb84_impl.py not found
Error: student_b92_impl.py not found
```

**Cause:** `%%vibe_code` cell didn't run successfully, or you're using wrong protocol.

**Solution:**

1. Make sure `%%vibe_code` is THE FIRST LINE
2. Check for syntax errors in your code
3. Run the cell again
4. Check the output for "SUCCESS: Code executed, saved, and tracked"

**Verify file exists:**

In JupyterLab, check left sidebar file browser:
- You should see `student_bb84_impl.py` (after BB84 implementation)
- You should see `student_b92_impl.py` (after B92 implementation)

---

### Issue 7: Protocol Switch Didn't Work

**Symptoms:**
- Ran `python switch_to_b92.py` but still tracking BB84
- Visualization shows wrong protocol

**Solution:**

**In JupyterLab terminal:**

```bash
python switch_to_b92.py
```

**Or in Docker container terminal:**

```bash
docker exec -it jupyter-lab-quantum python switch_to_b92.py
```

**Verify current protocol:**

```python
from protocol_detection_utils import detect_active_protocol
print(detect_active_protocol())
```

Should print `B92` after switching.

---

### Issue 8: Docker Build Takes Forever

**Symptoms:**
- `docker-compose up --build` stuck for > 20 minutes
- Downloads appear to hang

**Solution:**

1. **Check internet connection** - Docker downloads ~1-2 GB on first build
2. **Check Docker has enough resources:**
   - Open Docker Desktop → Settings → Resources
   - RAM: Set to at least 4 GB (8 GB recommended)
   - Disk: Ensure at least 15 GB free space
3. **Try without cache:**

```bash
docker-compose -f docker-compose.jupyter.yaml build --no-cache
docker-compose -f docker-compose.jupyter.yaml up
```

4. **Check Docker logs:**

```bash
docker-compose -f docker-compose.jupyter.yaml logs -f
```

---

### Issue 9: AI Assistant Not Responding

**Symptoms:**
- Type question in edu_agents panel
- No response appears
- Hangs or shows error

**Solution:**

1. **Check internet connection** - AI features require cloud access
2. **Check Firebase connection** - Make sure tracking initialized (Cell 1)
3. **Try a simple question first:**

```
Hello
```

If no response:

4. **Check browser console** for errors:
   - Press F12 in browser
   - Go to "Console" tab
   - Look for errors related to edu_agents

5. **Restart JupyterLab:**

```bash
docker-compose -f docker-compose.jupyter.yaml restart
```

---

## Quick Reference

### Complete Step-by-Step Checklist

| Step | Task | Status |
|------|------|--------|
| 1 | Open terminal/command prompt | ☐ |
| 2 | Clone repository: `git clone https://github.com/prateek780/qsimnotebookfinal` | ☐ |
| 3 | Navigate to folder: `cd qsimnotebookfinal` | ☐ |
| 4 | Run installer: `install.bat` (Windows) or `./install_mac.sh` (Mac) or `./install_linux.sh` (Linux) | ☐ |
| 5 | Wait for installation to complete (15-25 minutes) | ☐ |
| 6 | Open Docker Desktop application | ☐ |
| 7 | Wait for Docker to start | ☐ |
| 8 | Start JupyterLab: `docker-compose -f docker-compose.jupyter.yaml up --build` | ☐ |
| 9 | Wait for "Jupyter Server is running at: http://localhost:8888" message | ☐ |
| 10 | Open browser: `http://localhost:8888` | ☐ |
| 11 | Double-click `qsimnotebook.ipynb` in file browser | ☐ |
| 12 | Run Cell 1 (tracking setup), enter student ID | ☐ |
| 13 | Run Cell 2 (load vibe_magic) | ☐ |
| 14 | Click edu_agents icon in left sidebar to open AI assistant | ☐ |
| 15 | Implement BB84 method 1 (`__init__`) using AI + `%%vibe_code` | ☐ |
| 16 | Implement BB84 method 2 (`bb84_send_qubits`) | ☐ |
| 17 | Implement BB84 method 3 (`process_received_qbit`) | ☐ |
| 18 | Implement BB84 method 4 (`bb84_reconcile_bases`) | ☐ |
| 19 | Implement BB84 method 5 (`bb84_estimate_error_rate`) | ☐ |
| 20 | Run last cell to visualize BB84 | ☐ |
| 21 | Check `simulation_logs/` folder for BB84 logs | ☐ |
| 22 | Run `python switch_to_b92.py` in terminal | ☐ |
| 23 | Implement B92 method 1 (`__init__`) | ☐ |
| 24 | Implement B92 method 2 (`b92_send_qubits`) | ☐ |
| 25 | Implement B92 method 3 (`b92_process_received_qbit`) | ☐ |
| 26 | Implement B92 method 4 (`b92_sifting`) | ☐ |
| 27 | Implement B92 method 5 (`b92_estimate_error_rate`) | ☐ |
| 28 | Run last cell to visualize B92 | ☐ |
| 29 | Check `simulation_logs/` folder for B92 logs | ☐ |
| 30 | Review all code and logs - you're done! | ☐ |

---

### Essential Commands

#### Terminal Commands

```bash
# Clone repository
git clone https://github.com/prateek780/qsimnotebookfinal
cd qsimnotebookfinal

# Run installer (Windows)
install.bat

# Run installer (Mac)
chmod +x install_mac.sh
./install_mac.sh

# Run installer (Linux)
chmod +x install_linux.sh
./install_linux.sh

# Start JupyterLab with Docker (first time - includes build)
docker-compose -f docker-compose.jupyter.yaml up --build

# Start JupyterLab with Docker (subsequent times)
docker-compose -f docker-compose.jupyter.yaml up

# Stop JupyterLab
docker-compose -f docker-compose.jupyter.yaml down

# Restart JupyterLab
docker-compose -f docker-compose.jupyter.yaml restart

# View logs
docker-compose -f docker-compose.jupyter.yaml logs -f

# Switch protocols
python switch_to_bb84.py
python switch_to_b92.py

# Check Docker is running
docker ps

# Remove container and rebuild
docker rm -f jupyter-lab-quantum
docker-compose -f docker-compose.jupyter.yaml up --build
```

#### JupyterLab Shortcuts

| Action | Shortcut |
|--------|----------|
| Run cell | `Shift + Enter` |
| Run cell and insert below | `Alt + Enter` |
| Add cell above | `A` (in command mode) |
| Add cell below | `B` (in command mode) |
| Delete cell | `D D` (press D twice in command mode) |
| Enter command mode | `Esc` |
| Enter edit mode | `Enter` |
| Save notebook | `Ctrl + S` (or `Cmd + S` on Mac) |
| Restart kernel | `0 0` (press 0 twice in command mode) |

---

### Key Files and Folders

| Path | Description |
|------|-------------|
| `qsimnotebook.ipynb` | Main notebook with all instructions and cells |
| `student_bb84_impl.py` | Your BB84 implementation (auto-saved) |
| `student_b92_impl.py` | Your B92 implementation (auto-saved) |
| `simulation_logs/` | Folder containing all simulation logs |
| `vibe_magic.py` | Magic extension for auto-save and tracking |
| `.plugins/edu_agent_plugin/` | AI assistant extension source code |
| `docker-compose.jupyter.yaml` | Docker configuration for JupyterLab |
| `quantum_requirements.txt` | Python dependencies list |

---

### Support Resources

| Resource | Location |
|----------|----------|
| GitHub Repository | https://github.com/prateek780/qsimnotebookfinal |
| Installation Guide | `INSTALLATION_GUIDE.md` in repository |
| Installer Summary | `INSTALLER_SUMMARY.md` in repository |
| Docker Configuration | `docker-compose.jupyter.yaml` |

---

## Summary

You have completed the setup and implementation guide for the Quantum Key Distribution lab.

**What you accomplished:**

1. Installed all required software (Python, Node.js, Docker, JupyterLab, AI extension)
2. Started JupyterLab in a Docker container
3. Initialized Firebase tracking with your student ID
4. Learned how to use the edu_agents AI assistant
5. Implemented 5 BB84 protocol methods
6. Visualized BB84 implementation and analyzed results
7. Switched to B92 protocol
8. Implemented 5 B92 protocol methods
9. Visualized B92 implementation and compared with BB84

**What was automatically tracked:**

- Every code change with timestamps
- All AI assistant interactions
- Code snapshots for each method
- Time spent on each implementation
- Simulation results from logs

**Your assessment includes:**

- Final working code
- Learning process (how you used AI)
- Understanding (based on code modifications)
- Problem-solving approach (from multiple attempts)
- Protocol comparison insights

**Remember:** This lab values your learning journey, not just the destination. Your instructor can see how you learned, struggled, asked questions, and improved - which is more valuable than just seeing final code.

Good luck with your quantum networking lab!
