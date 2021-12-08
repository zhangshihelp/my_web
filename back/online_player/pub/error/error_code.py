from enum import Enum


###########################################################################################
# 错误码根节点
###########################################################################################
class ErrorRoot(Enum):
    USER = '100'
    SYSTEM = '900'


###########################################################################################
# 错误码用户类
###########################################################################################
class ErrorUserNode(Enum):
    REGISTER = '01'
    ACCESS = '02'


class ErrorRegisterLeaf(Enum):
    USER_EXIST = '001'


class ErrorAccessLeaf(Enum):
    DENIED = '001'


###########################################################################################
# 错误码系统类
###########################################################################################
class ErrorSystemNode(Enum):
    SYSTEM = '01'


class ErrorServerLeaf(Enum):
    INTERNAL_SERVER_ERROR = '001'


register = [ErrorRoot.USER, ErrorUserNode.REGISTER]
access = [ErrorRoot.USER, ErrorUserNode.ACCESS]
system = [ErrorRoot.SYSTEM, ErrorSystemNode.SYSTEM]


def get_error_code(errors):
    if not errors:
        return
    return errors[0].value + errors[1].value + errors[2].value
