import requests
import json
import os
from typing import Optional
import ipywidgets as widgets
from IPython.display import display, Markdown
from .vector_db_manager import VectorDBManager

class PeerAgent:
    """
    The backend "brain" for the Student Peer agent. It handles RAG searches
    and communication with an LLM via Ollama.
    """
    def __init__(self, 
                 db_path: str,
                 ollama_embed_model: str = 'nomic-embed-text',
                 ollama_chat_model: str = 'codellama:7b',
                 ollama_base_url: str = 'http://10.80.14.216:11434'):
        """Initializes the PeerAgent's backend."""
        self.db_manager = VectorDBManager(path=db_path, ollama_model=ollama_embed_model)
        self.ollama_chat_model = ollama_chat_model
        self.ollama_api_url = f"{ollama_base_url}/api/generate"

    def _call_ollama_llm(self, prompt: str) -> str:
        """Calls the Ollama API to get a response from the chat model."""
        try:
            payload = {
                "model": self.ollama_chat_model,
                "prompt": prompt,
                "stream": False 
            }
            response = requests.post(self.ollama_api_url, json=payload)
            response.raise_for_status()
            return response.json().get("response", "Sorry, I couldn't come up with a response.")
        except requests.exceptions.RequestException as e:
            error_message = f"Error calling Ollama API: {e}. Please ensure Ollama is running and the model '{self.ollama_chat_model}' is pulled."
            print(error_message)
            return error_message

    def _format_code_output(self, raw_output: str) -> str:
        """Clean and format code output using AST parsing for proper formatting."""
        import re
        import ast
        
        cleaned = raw_output.strip()
        
        # Step 1: Remove markdown code blocks and tags
        cleaned = re.sub(r'```python\n?', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'```\n?', '', cleaned, flags=re.IGNORECASE)
        
        tags_to_remove = [
            r'\[PYTHON\]', r'\[/PYTHON\]', 
            r'\[TESTS\]', r'\[/TESTS\]',
            r'\[TEST\]', r'\[/TEST\]',
            r'\[CODE\]', r'\[/CODE\]',
            r'<\|python\|>', r'<\|endoftext\|>',
            r'<\|end\|>', r'<python>', r'</python>'
        ]
        for tag in tags_to_remove:
            cleaned = re.sub(tag, '', cleaned, flags=re.IGNORECASE)
        
        # Step 2: Find the method definition
        def_match = re.search(r'def\s+\w+\([^)]*\):', cleaned)
        if not def_match:
            return cleaned.strip()
        
        # Extract from 'def' onwards and remove explanatory text after the method
        code = cleaned[def_match.start():]
        
        # Remove explanatory text after method (common patterns)
        explanatory_patterns = [
            r'\n\s*This (method|function|code)',
            r'\n\s*The above',
            r'\n\s*You can use',
            r'\n\s*Example usage:',
            r'\n\s*# Test',
            r'\n\s*if __name__',
        ]
        for pattern in explanatory_patterns:
            match = re.search(pattern, code, re.IGNORECASE)
            if match:
                code = code[:match.start()]
        
        # Step 3: Try AST-based reformatting (handles single-line code)
        try:
            # Parse the code into an AST
            tree = ast.parse(code)
            
            # Use ast.unparse (Python 3.9+) to reformat
            try:
                formatted_code = ast.unparse(tree)
                return formatted_code.strip()
            except AttributeError:
                # Python < 3.9, fall back to manual formatting
                pass
        except SyntaxError:
            # Code has syntax errors, try to fix common issues
            pass
        
        # Step 4: Fallback - Manual line-by-line formatting for single-line code
        # This handles the case where CodeLlama outputs everything on one line
        
        # First, ensure there's a space after colons if missing
        code = re.sub(r':(\S)', r': \1', code)
        
        # Add newlines after statement-ending patterns
        # Pattern: after def line's colon
        code = re.sub(r'(def\s+\w+\([^)]*\):)\s*', r'\1\n    ', code)
        
        # Pattern: Split statements that should be on separate lines
        # This is a simplified approach - split by common keywords
        formatted_lines = []
        current_line = ""
        indent_level = 0
        
        # Split by keywords and operators that indicate new statements
        tokens = re.split(r'(\s+def\s+|\s+if\s+|\s+elif\s+|\s+else:|\s+for\s+|\s+while\s+|\s+return\s+|\s+print\(|self\.\w+\s*=|^\s*\w+\s*=)', code)
        
        in_function = False
        for i, token in enumerate(tokens):
            token_stripped = token.strip()
            
            if token_stripped.startswith('def '):
                if formatted_lines:
                    formatted_lines.append('\n')
                formatted_lines.append(token_stripped)
                in_function = True
                indent_level = 1
            elif token_stripped.startswith(('if ', 'elif ', 'for ', 'while ')):
                formatted_lines.append('\n' + '    ' * indent_level + token_stripped)
                indent_level += 1
            elif token_stripped == 'else:':
                indent_level -= 1
                formatted_lines.append('\n' + '    ' * indent_level + token_stripped)
                indent_level += 1
            elif token_stripped.startswith('return '):
                formatted_lines.append('\n' + '    ' * indent_level + token_stripped)
            elif token_stripped.startswith('print(') or '=' in token_stripped:
                formatted_lines.append('\n' + '    ' * indent_level + token_stripped)
            elif token_stripped:
                formatted_lines.append(token)
        
        result = ''.join(formatted_lines)
        
        # Step 5: Clean up excessive whitespace
        while '\n\n\n' in result:
            result = result.replace('\n\n\n', '\n\n')
        
        # Remove trailing whitespace from each line
        result = '\n'.join(line.rstrip() for line in result.split('\n'))
        
        return result.strip()

    def _get_protocol_guidelines(self, protocol: str) -> tuple:
        """Returns coding style guidelines and structure for the specified protocol."""
        if protocol == 'BB84':
            style_guide = """
CODING STYLE REQUIREMENTS:
1. Use 4-space indentation
2. Print informative messages using f-strings: print(f"{{self.name}} is doing X...")
3. Initialize/clear lists at the start of methods when needed
4. Use if-elif-else chains for conditional logic
5. Use for loops with enumerate() or range() for iterations
6. Append to instance variable lists to track state
7. Calculate and print statistics/results before returning
8. Return appropriate values (lists, tuples, or single values)
9. Use quantum state notation: "|0⟩", "|1⟩", "|+⟩", "|-⟩"
10. Handle edge cases with bounds checking (e.g., if position < len(list))

STRUCTURE PATTERN:
def method_name(self, param1, param2):
    print(f"{{self.name}} is starting task...")
    # Initialize variables
    result_list = []
    counter = 0
    
    # Main logic with loops/conditions
    for item in param1:
        if condition:
            # Process and store
            result_list.append(value)
            counter += 1
    
    # Calculate statistics
    percentage = counter / total if total > 0 else 0
    print(f"Results: {{counter}}/{{total}} ({{percentage*100:.1f}}%)")
    
    return result_list
"""
            variables = """
AVAILABLE INSTANCE VARIABLES (BB84):
- self.name: Host identifier string
- self.random_bits: List of random 0/1 bits
- self.measurement_bases: List of basis choices (0 or 1)
- self.quantum_states: List of quantum state strings ("|0⟩", "|1⟩", "|+⟩", "|-⟩")
- self.received_bases: List of receiver's basis choices
- self.measurement_outcomes: List of measurement results (0 or 1)

COMMON OPERATIONS:
- Generate random bit: random.randint(0, 1)
- Choose basis: 0 for rectilinear (Z), 1 for diagonal (X)
- Encoding: basis 0: bit 0→"|0⟩", bit 1→"|1⟩" | basis 1: bit 0→"|+⟩", bit 1→"|-⟩"
- Measuring: Same basis → deterministic result, Different basis → random outcome

QUANTUM STATE ENCODING - COMMON MISTAKES TO AVOID:

❌ WRONG - Using f-strings creates invalid states:
    encoded_state = f"|{random_bit}⟩"          # Creates "|0⟩" or "|1⟩" but never diagonal states!
    encoded_state = f"|{random_bit + 1}⟩"      # Creates "|1⟩" or "|2⟩" (INVALID STATE!)
    state = f"|{bit}⟩" if basis == 0 else f"|{bit+1}⟩"  # Still WRONG!

✅ CORRECT - Use if-else with literal string values:
    if basis == 0:
        state = "|0⟩" if bit == 0 else "|1⟩"
    else:
        state = "|+⟩" if bit == 0 else "|-⟩"

VARIABLE NAMING - COMMON MISTAKES:

❌ WRONG variable names in bb84_send_qubits:
    random_bit = random.randint(0, 1)    # Should be: bit
    encoded_state = "..."                # Should be: state
    
✅ CORRECT variable names:
    bit = random.randint(0, 1)
    basis = random.randint(0, 1)
    state = "|0⟩" if ...

FINAL PRINT STATEMENT - COMMON MISTAKES:

❌ WRONG - Using variable name or "has prepared":
    print(f"{self.name} has prepared {num_qubits} qubits.")
    print(f"Prepared {len(self.quantum_states)} qubits")
    
✅ CORRECT - Use "prepared" + len():
    print(f"{self.name} prepared {len(self.quantum_states)} qubits")

===============================================================================
🔴 CRITICAL BB84_RECONCILE_BASES MANDATORY REQUIREMENTS:
===============================================================================

1. VARIABLE NAMES (MANDATORY):
   - Result list: MUST be "corresponding_bits" (NOT "bits", "matching_bits", "sifted_bits")
   - Loop variables: MUST be "i, (alice_basis, bob_basis)" (NOT "idx, (a, b)")

2. TOTAL COMPARISONS (MANDATORY):
   MUST calculate: total_comparisons = min(len(alice_bases), len(bob_bases))
   ❌ DO NOT use len(alice_bases) directly in print

3. PRINT FORMAT (MANDATORY):
   MUST use: print(f"Matches found: {{matches_found}} / {{total_comparisons}} ...")
   Where matches_found = len(matching_indices)

===============================================================================
🔴 CRITICAL BB84_ESTIMATE_ERROR_RATE MANDATORY REQUIREMENTS:
===============================================================================

1. VARIABLE NAMES (MANDATORY):
   - Loop variable for reference bits: MUST be "reference_bit" (NOT "reference", "ref", "ref_bit")
   - Loop pattern: MUST be "for position, reference_bit in zip(sample_positions, reference_bits):"

===============================================================================
🔴 CRITICAL PROCESS_RECEIVED_QBIT MANDATORY REQUIREMENTS:
===============================================================================

1. VARIABLE NAMES (MANDATORY):
   - Measurement basis variable: MUST be "basis" (NOT "measurement_basis", "meas_basis")

2. QUANTUM STATE MEASUREMENT (MANDATORY PATTERN):
   MUST use explicit if-elif for each state (NOT int() parsing):
   
   if qbit == "|0⟩":
       outcome = 0
   elif qbit == "|1⟩":
       outcome = 1
   elif qbit == "|+⟩":
       outcome = 0
   elif qbit == "|-⟩":
       outcome = 1
   else:
       outcome = random.randint(0, 1)
   
   ❌ DO NOT use: outcome = int(qbit[2])  (THIS IS WRONG!)
   ❌ DO NOT use: if qbit in ["|0⟩", "|1⟩"]: outcome = int(...)

3. MEASUREMENT LOGIC (MANDATORY):
   - If basis == 0 (rectilinear): deterministic for |0⟩/|1⟩, random for |+⟩/|-⟩
   - If basis == 1 (diagonal): deterministic for |+⟩/|-⟩, random for |0⟩/|1⟩

===============================================================================
🔴 CRITICAL BB84_SEND_QUBITS MANDATORY REQUIREMENTS - FOLLOW EXACTLY:
===============================================================================

When generating bb84_send_qubits, you MUST use these EXACT variable names and patterns:

1. VARIABLE NAMES (MANDATORY - DO NOT CHANGE):
   - Loop variable for random bit: MUST be "bit" (NOT "random_bit")
   - Loop variable for basis: MUST be "basis" (NOT "measurement_basis")
   - Loop variable for encoded state: MUST be "state" (NOT "encoded_state", "quantum_state", "encoded_qubit")
   - Instance list for bases: MUST be "self.measurement_bases" (NOT "self.bases", "self.received_bases")

2. QUANTUM STATE ENCODING (MANDATORY PATTERN):
   MUST use this exact if-else structure with string literals:
   
   if basis == 0:
       state = "|0⟩" if bit == 0 else "|1⟩"
   else:
       state = "|+⟩" if bit == 0 else "|-⟩"
   
   ❌ DO NOT use f-strings: state = f"|{{bit}}⟩"  (THIS IS WRONG!)
   ❌ DO NOT use calculations: state = f"|{{bit+1}}⟩"  (THIS IS WRONG!)
   ❌ DO NOT use ternary with f-strings (THIS IS WRONG!)

3. PRINT STATEMENTS (MANDATORY FORMAT):
   - First print: print(f"{{self.name}} is preparing {{num_qubits}} qubits.")
   - Last print: print(f"{{self.name}} prepared {{len(self.quantum_states)}} qubits")
   ❌ DO NOT use "has prepared" or "prepared {{num_qubits}}" in the final print

4. LIST INITIALIZATION (MANDATORY):
   Must clear these THREE lists at the start:
   - self.random_bits = []
   - self.measurement_bases = []  (NOT self.bases or self.received_bases!)
   - self.quantum_states = []

5. LOOP STRUCTURE (MANDATORY):
   Use: for _ in range(num_qubits):
   Generate bit and basis using: random.randint(0, 1)
   Append in this order: bit to random_bits, basis to measurement_bases, state to quantum_states
"""
            
        else:  # B92
            style_guide = """
CODING STYLE REQUIREMENTS:
1. Use 4-space indentation
2. Print informative messages with newlines: print(f"\\n{{self.name}} is doing X...")
3. Initialize/clear lists at the start of methods
4. Use if-elif-else chains for conditional logic
5. Use for loops with enumerate() for index tracking
6. Append tuples when storing multiple values: list.append((value1, value2))
7. Calculate efficiency/rates and print with percentage formatting: {{value:.2%}}
8. Print sample data: {{list[:10]}} for first 10 items
9. Use quantum state notation: '|0⟩', '|+⟩' and basis strings: "Z", "X"
10. Handle edge cases and validate inputs

STRUCTURE PATTERN:
def method_name(self, param1, param2):
    print(f"\\n{{self.name}} is starting task...")
    # Initialize variables
    result_indices = []
    result_values = []
    
    # Main logic with enumeration
    for index, (value1, value2) in enumerate(param2):
        if condition:
            # Process and accumulate
            result_indices.append(index)
            result_values.append(computed_value)
    
    # Calculate metrics
    efficiency = len(result_values) / len(param2) if len(param2) > 0 else 0
    print(f"Efficiency: {{efficiency:.2%}}")
    print(f"Sample results: {{result_values[:10]}}")
    
    return result_indices, result_values
"""
            variables = """
AVAILABLE INSTANCE VARIABLES (B92):
- self.name: Host identifier string
- self.sent_bits: List of random bits sent (0 or 1)
- self.prepared_qubits: List of prepared quantum states ('|0⟩' or '|+⟩')
- self.received_measurements: List of tuples (outcome, basis) where outcome is 0/1 and basis is "Z"/"X"
- self.sifted_key: List of sifted key bits after post-processing
- self.random_bits: Additional bit storage (if needed)
- self.measurement_outcomes: Additional outcome storage (if needed)
- self.received_bases: List of bases used during reception

COMMON OPERATIONS:
- Generate random bit: random.randint(0, 1)
- Choose random basis: random.choice(["Z", "X"])
- B92 encoding: bit 0→'|0⟩', bit 1→'|+⟩' (only 2 non-orthogonal states)
- B92 measurement: outcome 1 is conclusive, outcome 0 is inconclusive
- Sifting: Keep only conclusive results where outcome=1

B92 VALIDATION - COMMON MISTAKES:

❌ WRONG validation patterns:
    if not (0 <= bit < 2):                      # Too complex
    if bit != 0 and bit != 1:                   # Verbose
    
✅ CORRECT validation:
    if bit not in [0, 1]:
        raise ValueError(f"Invalid bit value: {bit}. Must be 0 or 1.")

===============================================================================
🔴 CRITICAL B92_SEND_QUBITS MANDATORY REQUIREMENTS:
===============================================================================

1. VARIABLE NAMES (MANDATORY):
   - Random bit variable: MUST be "random_bit" (NOT "bit")
   - Prepared qubit variable: MUST be "qubit" (NOT "prepared_qubit", "quantum_state")

2. PRINT FORMAT (MANDATORY):
   - First print: print(f"\\n{{self.name}} is preparing to send {{num_qubits}} qubits using B92 protocol...")
   - Last print: print(f"\\n{{self.name}} prepared {{num_qubits}} qubits successfully!")
   - Sample data: print(f"Random bits (first 10): {{self.sent_bits[:10]}}")

===============================================================================
🔴 CRITICAL B92_SIFTING MANDATORY REQUIREMENTS:
===============================================================================

1. VARIABLE NAMES (MANDATORY):
   - Sifted indices list: MUST be "sifted_indices" (NOT "conclusive_indices", "matching_indices")
   - Use local variable "sifted_key" in print (NOT "self.sifted_key")

2. F-STRING FORMAT (CRITICAL):
   ❌ NEVER use double braces: {{sifted_key[:10]}}  (THIS IS WRONG!)
   ✅ ALWAYS use single braces: {sifted_key[:10]}
   - print(f"Sifted key (first 10): {{sifted_key[:10]}}")  <- WRONG!
   - print(f"Sifted key (first 10): {sifted_key[:10]}")   <- CORRECT!

===============================================================================
🔴 CRITICAL B92_PREPARE_QUBIT MANDATORY REQUIREMENTS:
===============================================================================

1. VALIDATION (MANDATORY):
   MUST use: if bit not in [0, 1]:
   ❌ DO NOT use: if not (0 <= bit < 2)  (THIS IS WRONG!)

===============================================================================
🔴 CRITICAL B92_PROCESS_RECEIVED_QBIT MANDATORY REQUIREMENTS:
===============================================================================

1. MEASUREMENT CALL (MANDATORY):
   MUST call: self.b92_measure_qubit(qbit)
   ❌ DO NOT call: self.measurement()  (THIS IS WRONG!)

B92 METHOD CALLS - COMMON MISTAKES:

❌ WRONG method names:
    outcome, basis = self.measurement(qbit)     # No such method!
    
✅ CORRECT method names:
    outcome, basis = self.b92_measure_qubit(qbit)

B92 b92_send_qubits - PRINT PATTERNS:

❌ WRONG - Missing newlines or protocol name:
    print(f"{self.name} is preparing {num_qubits} qubits for transmission...")
    print(f"{self.name} has successfully prepared and sent {num_qubits} qubits!")
    print(f"First 10 transmitted bits: {self.sent_bits[:10]}")
    
✅ CORRECT - With newlines and proper labels:
    print(f"\n{self.name} is preparing to send {num_qubits} qubits using B92 protocol...")
    print(f"\n{self.name} prepared {num_qubits} qubits successfully!")
    print(f"Random bits (first 10): {self.sent_bits[:10]}")
    print(f"Prepared qubits (first 10): {self.prepared_qubits[:10]}")

B92 b92_sifting - PRINT PATTERNS:

❌ WRONG - Using double braces or wrong labels:
    print(f"First 10 bits of sifted key: {{self.sifted_key[:10]}}")  # Double braces!
    print(f"Conclusive results count: {conclusive_count}")           # Wrong var name
    print(f"Sifting efficiency: {efficiency:.2%}")                   # Should be 2f not 2%
    
✅ CORRECT - Single braces and right format:
    print(f"Sifted key (first 10): {sifted_key[:10]}")              # Local variable!
    print(f"Conclusive results: {conclusive_count}")                 
    print(f"Sifting efficiency: {sifting_efficiency:.2%}")

B92 b92_estimate_error_rate - COMPLETION MESSAGE:

❌ WRONG - Generic message:
    print(f"\n{self.name} finished calculating error rate.")
    print(f"Calculated error rate: {{error_rate:.2%}}")              # Double braces!
    
✅ CORRECT - Protocol-specific message:
    print(f"\n{self.name} B92 error rate estimation complete!")
    print(f"Calculated error rate: {error_rate:.2%}")
"""
        
        return style_guide, variables

    def answer_question(self, query: str, student_progress: int, persona_prompt: str, skeleton_code: Optional[str] = None) -> str:
        """
        Answers student questions: generates QKD code, explains concepts, or summarizes logs
        
        Args:
            query: Student's question or prompt
            student_progress: Current lesson number
            persona_prompt: System persona
            skeleton_code: Optional skeleton function to complete (e.g., "def method_name(self, param):")
        """
        query_lower = query.lower()
        
        # PRIORITY 1: Detect if this is asking for explanation/description
        explanation_keywords = [
            'explain', 'describe', 'what does', 'how does', 'why does',
            'tell me about', 'what is', 'can you explain', 'walk me through',
            'breakdown', 'help me understand', 'clarify', 'explain the',
            'describe the', 'what\'s this', 'how this', 'why this'
        ]
        is_explanation_request = any(keyword in query_lower for keyword in explanation_keywords)
        
        # PRIORITY 2: Detect explicit code generation requests
        code_generation_keywords = [
            'write', 'generate', 'implement', 'create', 'code for', 
            'method for', 'function for', 'give me code', 'show me code', 
            'need code', 'give me the', 'show me the', 'need the',
            'write a', 'create a', 'generate a', 'implement a'
        ]
        is_code_request = any(keyword in query_lower for keyword in code_generation_keywords)
        
        # If asking for explanation, NEVER generate code
        if is_explanation_request:
            is_code_request = False
        
        # If skeleton is provided, force code generation mode
        if skeleton_code:
            is_code_request = True
            is_explanation_request = False
        
        # Detect if this is a log summary request
        is_log_summary = any(keyword in query_lower for keyword in [
            'log', 'summary', 'summarize', 'analyze', 'what happened'
        ]) and 'error' not in query_lower  # Don't confuse with error_rate code requests
        
        # Detect protocol
        is_bb84 = 'bb84' in query_lower or 'studentquantumhost' in query_lower
        is_b92 = 'b92' in query_lower or 'studentb92host' in query_lower
        protocol = 'BB84' if is_bb84 else 'B92' if is_b92 else 'BB84'
        
        if is_code_request:
            # Get protocol-specific guidelines
            style_guide, variables = self._get_protocol_guidelines(protocol)
            
            if skeleton_code:
                # Use skeleton function to complete the code
                prompt = f"""You are a Python code generator for quantum key distribution protocols.

CRITICAL OUTPUT RULES:
1. OUTPUT ONLY THE COMPLETED METHOD CODE - NO EXPLANATIONS, NO MARKDOWN, NO TAGS
2. Keep the EXACT skeleton function signature provided
3. Fill in the method body based on the prompt
4. End with the return statement - nothing after
5. NO text before or after the method definition
6. FOLLOW THE EXACT CODE PATTERNS AND VARIABLE NAMES specified below

ABSOLUTELY FORBIDDEN:
- No ``` or markdown blocks
- No [PYTHON], [CODE], or any XML/bracket tags  
- No "Here's the code" or "This method does..." explanations
- No test cases or example usage after the method
- No class definitions
- No explanatory comments outside the method body
- NO double braces {{}} in f-strings (use single braces {{}})
- NO f-string interpolation for quantum states (use if-else with string literals)

{style_guide}

{variables}

PROTOCOL: {protocol}

🚨 ABSOLUTELY CRITICAL REQUIREMENTS - READ CAREFULLY:
1. Use ONLY the exact variable names specified in the "MANDATORY REQUIREMENTS" section above
2. For bb84_send_qubits: Use "bit", "basis", "state" (NOT random_bit, encoded_state, etc.)
3. For quantum encoding: Use if-else with string literals (NOT f-strings like f"|{{bit}}⟩")
4. For instance lists: Use "self.measurement_bases" (NOT self.bases or self.received_bases)
5. DO NOT improvise or change any variable names from what is specified
6. FOLLOW THE EXACT encoding pattern shown: if basis == 0: state = "|0⟩" if bit == 0 else "|1⟩"

SKELETON FUNCTION TO COMPLETE:
{skeleton_code}

STUDENT'S PROMPT: {query}

Generate code that STRICTLY follows ALL the mandatory requirements above.
Output ONLY the completed method starting with "def" and ending with "return":"""
            else:
                # Generate method from scratch
                prompt = f"""You are a Python code generator for quantum key distribution protocols.

CRITICAL OUTPUT RULES:
1. OUTPUT ONLY THE METHOD CODE - NO EXPLANATIONS, NO MARKDOWN, NO TAGS
2. Start directly with "def method_name(self, ...):"
3. End with the return statement - nothing after
4. NO text before or after the method definition
5. FOLLOW THE EXACT CODE PATTERNS AND VARIABLE NAMES specified below

ABSOLUTELY FORBIDDEN:
- No ``` or markdown blocks
- No [PYTHON], [CODE], or any XML/bracket tags  
- No "Here's the code" or "This method does..." explanations
- No test cases or example usage after the method
- No class definitions
- No explanatory comments outside the method body
- NO double braces {{}} in f-strings (use single braces {{}})
- NO f-string interpolation for quantum states (use if-else with string literals)

{style_guide}

{variables}

PROTOCOL: {protocol}

🚨 ABSOLUTELY CRITICAL REQUIREMENTS - READ CAREFULLY:
1. Use ONLY the exact variable names specified in the "MANDATORY REQUIREMENTS" section above
2. For bb84_send_qubits: Use "bit", "basis", "state" (NOT random_bit, encoded_state, etc.)
3. For quantum encoding: Use if-else with string literals (NOT f-strings like f"|{{bit}}⟩")
4. For instance lists: Use "self.measurement_bases" (NOT self.bases or self.received_bases)
5. DO NOT improvise or change any variable names from what is specified
6. FOLLOW THE EXACT encoding pattern shown: if basis == 0: state = "|0⟩" if bit == 0 else "|1⟩"

STUDENT'S REQUEST: {query}

Generate code that STRICTLY follows ALL the mandatory requirements above.
Output ONLY the method definition starting with "def" and ending with "return":"""
            
        elif is_log_summary:
            # Log analysis mode
            prompt = f"""You are a quantum network simulation expert analyzing QKD protocol execution logs.

Provide a structured analysis covering:
1. Protocol identified (BB84 or B92)
2. Qubit transmission (how many sent/received)
3. Basis reconciliation or sifting results
4. Error rate calculation
5. Security assessment
6. Any anomalies or issues detected

Student's log query: {query}

Analysis:"""
            
        else:
            # Explanation mode with optional RAG context
            context_chunks = self.db_manager.search_with_filter(
                query=query, max_lesson_number=student_progress, num_results=3
            )
            context_str = "\n\n".join(context_chunks)

            if context_str:
                prompt = f"""{persona_prompt}

Relevant course materials:
---
{context_str}
---

Student question: {query}

Provide a clear, friendly explanation (2-4 paragraphs). Use simple language and analogies where helpful:"""
            else:
                prompt = f"""{persona_prompt}

Student question: {query}

Provide a clear, friendly explanation (2-4 paragraphs) based on quantum key distribution concepts:"""
        
        # Get response from Ollama
        response = self._call_ollama_llm(prompt)
        
        # Format code output if this is a code request
        if is_code_request:
            response = self._format_code_output(response)
            # Format as clean code block without extra notes
            response = "```python\n" + response + "\n```"
        
        return response

class PeerAgentUI:
    """
    Creates and manages the ipywidgets UI for the Peer Agent in a Jupyter Notebook.
    This is the main entry point to be used in the notebook.
    """
    def __init__(self, 
                 db_path: str = "./faiss_course_db",
                 persona_file: str = "student-peer-persona.md",
                 progress_file: str = "student_progress.json",
                 ollama_embed_model: str = 'nomic-embed-text',
                 ollama_chat_model: str = 'codellama:7b'):
        """Initializes the UI and the backend agent."""
        self.progress_file = progress_file
        self.learning_pointer = self._get_student_progress()
        self.persona_prompt = self._load_persona(persona_file)
        
        try:
            self.agent = PeerAgent(
                db_path=db_path,
                ollama_embed_model=ollama_embed_model,
                ollama_chat_model=ollama_chat_model
            )
        except Exception as e:
            print(f"Error initializing Peer Agent backend: {e}")
            self.agent = None
            
        self._create_ui_layout()

    def _get_student_progress(self) -> int:
        """Loads the student's current lesson number."""
        if not os.path.exists(self.progress_file):
            return 1
        try:
            with open(self.progress_file, 'r') as f:
                return json.load(f).get("current_lesson", 1)
        except (json.JSONDecodeError, FileNotFoundError):
            return 1
            
    def _load_persona(self, filepath: str) -> str:
        """Loads the persona prompt from a file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Warning: Persona file not found at {filepath}. Using a default persona.")
            return "You are a helpful quantum cryptography peer tutor. Explain concepts clearly using quantum notation. When generating code, produce clean, working implementations that match the student's coding style. Be encouraging and precise with technical details."

    def _create_ui_layout(self):
        """Creates and styles all the ipywidgets for a more immersive UI."""
        
        intro_html = widgets.HTML(
            value=f"""
            <div style="line-height: 1.5;">
                Hey there! 👋 Looks like we're both on <b>Lesson {self.learning_pointer}</b>.
                <br>
                If you're stuck on anything from this lesson or the ones before, just ask me below. 
                I'll check my notes and we can try to figure it out together. 
                <br>
                <b>💡 Tip:</b> Ask "write [method name]" for code, or "explain [concept]" for help understanding! 😄
            </div>
            """
        )

        self.question_area = widgets.Textarea(
            value='',
            placeholder="Try: 'write bb84_send_qubits method' or 'explain how BB84 works'",
            layout=widgets.Layout(width='98%', height='90px')
        )

        self.submit_button = widgets.Button(
            description="Let's figure it out!",
            button_style='success',
            tooltip="Ask me your question",
            icon='code',
            layout=widgets.Layout(width='200px', height='auto')
        )

        self.output_area = widgets.Output(
            layout=widgets.Layout(padding='10px', border='1px solid #fafafa', min_height='80px')
        )
        
        self.submit_button.on_click(self._on_button_clicked)

        self.ui_container = widgets.VBox([
            intro_html,
            self.question_area,
            self.submit_button,
            self.output_area
        ], layout=widgets.Layout(
            display='flex',
            flex_flow='column',
            align_items='flex-start',
            border='2px solid #66c2a5',
            padding='15px',
            margin='10px 0 0 0',
            border_radius='10px',
            width='95%'
        ))

    def _on_button_clicked(self, b):
        """Handles the button click event."""
        with self.output_area:
            self.output_area.clear_output()
            query = self.question_area.value
            
            if not query.strip():
                display(Markdown("<i>Oops, looks like you forgot to type a question!</i>"))
                return
            if not self.agent:
                display(Markdown("<b>Oh no! It seems like my 'brain' isn't working right now. Please check the setup errors above.</b>"))
                return
            
            self.submit_button.disabled = True
            self.submit_button.description = 'Thinking...'
            self.submit_button.icon = 'spinner'
            
            response = self.agent.answer_question(query, self.learning_pointer, self.persona_prompt)
            
            display(Markdown(response))
            
            self.submit_button.disabled = False
            self.submit_button.description = "Let's figure it out!"
            self.submit_button.icon = 'code'

    def display_ui(self):
        """Renders the complete UI in the notebook."""
        display(self.ui_container)


# Example usage:
# peer_agent = PeerAgentUI()
# peer_agent.display_ui()
