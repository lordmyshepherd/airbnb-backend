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

class Languages(models.Model) :
    language    = models.CharField(max_length = 200)

    class Meta :
        db_table = 'languages'

class HostInfos(models.Model) :
    user            = models.OneToOneField(Users, on_delete = models.CASCADE, null = True)
    language        = models.ManyToManyField(Languages, through = 'HostInfosLanguages')
    host_image      = models.URLField()
    nickname        = models.CharField(max_length = 100, null = True)
    intro           = models.TextField(null = True)
    interaction     = models.CharField(max_length = 1000, null = True)
    country         = models.CharField(max_length = 100, null = True)
    city            = models.CharField(max_length = 100, null = True)

    class Meta :
        db_table = 'host_infos'

class HostInfosLanguages(models.Model) :
    hostinfo    = models.ForeignKey(HostInfos, on_delete = models.CASCADE, null = True)
    language    = models.ForeignKey(Languages, on_delete = models.CASCADE, null = True)

    class Meta :
        db_table = 'host_infos_languages'
