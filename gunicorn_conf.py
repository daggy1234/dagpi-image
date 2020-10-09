import multiprocessing
import os

host = os.getenv("HOST", "0.0.0.0")
port = os.getenv("PORT", "5000")

print("Initialising Gunicorn Vars")

loglevel = "info"
workers = f"{multiprocessing.cpu_count() * 1}"
bind = f"{host}:{port}"
worker_tmp_dir = "/dev/shm"
graceful_timeout = 120
timeout = 120
keepalive = 5
accesslog = "-"
errorlog = "-"

print(
    f"\nStarting With the Following:\nPORT: {bind}\nHOST: {host}\nWORKERS: {workers}\n")
