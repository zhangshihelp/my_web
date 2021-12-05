from django.db import connection

from psycopg2 import sql as safe_sql


def execute_many_safe(func):
    """
    使用该装饰器，需要返回参数列表和sql模板
    data --> [{key1: value1, key2: value2}, {key3: value3, key4: value4}...]
    sql --> delete from table where name={name};
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        data, sql = func(*args, **kwargs)
        for item in data:
            __execute_safe(item, sql)
    return wrapper


def execute_one_safe(func):
    """
    使用该装饰器，需要返回参数列表和sql模板
    data --> {key1: value1, key2: value2}
    sql --> delete from table where name={name};
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        data, sql = func(*args, **kwargs)
        __execute_safe(data, sql)
    return wrapper


def execute_query_safe(func):
    """
    使用该装饰器，需要返回参数列表和sql模板
    data --> {key1: value1, key2: value2}
    sql --> select * from table where name={name};
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        data, sql = func(*args, **kwargs)
        return __execute_safe(data, sql, True)
    return wrapper


def __execute_safe(data, sql, query=False):
    """
    防止sql注入的方法
    :param data: sql的参数
    :param sql: sql模板
    :param query: True则未查询，False为执行sql语句
    :return:
    """
    query_result = None
    with connection.cursor() as cursor:
        condition = {}
        for key, value in data.items():
            if key == 'table_name':
                condition.update({key: safe_sql.Identifier(value)})
            condition.update({key: safe_sql.Literal(value)})
        sql = safe_sql.SQL(sql).format(**condition)
        cursor.execute(sql)
        if query:
            query_result = __dict_fetchall(cursor)
    return query_result


def __dict_fetchall(cursor):
    """
    sql执行的结果返回值转换为dict
    :param cursor:
    :return:
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
