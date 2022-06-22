from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=50, null=False)
    author = models.CharField(max_length=50, null=False)
    quantity = models.IntegerField(blank=False)
    description = models.TextField(max_length=400)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
