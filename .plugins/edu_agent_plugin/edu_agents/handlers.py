import json

from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado

from .v_db.peer_agent import PeerAgent

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
            
            answer = self.peer_agent.answer_question(query, 1, qkd_persona)

            # 3. Send the response back to the front-end
            self.finish(json.dumps({
                "data": answer
            }))

        except Exception as e:
            self.set_status(500)
            self.finish(json.dumps({"error": str(e)}))

def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    # The URL your front-end will call: /q-toolkit/ask
    route_pattern = url_path_join(base_url, "q-toolkit", "ask")
    
    handlers = [(route_pattern, AskAgentHandler)]
    web_app.add_handlers(host_pattern, handlers)
