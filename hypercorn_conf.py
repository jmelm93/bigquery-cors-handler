import json
import multiprocessing
import os

# https://github.com/cormorack/hypercorn-docker/blob/main/docker-images/hypercorn_conf.py


host = os.getenv("HOST", "0.0.0.0")
port = os.getenv("PORT", "8080")
# port = os.getenv("PORT", "8001")

bind_env = os.getenv("BIND", None)
use_loglevel = os.getenv("LOG_LEVEL", "info")

if bind_env:
    use_bind = bind_env
else:
    use_bind = f"{host}:{port}"

cores = multiprocessing.cpu_count()

accesslog_var = os.getenv("ACCESS_LOG", "-")
use_accesslog = accesslog_var or None
errorlog_var = os.getenv("ERROR_LOG", "-")
use_errorlog = errorlog_var or None
graceful_timeout_str = os.getenv("GRACEFUL_TIMEOUT", "120")
keepalive_str = os.getenv("KEEP_ALIVE", "1800") # 30 minutes

# Hypercorn config variables
loglevel = use_loglevel
bind = use_bind
errorlog = use_errorlog
accesslog = use_accesslog
graceful_timeout = int(graceful_timeout_str)
keep_alive_timeout = int(keepalive_str)
# access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# For debugging and testing
log_data = {
    "loglevel": loglevel,
    # "workers": workers,
    # "worker_class": worker_class,
    "bind": bind,
    "graceful_timeout": graceful_timeout,
    "keepalive": keep_alive_timeout,
    "errorlog": errorlog,
    "accesslog": accesslog,
    # "access_log_format": access_log_format,
    # Additional, non-hypercorn variables
    # "workers_per_core": workers_per_core,
    # "use_max_workers": use_max_workers,
    "host": host,
    "port": port,
}

print(json.dumps(log_data))