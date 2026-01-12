"""
Run the FastAPI server
"""

import uvicorn
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables from project root
env_path = project_root / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    load_dotenv()

if __name__ == "__main__":
    # Change to project root directory
    os.chdir(project_root)
    
    uvicorn.run(
        "api.main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=True,  # Enable auto-reload for development
        reload_dirs=[str(project_root)]  # Watch project root for changes
    )
