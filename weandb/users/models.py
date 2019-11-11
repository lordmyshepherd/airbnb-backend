from django.db import models

class SocialPlatform(models.Model) :
    platform        = models.CharField(max_length = 100)

    class Meta :
        db_table = 'social_platform'

class Users(models.Model) : 
    social_platform = models.ForeignKey(SocialPlatform, on_delete=models.CASCADE, null = True)
    social_id       = models.IntegerField(null = True)
    first_name      = models.CharField(max_length = 100, null = True)
    last_name       = models.CharField(max_length = 100, null = True)
    email           = models.CharField(max_length = 100, null = True)
    password        = models.CharField(max_length = 100, null = True)
    birth_year      = models.IntegerField(null = True)
    birth_month     = models.IntegerField(null = True)
    birth_day       = models.IntegerField(null = True)
    is_host         = models.BooleanField(default = False)
    created_at      = models.DateTimeField(auto_now_add = True)
    updated_at      = models.DateTimeField(auto_now = True)

    class Meta : 
        db_table = 'users'

class HostInfos(models.Model) :
    user            = models.OneToOneField(Users, on_delete=models.CASCADE, null = True)
    host_image      = models.URLField(null = True)
    nickname        = models.CharField(max_length = 100, null = True)
    intro           = models.TextField(null = True)
    relation        = models.CharField(max_length=1000, null=True)
    language        = models.CharField(max_length=100, null=True)
    address         = models.CharField(max_length=1000, null=True)

    class Meta : 
        db_table = 'host_infos'
