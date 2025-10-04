# gunicorn.conf.py
workers = 2
worker_class = 'sync'
worker_connections = 1000
timeout = 120
keepalive = 5