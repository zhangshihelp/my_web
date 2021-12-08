from online_player.pub.tools.dbutil import execute_query_safe


@execute_query_safe
def get_user_auth_info(data):
    sql = """
        select role, token from public."user" where account={account};
    """
    return data, sql


@execute_query_safe
def get_users():
    sql = """
        select name from public."user"
    """
    return {}, sql
