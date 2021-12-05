from online_player.pub.tools.dbutil import execute_query_safe


def get_users(data):
    sql = """
        select name from public.user
    """
