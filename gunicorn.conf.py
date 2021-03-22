import multiprocessing

name = "fastapi-basic"
bind = "0.0.0.0:4000"
workers = multiprocessing.cpu_count() * 2 + 1
reload = False
worker_connections = 1000 * workers
worker_class = "uvicorn.workers.UvicornWorker"
loglevel = "info"
accesslog = "logs/gunicorn-access.log"

max_requests = 1000
max_requests_jitter = 50
