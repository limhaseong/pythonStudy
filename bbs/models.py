from django.db import models
# from account.models import User
from django.conf import settings


# Create your models here.
class Board(models.Model):
    seq = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    title = models.CharField(max_length=50, null=False)
    contents = models.TextField(null=False)
    url = models.URLField(null=False)
    email = models.EmailField(null=False)
    cdate = models.DateTimeField(auto_now_add=True)
    user_id = models.CharField(max_length=50, null=True)           # settings.AUTH_USER_MODEL, db_column='user_id', on_delete=models.DO_NOTHING, 

    def __str__(self):
        return self.name 
    
    