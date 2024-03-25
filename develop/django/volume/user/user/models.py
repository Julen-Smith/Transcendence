from django.db import models

class user_login(models.Model):

    username = models.CharField(max_length=16, unique=True)
    email = models.EmailField(max_length=32, unique=True)
    password = models.CharField(max_length=100)
    last_log = models.DateTimeField(auto_now=True)
    mode = models.SmallIntegerField(default=0)

    class Meta:
        db_table = 'user_login'
        managed = False

# Create your models here.
class Friends(models.Model):

    user = models.ForeignKey(user_login, related_name='friends', on_delete=models.CASCADE)
    friend = models.ForeignKey(user_login, related_name='users', on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'friend')