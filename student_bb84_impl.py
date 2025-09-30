# coding: utf-8
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
