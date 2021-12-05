from logging import Logger
from urllib.parse import unquote

from rest_framework.request import Request


def get_http_head_param(request: Request, param: str, log: Logger):
    try:
        param = 'HTTP_' + param.upper()
        return unquote(request.META.get(param))
    except Exception as e:
        log.warning(e)
