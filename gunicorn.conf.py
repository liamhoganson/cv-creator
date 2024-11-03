bind = '0.0.0.0:8080'
backlog = 2048
workers = 2
worker_class = 'sync' #TODO: Use async workers for the API requests
worker_connections = 1000
timeout = 30
keepalive = 2
spew = False
