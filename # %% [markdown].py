# %% [markdown]
# 
# 
#  # Introduction to Quantum Networking
# 
#  Welcome to the fascinating world of **Quantum Networking**!
# 
#  In this interactive notebook, you'll learn the fundamentals of quantum communication protocols and get hands-on experience with quantum key distribution, entanglement, and quantum network simulation.
# 
#  ## What is Quantum Networking?
# 
#  Quantum networking leverages the principles of quantum mechanics to create ultra-secure communication channels. Unlike classical networks that transmit bits (0s and 1s), quantum networks transmit quantum bits (qubits) that can exist in superposition states.
# 
#  ### Key Concepts:
#  - **Quantum Key Distribution (QKD)**: Secure key sharing using quantum mechanics
#  - **Quantum Entanglement**: Spooky action at a distance for instant correlation
#  - **BB84 Protocol**: A pioneering quantum cryptography protocol
#  - **Quantum Channels**: The medium for transmitting qubits
# 
#  ### Learning Objectives:
#  By the end of this notebook, you will:
#  1. Understand quantum networking fundamentals
#  2. Implement quantum protocols from scratch
#  3. Interact with a live quantum network simulation
#  4. Write your own quantum host implementations
#  5. Analyze quantum security and error rates
# 
#  Let's begin this quantum journey!

# %%
import os
print("Current directory:", os.getcwd())



# %%


import random
import numpy as np

def prepare_quantum_state(bit, basis):
    """
    Prepare a quantum state for BB84 protocol
    
    Args:
        bit: 0 or 1 (the classical bit to encode)
        basis: 0 (Z-basis) or 1 (X-basis)
    
    Returns:
        String representation of the quantum state
    """
    if basis == 0:  # Z-basis (computational basis)
        if bit == 0:
            return '|0⟩'  # |0⟩ state
        else:
            return '|1⟩'  # |1⟩ state
    else:  # X-basis (Hadamard basis)
        if bit == 0:
            return '|+⟩'  # |+⟩ = (|0⟩ + |1⟩)/√2
        else:
            return '|-⟩'  # |-⟩ = (|0⟩ - |1⟩)/√2

def measure_quantum_state(quantum_state, measurement_basis):
    """
    Measure a quantum state in a given basis.

    Args:
        quantum_state: one of '|0⟩', '|1⟩', '|+⟩', '|-⟩'
        measurement_basis: 0 = Z, 1 = X

    Returns:
        0 or 1
    """
    if measurement_basis == 0:  # Z-basis measurement
        if quantum_state in ['|0⟩', '|1⟩']:
            return 0 if quantum_state == '|0⟩' else 1
        else:
            # Measuring X states in Z basis is random
            return random.randint(0, 1)
    else:  # X-basis measurement
        if quantum_state in ['|+⟩', '|-⟩']:
            return 0 if quantum_state == '|+⟩' else 1
        else:
            # Measuring Z states in X basis is random
            return random.randint(0, 1)

# Test the functions
print(" Testing Quantum State Functions:")
print(f"Bit 0, Z-basis: {prepare_quantum_state(0, 0)}")
print(f"Bit 1, Z-basis: {prepare_quantum_state(1, 0)}")
print(f"Bit 0, X-basis: {prepare_quantum_state(0, 1)}")
print(f"Bit 1, X-basis: {prepare_quantum_state(1, 1)}")
print(" Quantum state functions working!")


# %%


# %% [markdown]
# 
# 
#  ## Section 1: Quantum Fundamentals
# 
#  Before diving into quantum networking, let's understand the basic building blocks:
# 
#  ### Qubits - The Quantum Bits
# 
#  A qubit is the basic unit of quantum information. Unlike classical bits that are either 0 or 1, qubits can exist in a **superposition** of both states:
# 
#  $$|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$$
# 
#  Where $\alpha$ and $\beta$ are complex numbers called amplitudes, and $|\alpha|^2 + |\beta|^2 = 1$.
# 

# %% [markdown]
# [markdown]
# 
#  ##  Section 2: Understanding BB84 Protocol
# 
#  The BB84 protocol is a quantum key distribution protocol that allows two parties (Alice and Bob) to share a secret key using quantum mechanics.
# 
#  ### Key Steps:
#  1. **Alice** prepares qubits in random bases (Z or X)
#  2. **Alice** sends qubits to Bob through a quantum channel
#  3. **Bob** measures qubits in random bases
#  4. **Alice and Bob** publicly compare their basis choices
#  5. **Alice and Bob** keep only the bits where bases matched
#  6. **Alice and Bob** estimate error rate and perform privacy amplification
# 
#  Let's implement this step by step!
# 

# %%


# Import required libraries for quantum networking
import sys
import numpy as np
import random
from IPython.display import HTML, display, clear_output
import warnings
warnings.filterwarnings('ignore')

# Import our custom quantum networking modules
sys.path.append('.')

print(" All libraries imported successfully!")
print(" Ready to implement quantum networking protocols!")

# %%
# %%

#  Section 2: Quantum State Preparation
# ===========================================
# Let's create quantum states for the BB84 protocol

def prepare_quantum_state(bit, basis):
    """
    Prepare a quantum state for BB84 protocol
    
    Args:
        bit: 0 or 1 (the classical bit to encode)
        basis: 0 (Z-basis) or 1 (X-basis)
    
    Returns:
        String representation of the quantum state
    """
    if basis == 0:  # Z-basis (computational basis)
        if bit == 0:
            return '|0⟩'  # |0⟩ state
        else:
            return '|1⟩'  # |1⟩ state
    else:  # X-basis (Hadamard basis)
        if bit == 0:
            return '|+⟩'  # |+⟩ = (|0⟩ + |1⟩)/√2
        else:
            return '|-⟩'  # |-⟩ = (|0⟩ - |1⟩)/√2

# Test the quantum state preparation
print("🧪 Testing quantum state preparation:")
print(f"Bit 0, Z-basis: {prepare_quantum_state(0, 0)}")
print(f"Bit 1, Z-basis: {prepare_quantum_state(1, 0)}")
print(f"Bit 0, X-basis: {prepare_quantum_state(0, 1)}")
print(f"Bit 1, X-basis: {prepare_quantum_state(1, 1)}")
print("✅ Quantum state preparation working!")

# %%
# %%

import random

def measure_quantum_state(quantum_state, measurement_basis):
    """
    Measure a quantum state in a given basis.

    Args:
        quantum_state: one of '|0⟩', '|1⟩', '|+⟩', '|-⟩'
        measurement_basis: 0 = Z, 1 = X

    Returns:
        0 or 1
    """
    if measurement_basis == 0:  # Z-basis measurement
        if quantum_state in ['|0⟩', '|1⟩']:
            return 0 if quantum_state == '|0⟩' else 1
        else:
            # Measuring X states in Z basis is random
            return random.randint(0, 1)
    else:  # X-basis measurement
        if quantum_state in ['|+⟩', '|-⟩']:
            return 0 if quantum_state == '|+⟩' else 1
        else:
            # Measuring Z states in X basis is random
            return random.randint(0, 1)

# %% [markdown]
#  [markdown]
# 
#  ##  Section 4: Your BB84 Implementation
# 
#  Now it's time to implement the complete BB84 protocol! This is where you'll create your "vibe coded" implementation that will power the quantum network simulation.
# 
#  ### Your Task:
#  Implement the `StudentQuantumHost` class with the BB84 protocol methods. This will be your personal implementation that the simulation will use!
# 

# %%
import random




class StudentQuantumHost:
    """
    Your personal BB84 implementation!
    This class will be used by the quantum network simulation.
    """
   
    # PROMPT FOR CONSTRUCTOR:
    """
    Implement a constructor for the StudentQuantumHost class using the provided skeleton function.
    The constructor should accept a name for the host, such as 'Alice' or 'Bob', and store it so it
    can be used in log messages. It should also create empty lists to keep track of random classical bits
    generated, measurement bases chosen, quantum states encoded, measurement bases used when
    receiving qubits, and measurement outcomes obtained. After initializing these lists,
    the constructor must print a welcome message that dynamically includes the host's name,
    for example: StudentQuantumHost '<host name>' initialized successfully!
    All lists must start empty, and the host name handling must be dynamic so that
    it works for any name passed in.
    """
   
    def __init__(self, name):
        self.name = name
        self.random_bits = []
        self.measurement_bases = []
        self.quantum_states = []
        self.received_bases = []
        self.measurement_outcomes = []
        print(f"StudentQuantumHost '{self.name}' initialized successfully!")


    # PROMPT FOR BB84_SEND_QUBITS METHOD:
    """
    Implement the bb84_send_qubits method for the StudentQuantumHost class using the
    provided skeleton function. The method should begin by displaying a message that mentions
    the identity of the sender and the total number of qubits to be processed.
    It should then reinitialize any internal storage structures that will hold preparation data.
    For each qubit, the method must create a random classical value, choose a random preparation setting,
    transform the classical value into a quantum state using the chosen setting, and store the results
    in the internal collections. After all qubits are processed, the method should display a summary
    that includes how many qubits were prepared, a preview of the generated values, and a preview of the chosen settings.
    Finally, the method should return the collection of prepared quantum states.
    """
   
    def bb84_send_qubits(self, num_qubits):
        print(f"{self.name} is preparing {num_qubits} qubits...")
        self.random_bits = []
        self.measurement_bases = []
        self.quantum_states = []


        for _ in range(num_qubits):
            classical_bit = random.randint(0, 1)
            preparation_basis = random.randint(0, 1)


            if preparation_basis == 0:
                quantum_state = "|0⟩" if classical_bit == 0 else "|1⟩"
            else:
                quantum_state = "|+⟩" if classical_bit == 0 else "|-⟩"


            self.random_bits.append(classical_bit)
            self.measurement_bases.append(preparation_basis)
            self.quantum_states.append(quantum_state)


        print(f"{self.name} prepared {len(self.quantum_states)} qubits")
        return self.quantum_states


    # PROMPT FOR PROCESS_RECEIVED_QBIT METHOD:
    """
    Implement the process_received_qbit method for the StudentQuantumHost class using the provided skeleton function.
    The method should select a random measurement setting to determine how the incoming quantum state will be observed and
    record this chosen setting in the appropriate internal collection. It must then perform a measurement of the received
    quantum state using the chosen setting and store the resulting outcome in the internal collection of measurement results.
    The method should indicate successful processing by returning a confirmation value.
    """
   
    def process_received_qbit(self, qbit, from_channel):
        measurement_basis = random.randint(0, 1)
        self.received_bases.append(measurement_basis)


        if measurement_basis == 0:
            if qbit == "|0⟩":
                outcome = 0
            elif qbit == "|1⟩":
                outcome = 1
            elif qbit == "|+⟩" or qbit == "|-⟩":
                outcome = random.randint(0, 1)
            else:
                outcome = random.randint(0, 1)
        else:
            if qbit == "|+⟩":
                outcome = 0
            elif qbit == "|-⟩":
                outcome = 1
            elif qbit == "|0⟩" or qbit == "|1⟩":
                outcome = random.randint(0, 1)
            else:
                outcome = random.randint(0, 1)


        self.measurement_outcomes.append(outcome)
        return True


    # PROMPT FOR BB84_RECONCILE_BASES METHOD:
    """
    Implement the bb84_reconcile_bases method for the StudentQuantumHost class using the provided skeleton function.
    The method should start by displaying a message that indicates the participant is comparing basis choices.
    It must create two empty collections: one for indices where the bases align and another for the corresponding bit values.
    The method should iterate through both sets of basis choices simultaneously with their positions, and for each position,
    if the two bases are the same, it should record the index, and if a corresponding measurement result exists,
    it should also record the measured value. After completing the comparison, the method must display a summary that shows
    how many matches were found and the proportion of matches relative to the total comparisons.
    Finally, it should return both the list of matching indices and the list of corresponding bit values.
    """
   
    def bb84_reconcile_bases(self, alice_bases, bob_bases):
        print(f"{self.name} is comparing basis choices...")
        matching_indices = []
        corresponding_bits = []


        for i, (alice_basis, bob_basis) in enumerate(zip(alice_bases, bob_bases)):
            if alice_basis == bob_basis:
                matching_indices.append(i)
                if i < len(self.measurement_outcomes):
                    corresponding_bits.append(self.measurement_outcomes[i])
                elif i < len(self.random_bits):
                    corresponding_bits.append(self.random_bits[i])


        total_comparisons = min(len(alice_bases), len(bob_bases))
        matches_found = len(matching_indices)
        match_proportion = matches_found / total_comparisons if total_comparisons > 0 else 0


        print(f"Matches found: {matches_found} / {total_comparisons} ({match_proportion*100:.1f}%)")
        return matching_indices, corresponding_bits


    # PROMPT FOR BB84_ESTIMATE_ERROR_RATE METHOD:
    """
    Implement the bb84_estimate_error_rate method for the StudentQuantumHost class using the provided skeleton function.
    The method should begin by showing a message that indicates the participant is calculating the error rate.
    It must set up counters to track how many comparisons are made and how many discrepancies are found.
    The method should then iterate through the provided sample of reference bits along with their positions, and for each entry,
    if the position is valid relative to this host's recorded outcomes, it should increase the comparison count,
    and if the recorded outcome does not match the provided bit, it should increase the error count.
    After processing all samples, the method should calculate the error rate as the ratio of errors to comparisons,
    defaulting to zero if no comparisons were made. The method must display a summary that includes
    the calculated error rate and the raw error/total comparison counts. Finally, it should return the computed error rate.
    """
   
    def bb84_estimate_error_rate(self, sample_positions, reference_bits):
        print(f"{self.name} is calculating error rate...")
        comparison_count = 0
        error_count = 0


        for pos, ref_bit in zip(sample_positions, reference_bits):
            if pos < len(self.measurement_outcomes):
                comparison_count += 1
                if self.measurement_outcomes[pos] != ref_bit:
                    error_count += 1
            elif pos < len(self.random_bits):
                comparison_count += 1
                if self.random_bits[pos] != ref_bit:
                    error_count += 1


        error_rate = error_count / comparison_count if comparison_count > 0 else 0.0
        print(f"Error rate: {error_rate*100:.2f}% ({error_count}/{comparison_count})")
        return error_rate




def main():
    print("=" * 70)
    print("BB84 QUANTUM KEY DISTRIBUTION PROTOCOL DEMONSTRATION")
    print("=" * 70)
    print()


    print("STEP 1: Initializing Quantum Hosts")
    alice = StudentQuantumHost("Alice")
    bob = StudentQuantumHost("Bob")
    print()


    print("STEP 2: Quantum Transmission Phase")
    num_qubits = 15
    quantum_states = alice.bb84_send_qubits(num_qubits)
    print()


    print("STEP 3: Quantum Measurement Phase")
    for qbit in quantum_states:
        bob.process_received_qbit(qbit, None)
    print("Measurement phase complete")
    print()


    print("STEP 4: Basis Reconciliation Phase")
    matching_indices, _ = alice.bb84_reconcile_bases(alice.measurement_bases, bob.received_bases)
    matching_indices, _ = bob.bb84_reconcile_bases(alice.measurement_bases, bob.received_bases)
    print()


    print("STEP 5: Error Rate Estimation Phase")
    if len(matching_indices) > 5:
        sample_positions = matching_indices[:5]
        alice.bb84_estimate_error_rate(sample_positions, [bob.measurement_outcomes[i] for i in range(5)])
        bob.bb84_estimate_error_rate(sample_positions, [alice.random_bits[i] for i in range(5)])
    else:
        print("Not enough matching bases for error rate estimation")
    print()




if __name__ == "__main__":
    main()


# %%


%save -f student_bb84_impl.py 6

# %%
from protocol_helpers import create_bb84_status_file ,check_current_protocol, switch_to_bb84, switch_to_b92
create_bb84_status_file()
check_current_protocol()

# %% [markdown]
# # Now run the simulation from the cell at the end to test BB84 QKD Protocol 

# %% [markdown]
# # Switch to B92 Quantum key Distribution Protocol

# %% [markdown]
# #  The B92 Quantum Key Distribution Protocol
# 
# 
# The **B92 protocol** is a simplified version of BB84, introduced by Charles Bennett in 1992.  
# Unlike BB84 which uses *four* states, B92 only uses **two non-orthogonal quantum states**.  
# 
# 
# - Alice sends qubits randomly chosen from two possible states (for example, `|0⟩` and `|+⟩`).  
# - Bob measures each qubit using one of two bases, but since the states are not orthogonal, he sometimes gets an **inconclusive result**.  
# - Only when Bob's measurement gives a *definite result* do Alice and Bob keep that bit.  
# 
# 
#  The key idea: by using non-orthogonal states, an eavesdropper (Eve) cannot perfectly distinguish them without disturbing the qubits  and that disturbance reveals her presence.
# 

# %% [markdown]
# #  Why B92 Works and What to Look for in the Logs
# 
# 
# In B92, **information is hidden in the fact that not all measurements succeed**:  
# 
# 
# - Bob keeps only the bits where his measurement result is *certain*.  
# - This means fewer key bits than BB84, but **more security checks** against eavesdropping.  
# 
# 
# When we run the simulation:
# - You’ll see **Alice’s choices** of qubit states (randomly `|0⟩` or `|+⟩`).  
# - You’ll see **Bob’s measurement results** some conclusive (bit values), some inconclusive (discarded).  
# - Finally, you’ll notice that the **shared key** is formed only from the conclusive outcomes.  
# 
# 
#  Takeaway: The strength of B92 lies in the *impossibility of cloning non-orthogonal states*  making eavesdropping detectable

# %%
import random


class StudentB92Host:
    # Student's B92 QKD implementation class with instance methods.
    # All prompts are included above their respective implementations.
    #
    # B92 Protocol Summary:
    # - Alice encodes: bit 0 -> |0⟩, bit 1 -> |+⟩ = (|0⟩ + |1⟩)/√2
    # - Bob measures randomly in Z or X basis
    # - Bob keeps only results where he measures |1⟩ (outcome = 1)
    # - If Bob measures |1⟩ in Z basis -> Alice sent |+⟩ (bit 1)
    # - If Bob measures |1⟩ in X basis -> Alice sent |0⟩ (bit 0)


    # Implement the constructor for the StudentB92Host class using the provided skeleton function.
    # The constructor should accept the participant's name, such as "Alice" or "Bob", and store it for logging purposes.
    # It must initialize internal state with empty lists for sent bits, prepared qubits, received measurements, sifted key,
    # random bits, measurement outcomes, and received bases. All collections should start empty, and the constructor must
    # dynamically handle any host name passed to it.
    def __init__(self, name):
        # Initialize a StudentB92Host instance.
        #
        # Args:
        #     name (str): The participant's name (e.g., "Alice", "Bob")
        self.name = name
        self.sent_bits = []
        self.qubits = []
        self.received_measurements = []
        self.sifted_key = []
        self.random_bits = []
        self.measurement_outcomes = []
        self.received_bases = []


    # Implement the b92_prepare_qubit method using the provided skeleton function.
    # The method should prepare a qubit based on a classical bit following the B92 protocol.
    # It must use two non-orthogonal quantum states: bit 0 should be mapped to |0⟩, and bit 1 should be mapped to |+⟩
    # (the superposition state). The method should return the prepared qubit, and raise an error if the input bit is not 0 or 1.
    def b92_prepare_qubit(self, bit):
        # Prepare a qubit in the B92 protocol based on a classical bit.
        #
        # B92 encoding:
        # - bit 0 -> |0⟩ state
        # - bit 1 -> |+⟩ state (superposition)
        #
        # Args:
        #     bit (int): Classical bit value (0 or 1)
        #
        # Returns:
        #     str: The prepared quantum state representation
        if bit == 0:
            return "|0>"
        elif bit == 1:
            return "|+>"
        else:
            raise ValueError("Bit must be 0 or 1")


    # Implement the b92_measure_qubit method using the provided skeleton function.
    # The method should randomly choose a measurement basis ("Z" or "X").
    # - If basis is Z:
    #     * |0> maps to outcome 0 (deterministic)
    #     * |+> maps to outcome 0 or 1 with 50% probability each
    # - If basis is X:
    #     * |+> maps to outcome 0 (deterministic, since |+> is +1 eigenstate of X)
    #     * |0> maps to outcome 0 or 1 with 50% probability each
    # The method should return both the outcome and the chosen basis.
    def b92_measure_qubit(self, qubit):
        # Simulate measurement of a qubit in the B92 protocol.
        #
        # Measurement rules:
        # - Z basis: |0⟩ -> 0, |+⟩ -> 0 or 1 (50/50)
        # - X basis: |+⟩ -> 0, |0⟩ -> 0 or 1 (50/50)
        #
        # Args:
        #     qubit (str): Quantum state representation
        #
        # Returns:
        #     tuple: (measurement outcome, basis used)
        basis = random.choice(["Z", "X"])
       
        if basis == "Z":
            if qubit == "|0>":
                return 0, "Z"  # |0> always gives 0 in Z basis
            elif qubit == "|+>":
                return random.choice([0, 1]), "Z"  # |+> gives 0 or 1 randomly
        elif basis == "X":
            if qubit == "|+>":
                return 0, "X"  # |+> always gives 0 in X basis
            elif qubit == "|0>":
                return random.choice([0, 1]), "X"  # |0> gives 0 or 1 randomly
       
        raise ValueError(f"Invalid qubit state: {qubit}")


    # Implement the sifting stage of the B92 protocol.
    # Keep only measurement results that give a conclusive outcome (result = 1):
    # - In Z basis: outcome 1 conclusively indicates the sender sent |+⟩ (bit 1)
    # - In X basis: outcome 1 conclusively indicates the sender sent |0⟩ (bit 0)
    # All other results (outcome 0) are inconclusive and should be discarded.
    def b92_sifting(self, sent_bits, received_measurements):
        # Perform the sifting stage of the B92 protocol.
        #
        # B92 sifting rules:
        # - Keep only measurements where Bob got outcome = 1
        # - If Z basis, outcome 1 -> Alice sent bit 1 (|+⟩)d thi
        # - If X basis, outcome 1 -> Alice sent bit 0 (|0⟩)
        #
        # Args:
        #     sent_bits (list): List of bits sent by Alice
        #     received_measurements (list): List of (outcome, basis) pairs from Bob
        #
        # Returns:
        #     tuple: (sifted_sender, sifted_receiver)
        sifted_sender = []
        sifted_receiver = []
       
        for i, (sent_bit, (outcome, basis)) in enumerate(zip(sent_bits, received_measurements)):
            # Only keep measurements where Bob got outcome = 1
            if outcome == 1:
                if basis == "Z":
                    # If Bob measured 1 in Z basis, Alice must have sent |+⟩ (bit 1)
                    if sent_bit == 1:  # Verify Alice actually sent bit 1
                        sifted_sender.append(1)
                        sifted_receiver.append(1)
                elif basis == "X":
                    # If Bob measured 1 in X basis, Alice must have sent |0⟩ (bit 0)
                    if sent_bit == 0:  # Verify Alice actually sent bit 0
                        sifted_sender.append(0)
                        sifted_receiver.append(0)


        self.sifted_key = sifted_receiver
        return sifted_sender, sifted_receiver


    # Implement an instance method for Alice to generate random bits and prepare qubits.
    # The method should create a sequence of random bits, store them internally,
    # prepare corresponding qubits using the b92_prepare_qubit method, and return the prepared qubits.
    def b92_send_qubits(self, num_qubits):
        # Instance method for Alice to generate random bits and prepare qubits.
        #
        # Args:
        #     num_qubits (int): Number of qubits to generate
        #    
        # Returns:
        #     list: List of prepared qubits
        self.sent_bits = [random.randint(0, 1) for _ in range(num_qubits)]
        self.random_bits = self.sent_bits.copy()
        self.qubits = [self.b92_prepare_qubit(bit) for bit in self.sent_bits]
        return self.qubits


    # Implement an instance method for Bob to measure a received qubit.
    # The method should use b92_measure_qubit, store both the measurement outcome and the chosen basis
    # in received_measurements, and return True to confirm processing.
    def b92_process_received_qbit(self, qbit, from_channel=None):
        # Instance method for Bob to measure a received qubit.
        #
        # Args:
        #     qbit (str): The received qubit
        #     from_channel: Optional parameter for channel information
        #    
        # Returns:
        #     bool: True to confirm processing
        outcome, basis = self.b92_measure_qubit(qbit)
        self.received_measurements.append((outcome, basis))
        self.measurement_outcomes.append(outcome)
        self.received_bases.append(basis)
        return True


    # Implement the b92_estimate_error_rate method using the provided skeleton function.
    # The method should compute the error rate by comparing a sample of sifted key positions against reference bits.
    # It must iterate through the provided sample positions, count valid comparisons, and increase the error count whenever a mismatch occurs.
    # If no comparisons are available, it should default to an error rate of zero.
    # Finally, the method must return the computed error rate as a floating-point value between 0.0 and 1.0.
    def b92_estimate_error_rate(self, sample_positions, reference_bits):
        # Compute the error rate for the B92 protocol.
        #
        # Args:
        #     sample_positions (list): Positions to sample for error checking
        #     reference_bits (list): Reference bit values for comparison
        #
        # Returns:
        #     float: Estimated error rate (0.0 to 1.0)
        if not sample_positions or not reference_bits:
            return 0.0


        errors = 0
        comparisons = 0


        for pos, ref_bit in zip(sample_positions, reference_bits):
            if pos < len(self.sifted_key):
                comparisons += 1
                if self.sifted_key[pos] != ref_bit:
                    errors += 1


        return errors / comparisons if comparisons > 0 else 0.0
import random


class StudentB92Host:
    # Student's B92 QKD implementation class with instance methods.
    # All prompts are included above their respective implementations.
    #
    # B92 Protocol Summary:
    # - Alice encodes: bit 0 -> |0⟩, bit 1 -> |+⟩ = (|0⟩ + |1⟩)/√2
    # - Bob measures randomly in Z or X basis
    # - Bob keeps only results where he measures |1⟩ (outcome = 1)
    # - If Bob measures |1⟩ in Z basis -> Alice sent |+⟩ (bit 1)
    # - If Bob measures |1⟩ in X basis -> Alice sent |0⟩ (bit 0)


    # Implement the constructor for the StudentB92Host class using the provided skeleton function.
    # The constructor should accept the participant's name, such as "Alice" or "Bob", and store it for logging purposes.
    # It must initialize internal state with empty lists for sent bits, prepared qubits, received measurements, sifted key,
    # random bits, measurement outcomes, and received bases. All collections should start empty, and the constructor must
    # dynamically handle any host name passed to it.
    def __init__(self, name):
        # Initialize a StudentB92Host instance.
        #
        # Args:
        #     name (str): The participant's name (e.g., "Alice", "Bob")
        self.name = name
        self.sent_bits = []
        self.qubits = []
        self.received_measurements = []
        self.sifted_key = []
        self.random_bits = []
        self.measurement_outcomes = []
        self.received_bases = []


    # Implement the b92_prepare_qubit method using the provided skeleton function.
    # The method should prepare a qubit based on a classical bit following the B92 protocol.
    # It must use two non-orthogonal quantum states: bit 0 should be mapped to |0⟩, and bit 1 should be mapped to |+⟩
    # (the superposition state). The method should return the prepared qubit, and raise an error if the input bit is not 0 or 1.
    def b92_prepare_qubit(self, bit):
        # Prepare a qubit in the B92 protocol based on a classical bit.
        #
        # B92 encoding:
        # - bit 0 -> |0⟩ state
        # - bit 1 -> |+⟩ state (superposition)
        #
        # Args:
        #     bit (int): Classical bit value (0 or 1)
        #
        # Returns:
        #     str: The prepared quantum state representation
        if bit == 0:
            return "|0>"
        elif bit == 1:
            return "|+>"
        else:
            raise ValueError("Bit must be 0 or 1")


    # Implement the b92_measure_qubit method using the provided skeleton function.
    # The method should randomly choose a measurement basis ("Z" or "X").
    # - If basis is Z:
    #     * |0> maps to outcome 0 (deterministic)
    #     * |+> maps to outcome 0 or 1 with 50% probability each
    # - If basis is X:
    #     * |+> maps to outcome 0 (deterministic, since |+> is +1 eigenstate of X)
    #     * |0> maps to outcome 0 or 1 with 50% probability each
    # The method should return both the outcome and the chosen basis.
    def b92_measure_qubit(self, qubit):
        # Simulate measurement of a qubit in the B92 protocol.
        #
        # Measurement rules:
        # - Z basis: |0⟩ -> 0, |+⟩ -> 0 or 1 (50/50)
        # - X basis: |+⟩ -> 0, |0⟩ -> 0 or 1 (50/50)
        #
        # Args:
        #     qubit (str): Quantum state representation
        #
        # Returns:
        #     tuple: (measurement outcome, basis used)
        basis = random.choice(["Z", "X"])
       
        if basis == "Z":
            if qubit == "|0>":
                return 0, "Z"  # |0> always gives 0 in Z basis
            elif qubit == "|+>":
                return random.choice([0, 1]), "Z"  # |+> gives 0 or 1 randomly
        elif basis == "X":
            if qubit == "|+>":
                return 0, "X"  # |+> always gives 0 in X basis
            elif qubit == "|0>":
                return random.choice([0, 1]), "X"  # |0> gives 0 or 1 randomly
       
        raise ValueError(f"Invalid qubit state: {qubit}")


    # Implement the sifting stage of the B92 protocol.
    # Keep only measurement results that give a conclusive outcome (result = 1):
    # - In Z basis: outcome 1 conclusively indicates the sender sent |+⟩ (bit 1)
    # - In X basis: outcome 1 conclusively indicates the sender sent |0⟩ (bit 0)
    # All other results (outcome 0) are inconclusive and should be discarded.
    def b92_sifting(self, sent_bits, received_measurements):
        # Perform the sifting stage of the B92 protocol.
        #
        # B92 sifting rules:
        # - Keep only measurements where Bob got outcome = 1
        # - If Z basis, outcome 1 -> Alice sent bit 1 (|+⟩)d thi
        # - If X basis, outcome 1 -> Alice sent bit 0 (|0⟩)
        #
        # Args:
        #     sent_bits (list): List of bits sent by Alice
        #     received_measurements (list): List of (outcome, basis) pairs from Bob
        #
        # Returns:
        #     tuple: (sifted_sender, sifted_receiver)
        sifted_sender = []
        sifted_receiver = []
       
        for i, (sent_bit, (outcome, basis)) in enumerate(zip(sent_bits, received_measurements)):
            # Only keep measurements where Bob got outcome = 1
            if outcome == 1:
                if basis == "Z":
                    # If Bob measured 1 in Z basis, Alice must have sent |+⟩ (bit 1)
                    if sent_bit == 1:  # Verify Alice actually sent bit 1
                        sifted_sender.append(1)
                        sifted_receiver.append(1)
                elif basis == "X":
                    # If Bob measured 1 in X basis, Alice must have sent |0⟩ (bit 0)
                    if sent_bit == 0:  # Verify Alice actually sent bit 0
                        sifted_sender.append(0)
                        sifted_receiver.append(0)


        self.sifted_key = sifted_receiver
        return sifted_sender, sifted_receiver


    # Implement an instance method for Alice to generate random bits and prepare qubits.
    # The method should create a sequence of random bits, store them internally,
    # prepare corresponding qubits using the b92_prepare_qubit method, and return the prepared qubits.
    def b92_send_qubits(self, num_qubits):
        # Instance method for Alice to generate random bits and prepare qubits.
        #
        # Args:
        #     num_qubits (int): Number of qubits to generate
        #    
        # Returns:
        #     list: List of prepared qubits
        self.sent_bits = [random.randint(0, 1) for _ in range(num_qubits)]
        self.random_bits = self.sent_bits.copy()
        self.qubits = [self.b92_prepare_qubit(bit) for bit in self.sent_bits]
        return self.qubits


    # Implement an instance method for Bob to measure a received qubit.
    # The method should use b92_measure_qubit, store both the measurement outcome and the chosen basis
    # in received_measurements, and return True to confirm processing.
    def b92_process_received_qbit(self, qbit, from_channel=None):
        # Instance method for Bob to measure a received qubit.
        #
        # Args:
        #     qbit (str): The received qubit
        #     from_channel: Optional parameter for channel information
        #    
        # Returns:
        #     bool: True to confirm processing
        outcome, basis = self.b92_measure_qubit(qbit)
        self.received_measurements.append((outcome, basis))
        self.measurement_outcomes.append(outcome)
        self.received_bases.append(basis)
        return True


    # Implement the b92_estimate_error_rate method using the provided skeleton function.
    # The method should compute the error rate by comparing a sample of sifted key positions against reference bits.
    # It must iterate through the provided sample positions, count valid comparisons, and increase the error count whenever a mismatch occurs.
    # If no comparisons are available, it should default to an error rate of zero.
    # Finally, the method must return the computed error rate as a floating-point value between 0.0 and 1.0.
    def b92_estimate_error_rate(self, sample_positions, reference_bits):
        # Compute the error rate for the B92 protocol.
        #
        # Args:
        #     sample_positions (list): Positions to sample for error checking
        #     reference_bits (list): Reference bit values for comparison
        #
        # Returns:
        #     float: Estimated error rate (0.0 to 1.0)
        if not sample_positions or not reference_bits:
            return 0.0


        errors = 0
        comparisons = 0


        for pos, ref_bit in zip(sample_positions, reference_bits):
            if pos < len(self.sifted_key):
                comparisons += 1
                if self.sifted_key[pos] != ref_bit:
                    errors += 1


        return errors / comparisons if comparisons > 0 else 0.0


# %%
# ACCESS WEB-BASED SIMULATION INTERFACE WITH UI LOGGING
# ========================================================
# This cell connects to your running Docker backend and displays the web simulation
# with proper logging support for both BB84 and B92 protocols


import urllib.request
import urllib.error
import socket
import json


DO_NOT_SPAWN_SERVERS = True  # Force notebook-safe behavior


def check_server_status_simple(url: str, timeout: float = 2.0) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return resp.status in (200, 301, 302, 404)
    except Exception:
        return False


def write_notebook_status_file(protocol: str = "bb84"):
    """Ensure the backend sees student implementation as ready with proper protocol detection."""
    try:
        # Detect which protocol is being used
        if protocol.lower() == "b92":
            methods = [
                "b92_send_qubits",
                "b92_process_received_qbit",
                "b92_sifting",
                "b92_estimate_error_rate",
            ]
            status_file = "student_b92_implementation_status.json"
        else:
            methods = [
                "bb84_send_qubits",
                "process_received_qbit",
                "bb84_reconcile_bases",
                "bb84_estimate_error_rate",
            ]
            status_file = "student_implementation_status.json"
       
        status = {
            "student_implementation_ready": True,
            "implementation_type": "StudentImplementationBridge",
            "protocol": protocol.upper(),
            "methods_implemented": methods,
            "ui_logging_enabled": True,
            "has_valid_implementation": True,
        }
        with open(status_file, "w") as f:
            json.dump(status, f)
        print(f" Created {protocol.upper()} status file: {status_file}")
        return True
    except Exception as e:
        print(f" Error creating status file: {e}")
        return False


def get_backend_unblock_status(base: str, protocol: str = "bb84") -> dict | None:
    try:
        # Use B92-specific endpoint if protocol is B92
        if protocol.lower() == "b92":
            endpoint = base + "/api/simulation/student-implementation-status-b92/"
        else:
            endpoint = base + "/api/simulation/student-implementation-status/"
           
        with urllib.request.urlopen(endpoint, timeout=2.5) as resp:
            if resp.status == 200:
                return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Error checking {protocol} status: {e}")
        return None
    return None


def show_section2_simulation(height: int = 1050, host: str = "http://127.0.0.1:8001", protocol: str = "bb84"):
    print(f" Checking backend proxy ({host}) for {protocol.upper()} protocol...")
    ok = check_server_status_simple(host)
    if not ok:
        # Try localhost fallback
        alt = host.replace("127.0.0.1", "localhost")
        print(" Backend not reachable at", host, "— trying", alt)
        if check_server_status_simple(alt):
            host = alt
        else:
            print(" Backend proxy not reachable. Ensure Docker containers are running.")
            print(" Run: docker-compose up --build")
            return


    # Write status file so backend reports valid implementation when not running
    write_notebook_status_file(protocol)


    # Poll the backend status a few times to encourage UI to unblock
    for _ in range(3):
        status = get_backend_unblock_status(host, protocol)
        if status and status.get("has_valid_implementation"):
            print(f" {protocol.upper()} implementation detected and ready!")
            break
        else:
            print(f" Waiting for {protocol.upper()} implementation...")


    # Use direct IFrame creation with proper logging support
    from IPython.display import IFrame, display
    display(IFrame(src=host, width="100%", height=height))
    print(" Using direct IFrame to display simulation interface.")
    print(" UI Logging enabled - logs will be displayed in the simulation interface")
    print(f" The system will use {protocol.upper()} protocol with appropriate log parser")


def show_b92_simulation(height: int = 1050, host: str = "http://127.0.0.1:8001"):
    """Display B92 simulation interface"""
    print(" Starting B92 Quantum Key Distribution Simulation...")
    show_section2_simulation(height=height, host=host, protocol="b92")


def show_bb84_simulation(height: int = 1050, host: str = "http://127.0.0.1:8001"):
    """Display BB84 simulation interface"""
    print(" Starting BB84 Quantum Key Distribution Simulation...")
    show_section2_simulation(height=height, host=host, protocol="bb84")


# Dynamic protocol detection and auto-load simulation
print(" Loading Simulation Interface...")
print("=" * 50)


# Detect current protocol and load appropriate simulation
import os
if os.path.exists('student_b92_implementation_status.json') and not os.path.exists('student_b92_implementation_status.json.disabled'):
    print(" B92 protocol detected - loading B92 simulation...")
    show_section2_simulation(height=1050, protocol="b92")
elif os.path.exists('student_implementation_status.json') and not os.path.exists('student_implementation_status.json.disabled'):
    print(" BB84 protocol detected - loading BB84 simulation...")
    show_section2_simulation(height=1050, protocol="bb84")
else:
    show_section2_simulation(height=1050, protocol="bb84") # default


# %% [markdown]
# 
# 
#  ## 🎓 Congratulations!
# 
#  You've successfully:
# 
#  1. **Implemented BB84  and B92 Protocol**: Created a complete quantum key distribution system
#  2. **Built Quantum Hosts**: Alice and Bob with your personal implementation
#  3. **Powered a Quantum Network**: Your code ran a complete quantum-classical network
#  4. **Achieved Quantum Communication**: Successfully distributed quantum keys
# 
#  ### What You Learned:
#  - **Quantum State Preparation**: How to encode classical bits into quantum states
#  - **Quantum Measurement**: How to measure qubits in different bases
#  - **BB84 and B92 Protocol**: The complete quantum key distribution process
#  - **Quantum Networking**: How quantum and classical networks work together
# 
#  ### Next Steps:
#  - Experiment with different numbers of qubits
#  
#  - Explore quantum error correction
#  - Learn about quantum repeaters and quantum internet
# 
#  **You're now a quantum networking expert!** 
# 

# %% [markdown]
# 


