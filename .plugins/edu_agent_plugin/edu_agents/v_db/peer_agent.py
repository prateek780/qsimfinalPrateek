import requests
import json
import os
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
        """Clean and format code output for easy copy-paste with line-by-line structure."""
        import re
        
        cleaned = raw_output.strip()
        
        # Step 1: Remove markdown code blocks
        cleaned = re.sub(r'```python\n?', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'```\n?', '', cleaned, flags=re.IGNORECASE)
        
        # Step 2: Remove ALL bracketed tags and XML-style tags
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
        
        # Step 3: Split into lines and find code boundaries
        lines = cleaned.split('\n')
        code_start_idx = -1
        code_end_idx = len(lines)
        
        # Find where code starts (first 'def')
        for i, line in enumerate(lines):
            stripped = line.strip()
            # Skip explanatory lines before code
            if any(phrase in stripped.lower() for phrase in [
                "here is", "here's", "this code", "this method", 
                "the following", "below is", "i've created"
            ]):
                continue
            if stripped.startswith('def '):
                code_start_idx = i
                break
        
        if code_start_idx == -1:
            return cleaned.strip()
        
        # Extract from the def line onwards
        lines = lines[code_start_idx:]
        
        # Step 4: Extract ONLY the method definition (stop at explanatory text)
        method_lines = []
        base_indent = None
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # First line should be def
            if i == 0:
                if not stripped.startswith('def '):
                    continue
                method_lines.append(line)
                base_indent = len(line) - len(line.lstrip())
                continue
            
            # Stop at explanatory text after the method
            if stripped and not line.startswith(' ' * (base_indent + 1)) and base_indent is not None:
                # This line is not indented under the method
                if not stripped.startswith('def '):
                    # It's explanatory text, stop here
                    break
            
            # Stop at common explanatory phrases
            if any(phrase in stripped.lower() for phrase in [
                'this method', 'this function', 'the above', 'note that',
                'you can use', 'example usage', 'to use this'
            ]):
                break
            
            # Stop at test cases, assertions, examples
            if any(keyword in stripped.lower() for keyword in [
                '# test', '# example', '# usage', 'assert ', 
                'if __name__', 'print("test'
            ]):
                break
            
            # Stop at next method or class
            if stripped.startswith('def ') or stripped.startswith('class '):
                break
            
            method_lines.append(line)
        
        # Step 5: Clean up trailing empty lines
        while method_lines and not method_lines[-1].strip():
            method_lines.pop()
        
        if not method_lines:
            return cleaned.strip()
        
        # Step 6: Join and format
        result = '\n'.join(method_lines)
        
        # Ensure consistent spacing (max 1 blank line between sections)
        while '\n\n\n' in result:
            result = result.replace('\n\n\n', '\n\n')
        
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

COMMON OPERATIONS:
- Generate random bit: random.randint(0, 1)
- Choose random basis: random.choice(["Z", "X"])
- B92 encoding: bit 0→'|0⟩', bit 1→'|+⟩' (only 2 non-orthogonal states)
- B92 measurement: outcome 1 is conclusive, outcome 0 is inconclusive
- Sifting: Keep only conclusive results where outcome=1
"""
        
        return style_guide, variables

    def answer_question(self, query: str, student_progress: int, persona_prompt: str) -> str:
        """
        Answers student questions: generates QKD code, explains concepts, or summarizes logs
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
            
            # Enhanced prompt for better code generation with guidelines instead of examples
            prompt = f"""You are a Python code generator for quantum key distribution protocols.

CRITICAL OUTPUT RULES:
1. OUTPUT ONLY THE METHOD CODE - NO EXPLANATIONS, NO MARKDOWN, NO TAGS
2. Start directly with "def method_name(self, ...):"
3. End with the return statement - nothing after
4. NO text before or after the method definition

ABSOLUTELY FORBIDDEN:
- No ``` or markdown blocks
- No [PYTHON], [CODE], or any XML/bracket tags  
- No "Here's the code" or "This method does..." explanations
- No test cases or example usage after the method
- No class definitions
- No explanatory comments outside the method body

{style_guide}

{variables}

PROTOCOL: {protocol}

STUDENT'S REQUEST: {query}

Based on the style guidelines and available variables above, generate a clean, working method.
Remember: Output ONLY the method definition starting with "def" and ending with "return":"""
            
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
