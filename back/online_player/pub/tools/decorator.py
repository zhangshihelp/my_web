import logging
import time
from functools import update_wrapper

from django.core.handlers.wsgi import WSGIRequest
from rest_framework.request import Request

from online_player.pub.tools.http import get_http_head_param

log = logging.getLogger('time')


def time_calc(func):
    def wrapper(*args, **kwargs):
        user = None
        path = None
        method = None
        for arg in args:
            if isinstance(arg, Request) or isinstance(arg, WSGIRequest):
                user = get_http_head_param(arg, 'user', log)
                path = arg.path
                method = arg.method
                break
        start = time.time()
        result = func(*args, **kwargs)
        duration = float((time.time() - start) * 1000)
        if user:
            log.info('user: %s, request url: %s, method: %s, %s %s, time: %.2f ms' % (
                user, path, method, func.__module__, str(func).split(' ')[1], duration))
        else:
            log.info('%s %s, time: %.2f ms' % (func.__module__, str(func).split(' ')[1], duration))
        return result
    return update_wrapper(wrapper, func)
