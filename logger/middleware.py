import time

from logger.models import Log


class LoggerMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        diff = time.time() - start
        if not request.path.startswith('/admin'):
            log = Log(path=request.path, method=request.method, execution_time_sec=diff)
            log.save()
        return response
