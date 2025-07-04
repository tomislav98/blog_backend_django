from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
class Users(models.Model):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", _("Admin")
        AUTHOR = "AUTHOR", _("Author")
        SUBSCRIBER = "SUBSCRIBER", _("Subscriber")


    user_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30, unique=True)
    password = models.CharField() # assuming hashed
    role = models.CharField(max_length=10, choices=Role,default=Role.SUBSCRIBER)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class Posts(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", _("Draft")
        PUBLISHED = "PUBLISHED", _("Published")
    user = models.ForeignKey(Users, on_delete=models.CASCADE) # many to one relationships
    title = models.CharField()
    slug = models.SlugField(unique=True, blank=True)
    body = models.CharField()
    status = models.CharField(max_length=9, choice=Status, default=Status.DRAFT)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
