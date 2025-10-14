import os
import sys
import pathlib

# Set up environment variables BEFORE any imports
os.environ["REDIS_HOST"] = "localhost"
os.environ["REDIS_PORT"] = "6379"
os.environ["REDIS_USERNAME"] = "default"
os.environ["REDIS_PASSWORD"] = ""
os.environ["REDIS_DB"] = "0"
os.environ["REDIS_SSL"] = "false"
os.environ["REDIS_OM_URL"] = "redis://localhost:6379/0"

# Fix Python path for data.models imports
ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

# Set up Redis with fallback to file storage

# Disable only problematic features, keep topology storage
os.environ["DISABLE_EMBEDDING"] = "1"
os.environ["DISABLE_AI_FEATURES"] = "1"
os.environ["DISABLE_REDIS_LOGGING"] = "1"

# Clear config cache to force reload with new environment variables
from config.config import clear_config_cache
clear_config_cache()

# Try to clear Redis memory if it's full (silent cleanup)
try:
    import redis
    r = redis.Redis(
        host=os.environ["REDIS_HOST"],
        port=int(os.environ["REDIS_PORT"]),
        username=os.environ["REDIS_USERNAME"],
        password=os.environ["REDIS_PASSWORD"],
        db=int(os.environ["REDIS_DB"]),
        ssl=os.environ["REDIS_SSL"].lower() == "true"
    )
    # Clear only log-related keys to free memory
    log_keys = r.keys("network-sim:log:*")
    if log_keys:
        r.delete(*log_keys)
except Exception as e:
    pass  # Silent fail
os.environ["GOOGLE_API_KEY"] = "Use your API key here"
os.environ["OPENAI_API_KEY"] = os.environ["GOOGLE_API_KEY"]
os.environ["LANGCHAIN_API_KEY"] = os.environ["GOOGLE_API_KEY"]
# Disable embedding to prevent Redis memory issues
os.environ["DISABLE_EMBEDDING"] = "1"

# Replace flask.cli.load_dotenv with python-dotenv
try:
    from dotenv import load_dotenv
    if not load_dotenv():
        print("Warning: .env file not found, using environment variables set above")
except ImportError:
    print("python-dotenv not installed, using environment variables set above")
import traceback
from fastapi import FastAPI
from server.app import get_app
from fastapi.concurrency import asynccontextmanager

app = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Check if student implementation is ready
    try:
        import json
        status_file = "student_implementation_status.json"
        if os.path.exists(status_file):
            with open(status_file, 'r') as f:
                status = json.load(f)
            protocol = status.get("current_protocol", "BB84").upper()
            if status.get("student_implementation_ready", False):
                print(f"Student {protocol} implementation detected and ready")
            else:
                print(f"Student {protocol} implementation not ready")
    except Exception as e:
        pass  # Silent fail

    yield
    # Shutdown (silent)

app = get_app(lifespan=lifespan)

if __name__ == '__main__':
    try:
        host = os.getenv("HOST", "0.0.0.0")
        port = int(os.getenv("PORT", "8080"))  # Binder uses PORT env var
        reload_flag = os.getenv("DEBUG", "True").lower() in ["true", "1", "t"]
        
        # Enable CORS for frontend
        from fastapi.middleware.cors import CORSMiddleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                "http://localhost:3000",  # Frontend dev server
                "http://127.0.0.1:3000",
                "http://localhost:8080",  # Binder backend server
                "http://127.0.0.1:8080",
                "*",  # Allow all origins for Binder
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        print(f"Starting backend server on http://{host}:{port}")
        print("Make sure to start the frontend with 'npm run dev' in the ui directory")
        
        import uvicorn
        uvicorn.run(
            "start:app",
            host=host,
            port=port,
            reload=reload_flag
        )
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print(f"Server started on {host}:{port} with reload={reload_flag}")
