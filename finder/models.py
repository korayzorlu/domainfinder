from django.db import models

# Create your models here.

class Domain(models.Model):
    user = models.ForeignKey("auth.User", on_delete = models.CASCADE)
    name = models.CharField(max_length = 50)
    created_date = models.DateTimeField(auto_now_add = True)

class Subdomain(models.Model):
    domain = models.ForeignKey(Domain, on_delete = models.CASCADE, related_name = "subdomains")
    name = models.CharField(max_length = 50)
