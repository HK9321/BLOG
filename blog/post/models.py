from django.db import models

from user.models import User


class Post(models.Model):
    uid = models.IntegerField()
    title = models.CharField(max_length=32)
    content = models.TextField()
    publishTime = models.DateTimeField(auto_now=True)
    commentNum = models.IntegerField(default=0)
    tag = models.CharField(max_length=32)

    @property
    def user(self):
        user = User.objects.filter(id=self.uid)
        return user

    @property
    def get_user(self):
        user_set = User.objects.filter(id=self.uid)
        if user_set:
            user = user_set[0]
        else:
            user = User.objects.all()[0]
        return user


class Comment(models.Model):
    uid = models.IntegerField()
    pid = models.IntegerField()
    parent = models.ForeignKey('self', default=None,blank=True,null=True)
    comment_text = models.TextField(max_length=1000)
    create_time = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_username(self,*args):
        name = User.objects.filter(id=args[0].uid).first().username
        return name


class collectpost(models.Model):
    uid = models.IntegerField()
    pid = models.IntegerField()
