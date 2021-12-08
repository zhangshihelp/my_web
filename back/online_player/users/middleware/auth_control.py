import logging
import re

from django.utils.deprecation import MiddlewareMixin
from rest_framework import status

from online_player.pub.error.error_code import access, ErrorAccessLeaf
from online_player.pub.response.common_response import JSONResponse
from online_player.pub.tools.decorator import time_calc
from online_player.pub.tools.http import get_http_head_param
from online_player.users.middleware.auth_setting import USER_AUTH_SETTING

log = logging.getLogger('users')


class AuthMiddleware(MiddlewareMixin):

    @time_calc
    def process_request(self, request):
        path = request.path
        method = request.method
        is_permission = request_is_permission(path, method)
        if is_permission:
            headers = get_headers_dict(request)
            allow = False
            if not headers.get('token') or not headers.get('account'):
                return JSONResponse(status=False, error_head=access, error=ErrorAccessLeaf.DENIED, http_status=status.HTTP_400_BAD_REQUEST,
                                    language=headers.get('language'))


def request_is_permission(path, method):
    """
    判断请求是否被权限控制起来
    :param path: 请求的路由
    :param method: 请求的方法
    :return: 如果路由和方法均满足权限控制，则返回True
    """
    url_permission = method_permission = True
    permission_dict = USER_AUTH_SETTING.get('visitor')
    for k, v in permission_dict.items():
        if re.match(k, path):
            url_permission = False
            if method in v:
                method_permission = False
        if not url_permission and not method_permission:
            return False
    return True


def get_headers_dict(request):
    """
    获取header里面的用户信息
    :param request: 请求对象
    :return: 用户信息字典
    """
    token = get_http_head_param(request, 'authorization', log)
    language = get_http_head_param(request, 'language', log)
    account = get_http_head_param(request, 'user', log)
    role = get_http_head_param(request, 'role', log)
    return {
        'token': token,
        'language': language,
        'account': account,
        'role': role,
    }
