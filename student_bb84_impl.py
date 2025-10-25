import random


class StudentQuantumHost:
    """
    Your personal BB84 implementation!
    This class will be used by the quantum network simulation.
    """

    # PROMPT FOR CONSTRUCTOR:
    """
    Create a constructor that accepts a single parameter for the host's identifier.
    Store this identifier as an instance variable. Initialize five empty list attributes:
    one for storing random binary values, one for preparation bases, one for encoded states,
    one for measurement bases used during reception, and one for measurement results.
    After initialization, print a confirmation message in the format:
    "StudentQuantumHost '<identifier>' initialized successfully!"
    where <identifier> is replaced with the actual value passed to the constructor.
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
        Create a method that accepts an integer parameter specifying the quantity of qubits to prepare.
        Print a message indicating the host is preparing this quantity of qubits.
        Clear and reinitialize three instance lists: one for random bits, one for bases, and one for quantum states.
        For each qubit in the specified quantity:
        - Generate a random bit (0 or 1)
        - Generate a random basis (0 or 1)
        - If basis is 0: encode bit 0 as "|0⟩" and bit 1 as "|1⟩"
        - If basis is 1: encode bit 0 as "|+⟩" and bit 1 as "|-⟩"
        - Append the random bit to the first list, the basis to the second list, and the encoded state to the third list
        After processing all qubits, print a message showing how many qubits were prepared.
        Return the list of encoded quantum states.
        """
    def bb84_send_qubits(self, num_qubits):
        print(f"{self.name} is preparing {num_qubits} qubits...")
        self.random_bits = []
        self.measurement_bases = []
        self.quantum_states = []

        for _ in range(num_qubits):
            bit = random.randint(0, 1)
            basis = random.randint(0, 1)

            if basis == 0:
                state = "|0⟩" if bit == 0 else "|1⟩"
            else:
                state = "|+⟩" if bit == 0 else "|-⟩"

            self.random_bits.append(bit)
            self.measurement_bases.append(basis)
            self.quantum_states.append(state)

        print(f"{self.name} prepared {len(self.quantum_states)} qubits")
        return self.quantum_states

