from django.db import models

class Users(models.Model) : 
    email       = models.CharField(max_length=200)
    password    = models.CharField(max_length=200)
    host        = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta : 
        db_table = 'users'

class HostInfos(models.Model) :
    user        = models.ForeignKey(Users, on_delete=models.CASCADE)
    name        = models.CharField(max_length=100)
    image       = models.ImageField(blank=True, upload_to='images/') 
    intro       = models.TextField(null=True)
    language    = models.CharField(max_length=100)
    address     = models.CharField(max_length=1000)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta : 
        db_table = 'host_infos'



