import json
import sys
import os

from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado

from .v_db.peer_agent import PeerAgent

# Add project root to path to import firebase_manager and notebook_tracker
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Initialize Firebase when extension loads
try:
    import firebase_manager
    firebase_manager.init_firebase()
    print("[AI Agent Extension] Firebase initialized successfully")
except Exception as e:
    print(f"[AI Agent Extension] Warning: Firebase initialization failed: {e}")
    print("[AI Agent Extension] AI interactions will not be logged to Firebase")

class AskAgentHandler(APIHandler):
    """
    The handler that listens for API calls from the React front-end.
    """
    
    def __init__(self, application, request, **kwargs):
        resp = super().__init__(application, request, **kwargs)
        self.peer_agent = PeerAgent(
            db_path='data/vector_db'
        )
        return resp

    @tornado.web.authenticated
    def post(self):
        """
        Handles POST requests to /q-toolkit/ask
        """
        try:
            # 1. Get the incoming request body (the student's question)
            data = self.get_json_body()
            query = data.get("query")
            agent_type = data.get("agent_type", "peer") # e.g., 'peer' or 'tutor'
            
            if not query:
                raise ValueError("No query provided")

            # Process student query for QKD code generation or log analysis
            print(f"Received query for {agent_type}: {query}")
            
            qkd_persona = """You are an expert quantum cryptography teaching assistant specializing in BB84 and B92 protocols. 

Your capabilities:
1. Generate clean, production-ready Python code for QKD methods
2. Explain quantum concepts using proper notation (|0⟩, |1⟩, |+⟩, |-⟩)
3. Analyze simulation logs and identify issues
4. Help students debug their implementations

When generating code:
- Use StudentQuantumHost for BB84
- Use StudentB92Host for B92
- Include proper error handling
- Add detailed comments
- Return working, tested code

Be precise with technical details but maintain an encouraging, educational tone."""
            
            # Detect protocol and request type before generating response
            query_lower = query.lower()
            is_bb84 = 'bb84' in query_lower or 'studentquantumhost' in query_lower
            is_b92 = 'b92' in query_lower or 'studentb92host' in query_lower
            protocol = 'BB84' if is_bb84 else 'B92' if is_b92 else 'BB84'
            
            explanation_keywords = ['explain', 'describe', 'what does', 'how does', 'why does', 'tell me about']
            is_explanation = any(keyword in query_lower for keyword in explanation_keywords)
            
            code_keywords = ['write', 'generate', 'implement', 'create', 'code for', 'method for']
            is_code_request = any(keyword in query_lower for keyword in code_keywords) and not is_explanation
            
            # Extract skeleton code if present (pattern: "def method_name...")
            skeleton_code = None
            if is_code_request and 'def ' in query:
                # Try to extract the skeleton function from the query
                import re
                skeleton_match = re.search(r'def\s+\w+\s*\([^)]*\)[:\s]*', query)
                if skeleton_match:
                    skeleton_code = skeleton_match.group(0).strip()
            
            # Generate response
            answer = self.peer_agent.answer_question(query, 1, qkd_persona, skeleton_code=skeleton_code)

            # Log AI interaction to Firebase
            try:
                import firebase_manager
                import os
                
                # Read tracking state from file (written by notebook when student_id is initialized)
                tracking_state_file = os.path.join(project_root, '.tracking_state.json')
                
                student_id = None
                session_id = None
                
                if os.path.exists(tracking_state_file):
                    try:
                        with open(tracking_state_file, 'r') as f:
                            tracking_state = json.load(f)
                            if tracking_state.get('initialized'):
                                student_id = tracking_state.get('student_id')
                                session_id = tracking_state.get('session_id')
                                print(f"\n[AI Tracking] Using student: {student_id}, session: {session_id}")
                    except Exception as e:
                        print(f"[AI Tracking] Warning: Could not read tracking state: {e}")
                
                if not student_id or not session_id:
                    print(f"\n[AI Tracking] WARNING: Student not initialized yet")
                    print(f"[AI Tracking] AI interactions will NOT be logged to Firebase")
                    print(f"[AI Tracking] Please run the notebook setup cell first")
                else:
                    # Log the interaction to Firebase
                    print(f"\n[AI Tracking] Logging interaction to Firebase...")
                    result = firebase_manager.log_ai_interaction(
                        student_id=student_id,
                        session_id=session_id,
                        query=query,
                        response=answer,
                        protocol=protocol,
                        was_code_request=is_code_request,
                        was_explanation=is_explanation
                    )
                    
                    if result:
                        print(f"[AI Tracking] Successfully logged: {result}")
                    else:
                        print("[AI Tracking] Failed to log (check Firebase credentials)")
                    
            except Exception as e:
                print(f"[AI Tracking] ERROR: {e}")
                import traceback
                traceback.print_exc()

            # 3. Send the response back to the front-end
            self.finish(json.dumps({
                "data": answer
            }))

        except Exception as e:
            import traceback
            error_details = {
                "error": str(e),
                "type": type(e).__name__,
                "traceback": traceback.format_exc()
            }
            print(f"[ERROR] Handler exception: {error_details}")
            self.set_status(500)
            self.finish(json.dumps({
                "message": f"Error: {str(e)}",
                "reason": type(e).__name__,
                "traceback": traceback.format_exc()
            }))

def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    # The URL your front-end will call: /q-toolkit/ask
    route_pattern = url_path_join(base_url, "q-toolkit", "ask")
    
    handlers = [(route_pattern, AskAgentHandler)]
    web_app.add_handlers(host_pattern, handlers)
