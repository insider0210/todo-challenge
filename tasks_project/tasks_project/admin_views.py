from django.http import HttpResponse
import logging


logger = logging.getLogger(__name__)


def status_index(request):
    logger.info('Se accedio al index para la verificacion del estado del servidor')
    return HttpResponse('<h3>Server runing ✔️</h3>')