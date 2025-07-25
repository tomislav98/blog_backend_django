from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from blogproject.utils import extract_toc

class CustomUserManager(BaseUserManager):
    def create_user(self, email, user_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, user_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, user_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", _("Admin")
        AUTHOR = "AUTHOR", _("Author")
        SUBSCRIBER = "SUBSCRIBER", _("Subscriber")

    user_name = models.CharField(max_length=30,  unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.SUBSCRIBER)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'user_name' # required on login field
    REQUIRED_FIELDS = ['email'] # required on registration field

    def __str__(self):
        return self.email


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", _("Draft")
        PUBLISHED = "PUBLISHED", _("Published")

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')  # many-to-one relation
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    body = models.TextField()
    toc = models.JSONField(default=list, blank=True)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    status = models.CharField(max_length=9, choices=Status.choices, default=Status.DRAFT)
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.toc = extract_toc(self.body)  # auto-generate TOC from markdown body
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title


class Comment(models.Model):
    class Status(models.TextChoices):
        APPROVED = "APPROVED", _("Approved")
        PENDING = "PENDING", _("Pending")
        SPAM = "SPAM", _("Spam")

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    comment_body = models.TextField()
    status = models.CharField(max_length=9, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.post}'


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='post_categories')

    class Meta:
        unique_together = ('post', 'category')

    def __str__(self):
        return f'{self.post.title} in {self.category.name}'


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='post_tags')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['post', 'tag'], name='unique_post_tag')
        ]

    def __str__(self):
        return f'{self.post.title} - {self.tag.name}'


class PostView(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_views')
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
