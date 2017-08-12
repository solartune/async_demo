from multiprocessing import cpu_count

bind = '0.0.0.0:8000'
workers = cpu_count() * 2 + 1
max_requests = 1000
worker_class = 'aiohttp.GunicornWebWorker'
