from django.db import models

class SiteAccess(models.Model):
    ip = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255, blank=True)
    path = models.CharField(max_length=255)  # URL acessada
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip} acessou {self.path} em {self.date}"
