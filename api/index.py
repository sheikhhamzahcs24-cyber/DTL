import os
import sys

# Add project root AND backend dir to sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(root_dir, 'backend')
sys.path.append(root_dir)
sys.path.append(backend_dir)

try:
    from backend.main import app
except Exception as e:
    import traceback
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    
    app = FastAPI()
    
    @app.get("/{path:path}")
    async def catch_all(path: str):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Backend Import Failed",
                "message": str(e),
                "traceback": traceback.format_exc(),
                "cwd": os.getcwd(),
                "path": sys.path
            }
        )

