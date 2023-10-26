from django.db import models
from django.utils import timezone
   
class Book(models.Model):
    address = models.CharField(max_length=500, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    year = models.CharField(max_length=10, null=True, blank=True)
    size = models.CharField(max_length=30, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.is_deleted = True
        self.save()
    def __str__(self) -> str:
        return self.address

class Keyword(models.Model):
    name = models.CharField(max_length=100)
    books=models.ManyToManyField(Book, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.is_deleted = True
        self.save()
    def __str__(self) -> str:
        return self.name



