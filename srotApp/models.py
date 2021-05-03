from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone as tz
# Create your models here.

class Discussion(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    dis_type = models.CharField(choices=(("Helping",'Helping'),("Help Needed","Help Needed")),max_length=100)
    information = models.TextField()
    hashtags = models.TextField()
    timestamp = models.DateTimeField(default=tz.now)

    def __str__(self):
        return self.title
    

