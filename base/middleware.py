from .models import RequestLog
from django.utils.timezone import now
import logging

logger = logging.getLogger(__name__)

class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        method = request.method
        path = request.get_full_path()
        user = request.user if request.user.is_authenticated else None

        logger.info(f"{method} request made to {path}")

        RequestLog.objects.create(
            method=method,
            path=path,
            created_by=user,
            created_date=now()
        )

        return self.get_response(request)

