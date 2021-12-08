USER_AUTH_SETTING = {
    # ---------- 游客相关 ----------
    'visitor': {
        r'/v1/users/login/?': ['POST'],
        r'/v1/users/register/?': ['POST'],
        r'/v1/users/logout/?': ['POST'],
    }
}
