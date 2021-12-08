import logging
import re

from django.utils.deprecation import MiddlewareMixin
from rest_framework import status

from online_player.pub.const.user_const import UserConst
from online_player.pub.error.error_code import access, ErrorAccessLeaf, system, ErrorServerLeaf
from online_player.pub.exception.user import UserNotExistError, UserPermissionError
from online_player.pub.response.common_response import JSONResponse
from online_player.pub.tools.decorator import time_calc
from online_player.pub.tools.http import get_http_head_param
from online_player.users.dao.user_mapper import get_user_auth_info
from online_player.users.middleware.auth_setting import USER_AUTH_SETTING

log = logging.getLogger('users')


class AuthMiddleware(MiddlewareMixin):

    @time_calc
    def process_request(self, request):
        path = request.path
        method = request.method
        url_permission, method_permission = request_is_permission(path, method)
        if url_permission and method_permission:
            headers = get_headers_dict(request)
            if not headers.get('token') or not headers.get('account'):
                return JSONResponse(status=False, error_head=access, error=ErrorAccessLeaf.DENIED,
                                    http_status=status.HTTP_403_FORBIDDEN,
                                    language=headers.get('language'))
            try:
                user_do_match(headers)
                if user_permitted(headers.get('role'), path, method):
                    log.info('User {} permission authentication is successful!'.format(headers.get('account')))
                else:
                    return JSONResponse(status=False, error_head=access, error=ErrorAccessLeaf.DENIED,
                                        http_status=status.HTTP_403_FORBIDDEN,
                                        language=headers.get('language'))
            except [UserNotExistError, UserPermissionError] as e:
                log.error(e)
                return JSONResponse(status=False, error_head=access, error=ErrorAccessLeaf.DENIED,
                                    http_status=status.HTTP_403_FORBIDDEN,
                                    language=headers.get('language'))
            except Exception as e:
                log.error(e)
                return JSONResponse(status=False, error_head=system, error=ErrorServerLeaf.INTERNAL_SERVER_ERROR,
                                    http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    language=headers.get('language'))
        elif not url_permission and not method_permission:
            log.info('A user can login as a visitor!')
        else:
            return JSONResponse(status=False, error_head=access, error=ErrorAccessLeaf.DENIED,
                                http_status=status.HTTP_403_FORBIDDEN)


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
            break
    return url_permission, method_permission


def get_headers_dict(request):
    """
    获取header里面的用户信息
    :param request: 请求对象
    :return: 用户信息字典
    """
    token = get_http_head_param(request, 'authorization', log)
    language = get_http_head_param(request, 'language', log)
    account = get_http_head_param(request, 'account', log)
    role = get_http_head_param(request, 'role', log)
    return {
        'token': token,
        'language': language,
        'account': account,
        'role': role,
    }


def user_do_match(headers):
    """
    请求的信息是否与数据库的匹配
    :param headers: 消息体的头信息
    :return: None
    """
    account = headers.get('account')
    request_role = headers.get('role')
    request_token = headers.get('token')
    user_info = get_user_auth_info({'account': account})
    if not user_info:
        raise UserNotExistError(f'User {account} does not exist!')
    user_role = user_info[0].get('role')
    user_token = user_info[0].get('token')
    if user_token != request_token or user_role != request_role:
        raise UserPermissionError(f'User {account}\'s permissions do not match!')


def user_permitted(role, path, method):
    if role == UserConst.COMMON_USER.value:
        matched = match(path, method, USER_AUTH_SETTING.get('common'))
    elif role == UserConst.SUPER_USER.value:
        matched = match(path, method, USER_AUTH_SETTING.get('super'))
    else:
        matched = False
    return matched


def match(path, method, dic):
    url_allow = False
    method_allow = False
    for k, v in dic.items():
        if re.match(k, path):
            url_allow = True
            if method in v:
                method_allow = True
                break
    if url_allow and method_allow:
        return True
    return False
