import multiprocessing, os

workers = int((multiprocessing.cpu_count() * 2) + 1)
bind = "0.0.0.0:8000"
timeout = 30
graceful_timeout = 30
loglevel = "info"

# Write to files on the shared volume
accesslog = "/logs/app/gunicorn.access.log"
errorlog  = "/logs/app/gunicorn.error.log"

# Optional: if you previously set this to "-", remove it so file logging is used
# accesslog = "-"
# errorlog  = "-"

# Temp dir tweak still fine
worker_tmp_dir = "/dev/shm"
