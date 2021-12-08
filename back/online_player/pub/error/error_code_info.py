from .error_code import *
from ..exception.common import CodeNotFoundError

ERROR_INFO = {
    ErrorRoot.USER: {
        ErrorUserNode.REGISTER: {
            ErrorRegisterLeaf.USER_EXIST: {
                'en': 'User name already exists!',
                'zh': '用户名已存在！',
                'advice_en': 'Please change your user name and try again!',
                'advice_zh': '请更换用户名后重试！',
            }
        },
        ErrorUserNode.ACCESS: {
            ErrorAccessLeaf.DENIED: {
                'en': 'User permission error, unable to access!',
                'zh': '用户权限错误，无法访问！',
                'advice_en': 'Please contact the administrator to confirm the permission!',
                'advice_zh': '请联系管理员确认权限！',
            }
        }
    }
}


def get_error_msg(language, errors, *args):
    if not errors:
        return
    try:
        if language is None or language == 'zh':
            msg = ERROR_INFO.get(errors[0]).get(errors[1]).get(errors[2]).get('zh')
        else:
            msg = ERROR_INFO.get(errors[0]).get(errors[1]).get(errors[2]).get('en')
        return msg % args if '%s' in msg else msg
    except AttributeError:
        raise CodeNotFoundError()


def get_error_advice(language, errors, *args):
    if not errors:
        return
    try:
        if language is None or language == 'zh':
            msg = ERROR_INFO.get(errors[0]).get(errors[1]).get(errors[2]).get('advice_zh')
        else:
            msg = ERROR_INFO.get(errors[0]).get(errors[1]).get(errors[2]).get('advice_en')
        return msg % args if '%s' in msg else msg
    except AttributeError:
        raise CodeNotFoundError()
