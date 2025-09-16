import random

class StudentB92Host:
    """
    Student's B92 QKD implementation class with instance methods.
    All prompts are included above their respective implementations.

    B92 Protocol Summary:
    - Alice encodes: bit 0 -> |0⟩, bit 1 -> |+⟩ = (|0⟩ + |1⟩)/√2
    - Bob measures randomly in Z or X basis
    - Bob keeps only results where he measures |1⟩ (outcome = 1)
    - If Bob measures |1⟩ in Z basis -> Alice sent |+⟩ (bit 1)
    - If Bob measures |1⟩ in X basis -> Alice sent |0⟩ (bit 0)
    """

    # Implement the constructor for the StudentB92Host class using the provided skeleton function.
    # The constructor should accept the participant's name, such as "Alice" or "Bob", and store it for logging purposes.
    # It must initialize internal state with empty lists for sent bits, prepared qubits, received measurements, sifted key,
    # random bits, measurement outcomes, and received bases. All collections should start empty, and the constructor must 
    # dynamically handle any host name passed to it.
    def __init__(self, name):
        """
        Initialize a StudentB92Host instance.

        Args:
            name (str): The participant's name (e.g., "Alice", "Bob")
        """
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
        """
        Prepare a qubit in the B92 protocol based on a classical bit.

        B92 encoding:
        - bit 0 -> |0⟩ state
        - bit 1 -> |+⟩ state (superposition)

        Args:
            bit (int): Classical bit value (0 or 1)

        Returns:
            str: The prepared quantum state representation
        """
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
        """
        Simulate measurement of a qubit in the B92 protocol.

        Measurement rules:
        - Z basis: |0⟩ -> 0, |+⟩ -> 0 or 1 (50/50)
        - X basis: |+⟩ -> 0, |0⟩ -> 0 or 1 (50/50)

        Args:
            qubit (str): Quantum state representation

        Returns:
            tuple: (measurement outcome, basis used)
        """
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
        """
        Perform the sifting stage of the B92 protocol.

        B92 sifting rules:
        - Keep only measurements where Bob got outcome = 1
        - If Z basis, outcome 1 -> Alice sent bit 1 (|+⟩)
        - If X basis, outcome 1 -> Alice sent bit 0 (|0⟩)

        Args:
            sent_bits (list): List of bits sent by Alice
            received_measurements (list): List of (outcome, basis) pairs from Bob

        Returns:
            tuple: (sifted_sender, sifted_receiver)
        """
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
        """
        Instance method for Alice to generate random bits and prepare qubits.

        Args:
            num_qubits (int): Number of qubits to generate

        Returns:
            list: List of prepared qubits
        """
        self.sent_bits = [random.randint(0, 1) for _ in range(num_qubits)]
        self.random_bits = self.sent_bits.copy()
        self.qubits = [self.b92_prepare_qubit(bit) for bit in self.sent_bits]
        return self.qubits

    # Implement an instance method for Bob to measure a received qubit.
    # The method should use b92_measure_qubit, store both the measurement outcome and the chosen basis
    # in received_measurements, and return True to confirm processing.
    def b92_process_received_qbit(self, qbit, from_channel=None):
        """
        Instance method for Bob to measure a received qubit.

        Args:
            qbit (str): The received qubit
            from_channel: Optional parameter for channel information

        Returns:
            bool: True to confirm processing
        """
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
        """
        Compute the error rate for the B92 protocol.

        Args:
            sample_positions (list): Positions to sample for error checking
            reference_bits (list): Reference bit values for comparison

        Returns:
            float: Estimated error rate (0.0 to 1.0)
        """
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


)
