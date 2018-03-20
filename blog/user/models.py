from django.db import models
from django.contrib.auth.hashers import make_password, check_password, is_password_usable

from blog.settings import SECRET_KEY as salt


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=10, unique=True)
    age = models.IntegerField(default=20)
    sex = models.BooleanField(default=True)
    password_hash = models.CharField(max_length=128)
    email = models.EmailField()
    icon = models.ImageField(upload_to='images/icon')
    createTime = models.DateTimeField(auto_now_add=True)

    # 将密码设置为保护字段
    @property
    def password(self):
        raise AttributeError('密码不可读')

    # 设置密码（加密存储）
    @password.setter
    def password(self, password):
        self.password_hash = make_password(password, hasher='default')

    # 密码校验
    def verify_password(self, password):
        if is_password_usable(self.password_hash):
            return check_password(password, self.password_hash)


class Mail(models.Model):
    uid = models.CharField(max_length=10, db_index=True)
    senderId = models.CharField(max_length=10)
    content = models.TextField()
    createTime = models.DateTimeField(auto_now_add=True)
