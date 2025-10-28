# enhanced_student_bridge.py
# ===================================
# Bridge for using StudentQuantumHost implementation from student_bb84_impl.py
# Preserves all features: qubit sending, receiving, basis reconciliation, error estimation

import random
import json

# Import student's actual BB84 implementation
from student_bb84_impl import StudentQuantumHost

# Helper functions for quantum operations (kept for compatibility)
def prepare_quantum_state(bit, basis):
    """Prepare a quantum state (used internally by fallback or testing)"""
    if basis == 0:  # Z-basis
        return '|0⟩' if bit == 0 else '|1⟩'
    else:  # X-basis
        return '|+⟩' if bit == 0 else '|-⟩'

def measure_quantum_state(quantum_state, measurement_basis):
    """Measure a quantum state in a given basis (used internally)"""
    if measurement_basis == 0:
        if quantum_state in ['|0⟩', '|1⟩']:
            return 0 if quantum_state == '|0⟩' else 1
        else:
            return random.randint(0, 1)
    else:
        if quantum_state in ['|+⟩', '|-⟩']:
            return 0 if quantum_state == '|+⟩' else 1
        else:
            return random.randint(0, 1)

# =================================================
# Enhanced bridge class using student's actual code
# =================================================
class EnhancedStudentImplementationBridge:
    """Directly uses StudentQuantumHost from student_bb84_impl.py"""
    
    def __init__(self, student_alice=None, student_bob=None, alice_name=None, bob_name=None):
        # Support both parameter styles for backwards compatibility
        if alice_name is not None:
            print(f"Creating Alice using StudentQuantumHost with name: {alice_name}...")
            self.student_alice = StudentQuantumHost(alice_name)
        elif student_alice is None:
            print("Creating Alice using StudentQuantumHost...")
            self.student_alice = StudentQuantumHost("Alice")
        else:
            self.student_alice = student_alice
            
        if bob_name is not None:
            print(f"Creating Bob using StudentQuantumHost with name: {bob_name}...")
            self.student_bob = StudentQuantumHost(bob_name)
        elif student_bob is None:
            print("Creating Bob using StudentQuantumHost...")
            self.student_bob = StudentQuantumHost("Bob")
        else:
            self.student_bob = student_bob
            
        self.host = None
        self.qkd_phase = "idle"
        self.bits_received = 0
        self.expected_bits = 0
        
        print("✅ Enhanced Bridge created using StudentQuantumHost!")
        print(f"   Alice type: {type(self.student_alice).__name__}")
        print(f"   Bob type: {type(self.student_bob).__name__}")
    
    def bb84_send_qubits(self, num_qubits):
        """Send qubits using student's implementation directly"""
        if self.host is None:
            print("Bridge not attached to a simulation host")
            return False
            
        self.qkd_phase = "sending"
        self.expected_bits = num_qubits
        print(f"Starting BB84 protocol with {num_qubits} qubits")
        
        if self.host and hasattr(self.host, '_send_update'):
            from core.enums import SimulationEventType
            self.host._send_update(SimulationEventType.INFO, 
                                   num_qubits=num_qubits, 
                                   protocol="BB84",
                                   message=f"STUDENT BB84: Starting with {num_qubits} qubits using your code!",
                                   student_implementation="StudentQuantumHost")
        
        # Call student's method
        encoded_qubits = self.student_alice.bb84_send_qubits(num_qubits)
        
        # Store Alice's data on host
        self.host.basis_choices = list(self.student_alice.measurement_bases)
        self.host.measurement_outcomes = list(self.student_alice.random_bits)
        
        # Send through quantum channel
        channel = self.host.get_channel()
        if channel is None:
            print(f"ERROR: {self.host.name} has no quantum channel")
            return False
        
        print(f"Sending {len(encoded_qubits)} qubits through quantum channel...")
        for i, q in enumerate(encoded_qubits):
            self.host.send_qubit(q, channel)
            if i % 10 == 0:
                print(f"   Sent {i+1}/{len(encoded_qubits)} qubits")
        
        print(f"All {len(encoded_qubits)} qubits sent successfully")
        
        if self.host and hasattr(self.host, '_send_update'):
            from core.enums import SimulationEventType
            self.host._send_update(SimulationEventType.DATA_SENT, 
                                   qubits_sent=len(encoded_qubits),
                                   message=f"STUDENT BB84: Sent {len(encoded_qubits)} qubits using bb84_send_qubits()!")
        
        # Trigger reconciliation
        if self.host and hasattr(self.host, 'send_bases_for_reconcile'):
            self.host.send_bases_for_reconcile()
        
        return True
    
    def process_received_qbit(self, qbit, from_channel):
        """Measure received qubit using student's implementation"""
        if self.host is None:
            return False
            
        if self.qkd_phase == "idle":
            self.qkd_phase = "receiving"
            print("Started receiving qubits...")
            
        self.bits_received += 1
        result = self.student_bob.process_received_qbit(qbit, from_channel)
        
        self.host.basis_choices = list(self.student_bob.received_bases)
        self.host.measurement_outcomes = list(self.student_bob.measurement_outcomes)
        
        if self.host and hasattr(self.host, '_send_update'):
            from core.enums import SimulationEventType
            self.host._send_update(SimulationEventType.DATA_RECEIVED,
                                   message=f"STUDENT BOB: Received qubit {self.bits_received}/{self.expected_bits}!",
                                   qubits_received=self.bits_received,
                                   total_expected=self.expected_bits)
        
        if self.bits_received % 10 == 0:
            print(f"   Received {self.bits_received}/{self.expected_bits} qubits")
        
        if self.bits_received >= self.expected_bits:
            print(f"Received all {self.bits_received} qubits, ready for reconciliation...")
            self.qkd_phase = "ready_for_reconciliation"
        
        return result
    
    def bb84_reconcile_bases(self, their_bases):
        """Find matching bases using student's implementation"""
        if self.host is None:
            return False
        
        self.qkd_phase = "reconciling"
        print("Starting basis reconciliation...")
        
        shared_indices, shared_bits = self.student_bob.bb84_reconcile_bases(
            alice_bases=their_bases,
            bob_bases=self.student_bob.received_bases
        )
        
        self.host.shared_bases_indices = list(shared_indices)
        
        if self.host and hasattr(self.host, '_send_update'):
            from core.enums import SimulationEventType
            efficiency = (len(shared_indices) / len(their_bases) * 100) if their_bases else 0
            self.host._send_update(SimulationEventType.INFO,
                                   message=f"STUDENT BOB: Found {len(shared_indices)} matching bases ({efficiency:.1f}% efficiency)!",
                                   shared_bases=len(shared_indices),
                                   efficiency=efficiency)
        
        self.host.send_classical_data({'type': 'shared_bases_indices', 'data': self.host.shared_bases_indices})
        return shared_indices, shared_bits
    
    def bb84_estimate_error_rate(self, their_bits_sample):
        """Compute error rate using student's implementation"""
        if self.host is None:
            return False
        
        self.qkd_phase = "error_checking"
        print("Starting error rate estimation...")
        
        positions, reference_bits = zip(*their_bits_sample) if their_bits_sample else ([], [])
        error_rate = self.student_bob.bb84_estimate_error_rate(positions, reference_bits)
        
        print(f"Student Bob error rate: {error_rate:.1%}")
        
        if self.host and hasattr(self.host, '_send_update'):
            from core.enums import SimulationEventType
            self.host._send_update(SimulationEventType.INFO,
                                   message=f"STUDENT BOB: Error rate {error_rate:.1%} using bb84_estimate_error_rate()!",
                                   error_rate=error_rate)
        
        if self.host and hasattr(self.host, '_send_update'):
            from core.enums import SimulationEventType
            self.host._send_update(SimulationEventType.SHARED_KEY_GENERATED,
                                   message="BB84 QKD protocol completed successfully using student's code!",
                                   error_rate=error_rate,
                                   shared_bases=len(self.host.shared_bases_indices))
        
        self.host.send_classical_data({'type': 'complete'})
        self.qkd_phase = "complete"
        
        print("BB84 PROTOCOL COMPLETE using student's implementation!")
        return error_rate
    
    def update_shared_bases_indices(self, shared_base_indices):
        """Update shared bases indices - called by Alice"""
        if self.host is None:
            return False
        
        print(f"Alice: Received {len(shared_base_indices)} shared bases indices from Bob")
        self.host.shared_bases_indices = shared_base_indices
        
        if self.host and hasattr(self.host, 'update_shared_bases_indices'):
            self.host.update_shared_bases_indices(shared_base_indices)
        
        return True

# ==========================================
# Simple wrapper to attach bridge to host
# ==========================================
class StudentImplementationBridge:
    """Wrapper that uses EnhancedStudentImplementationBridge"""
    
    def __init__(self, host):
        self.host = host
        self._bridge = EnhancedStudentImplementationBridge()
        self._bridge.host = host
        print(f"✅ Bridge created using StudentQuantumHost for host: {host.name if host else 'Unknown'}")
    
    def set_host(self, host):
        self.host = host
        self._bridge.host = host
        print(f"Bridge host updated: {host.name if host else 'Unknown'}")
    
    def bb84_send_qubits(self, num_qubits):
        return self._bridge.bb84_send_qubits(num_qubits)
    
    def process_received_qbit(self, qbit, from_channel):
        return self._bridge.process_received_qbit(qbit, from_channel)
    
    def bb84_reconcile_bases(self, their_bases):
        return self._bridge.bb84_reconcile_bases(their_bases)
    
    def bb84_estimate_error_rate(self, their_bits_sample):
        return self._bridge.bb84_estimate_error_rate(their_bits_sample)
