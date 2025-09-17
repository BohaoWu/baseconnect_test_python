from django.db import models

# Create your models here.

class Articles(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=2000)
    url = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    abstract = models.CharField(max_length=200)
    risk_score = models.IntegerField(default=0)

    
