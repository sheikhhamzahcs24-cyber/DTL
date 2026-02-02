import os
import sys

# Add backend to path so imports work
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

try:
    from main import app
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

