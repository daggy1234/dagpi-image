import os

import uvicorn
from concurrent.futures import ProcessPoolExecutor

host: str = os.getenv("HOST", "127.0.0.1")
port: int = int(os.getenv("PORT", 5000))

if __name__ == "__main__":
    print("Executors baby")
    print("Ready to run app")
    uvicorn.run("app:app", host=host, port=port, log_level="info")
