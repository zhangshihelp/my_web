from enum import Enum


###########################################################################################
# 错误码根节点，定义error_root
###########################################################################################
class ErrorRoot(Enum):
    USER = '100'
    SYSTEM = '900'


class ErrorUserNode(Enum):
    REGISTER = '01'


class ErrorRegisterLeaf(Enum):
    USER_EXIST = '001'


def get_error_code(errors):
    if not errors:
        return
    return errors[0].value + errors[1].value + errors[2].value
