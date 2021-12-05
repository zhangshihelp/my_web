from rest_framework.response import Response

from online_player.pub.error.error_code import get_error_code
from online_player.pub.error.error_code_info import get_error_msg, get_error_advice


class OnlinePlayerResponse(Response):
    def __init__(self, data=None, status=None, http_status=None, error_head=None, error=None, extra=None, language='zh', template_name=None, headers=None,
                 exception=None, content_type=None):
        errors = None
        if error_head and error:
            errors = [error_head[0], error_head[1], error]
        context = {
            'status': status,
            'error_code': get_error_code(errors),
            'error_msg': get_error_msg(language, errors, *extra) if extra else get_error_msg(language, errors),
            'advice_msg': get_error_advice(language, errors, *extra) if extra else get_error_advice(language, errors),
            'data': data
        }

        super().__init__(data=context, status=http_status, template_name=template_name, headers=headers, exception=exception, content_type=content_type)

        self['Access-Control-Allow-Origin'] = '*'
        self['Access-Control-Allow-Methods'] = 'POST, DELETE, PUT, GET, OPTIONS'
        self['Access-Control-Max-Age'] = '1000'
        self['Access-Control-Allow-Headers'] = '*'
