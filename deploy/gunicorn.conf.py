"""
Gunicorn configuration for JustBaddo production application server.
"""

import multiprocessing
import os

# Server socket
bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:8000')
backlog = 2048

# Worker processes: recommended rule is (2 * CPU cores) + 1
workers = int(os.environ.get('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'gthread'
threads = int(os.environ.get('GUNICORN_THREADS', 4))
worker_connections = 1000
timeout = int(os.environ.get('GUNICORN_TIMEOUT', 60))
keepalive = 5

# Process naming
proc_name = 'justbaddo_gunicorn'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Logging
accesslog = '-'  # standard output for container/systemd logging
errorlog = '-'   # standard error
loglevel = os.environ.get('GUNICORN_LOG_LEVEL', 'info')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)sµs'

# Lifecycle hooks
def on_starting(server):
    server.log.info("Starting JustBaddo Gunicorn application server...")

def when_ready(server):
    server.log.info("JustBaddo WSGI server is ready to accept HTTP connections.")
