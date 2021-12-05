from django.db import models

from online_player.pub.const.user_const import UserConst


class User(models.Model):
    id = models.AutoField(primary_key=True, help_text='用户id')
    name = models.CharField(null=False, max_length=UserConst.NAME.value, help_text='用户姓名')
    address = models.CharField(null=True, max_length=UserConst.ADDRESS.value, help_text='用户地址')
    sex = models.CharField(null=False, max_length=UserConst.SEX.value, help_text='用户性别')
    phone = models.CharField(null=True, max_length=UserConst.PHONE.value, help_text='电话')
    token = models.CharField(null=False, max_length=UserConst.TOKEN.value, help_text='用户令牌')
    password = models.CharField(null=False, max_length=UserConst.PASSWORD.value, help_text='用户密码')
    email = models.CharField(null=True, max_length=UserConst.EMAIL.value, help_text='邮箱')
    state = models.BooleanField(default=False, help_text='用户状态，True为在线，False为离线')
    role = models.SmallIntegerField(default=1, help_text='用户角色，1为普通用户，9为超级管理员')
    application_time = models.DateTimeField(null=False, help_text='用户申请时间')
    last_login_time = models.DateTimeField(null=True, help_text='用户最后一次登录时间')
    last_logout_time = models.DateTimeField(null=True, help_text='用户最后一次登出时间')
    update_time = models.DateTimeField(null=True, help_text='用户最后一次更新时间')
    desc = models.CharField(null=True, max_length=UserConst.DESC.value, help_text='用户描述')
    try_count = models.SmallIntegerField(default=0, help_text='用户尝试次数，默认为0，重置为0，清除锁定和首次尝试时间')
    locked_time = models.DateTimeField(null=True, help_text='锁定的起始时间，10分钟后自动解锁，清除时间')
    first_try_time = models.DateTimeField(null=True, help_text='首次尝试错误的时间，10分钟且未锁定自动清除时间')
    commitment_letter = models.SmallIntegerField(default=0, help_text='承诺书签署标记，默认为未签署')

    class Meta:
        db_table = 'user'
        managed = False
