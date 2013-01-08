from django.db import models

class CloudStackIpAddress(models.Model):
    name                = models.CharField(max_length=200)
  
    def __unicode__(self):
        return self.name

class DbConfig(models.Model):

    DBCONFIG = (
        ("cloudstack", "cloudstack"),
        ("cloudportal", "cloudportal"),
        ("cloud_tests", "cloud_tests"),)

    db_purpose          = models.CharField(choices=DBCONFIG, max_length=64)
    sql_host            = models.CharField(max_length=200)
    sql_user            = models.CharField(max_length=200)
    sql_password        = models.CharField(max_length=200)
    sql_database        = models.CharField(max_length=200)

    def __unicode__(self):
        return self.db_purpose
