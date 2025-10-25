import uvicorn
import os
from app import score_app

if __name__ == "__main__":
    uvicorn.run(score_app, host="127.0.0.1", port=8040, log_level="info")