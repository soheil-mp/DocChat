from prometheus_client import Counter, Histogram
import time

request_count = Counter('http_requests_total', 'Total HTTP requests')
response_time = Histogram('http_response_time_seconds', 'HTTP response time')

class MetricsMiddleware:
    async def __call__(self, request, call_next):
        request_count.inc()
        start_time = time.time()
        response = await call_next(request)
        response_time.observe(time.time() - start_time)
        return response 