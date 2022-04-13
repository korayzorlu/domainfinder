from django.db import models

# Create your models here.

class Domain(models.Model):
    user = models.ForeignKey("auth.User", on_delete = models.CASCADE)
    name = models.CharField(max_length = 500)
    creation_date = models.CharField(max_length = 50, blank =True, null = True)
    expiration_date = models.CharField(max_length = 50, blank =True, null = True)
    name_servers = models.CharField(max_length = 500, blank =True, null = True)
    registrant_name = models.CharField(max_length = 1000, blank =True, null = True)
    created_date = models.DateTimeField(auto_now_add = True)

class Subdomain(models.Model):
    domain = models.ForeignKey(Domain, on_delete = models.CASCADE, related_name = "subdomains")
    name = models.CharField(max_length = 500, blank =True, null = True)

    def __str__(self):
        return self.name
