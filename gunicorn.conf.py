"""
Production Gunicorn Configuration for Konkan Guide Django Application.
"""

import os
import multiprocessing

# Network Binding
bind = os.environ.get("GUNICORN_BIND", "0.0.0.0:8000")

# Worker & Thread Concurrency
# Default: 2-3 workers with 2 threads per worker for I/O bound web workloads
default_workers = max(2, min(4, multiprocessing.cpu_count() * 2 + 1))
workers = int(os.environ.get("GUNICORN_WORKERS", default_workers))
threads = int(os.environ.get("GUNICORN_THREADS", 2))
worker_class = "gthread"
worker_connections = 1000

# Timeouts & Keep-Alive
timeout = int(os.environ.get("GUNICORN_TIMEOUT", 60))
graceful_timeout = int(os.environ.get("GUNICORN_GRACEFUL_TIMEOUT", 30))
keepalive = int(os.environ.get("GUNICORN_KEEPALIVE", 5))

# Memory Protection (Restart workers periodically with jitter to avoid simultaneous restarts)
max_requests = int(os.environ.get("GUNICORN_MAX_REQUESTS", 1200))
max_requests_jitter = int(os.environ.get("GUNICORN_MAX_REQUESTS_JITTER", 60))

# Logging to standard output/error (container-friendly)
accesslog = "-"
errorlog = "-"
loglevel = os.environ.get("GUNICORN_LOG_LEVEL", "info")
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" (%(D)s µs)'
capture_output = True

# Process naming
proc_name = "konkan_django"
