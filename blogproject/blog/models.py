from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", _("Admin")
        AUTHOR = "AUTHOR", _("Author")
        SUBSCRIBER = "SUBSCRIBER", _("Subscriber")

    user_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30, unique=True)
    password = models.CharField(max_length=128)  # assuming hashed password length
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.SUBSCRIBER)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_name


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", _("Draft")
        PUBLISHED = "PUBLISHED", _("Published")

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')  # many-to-one relation
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    body = models.TextField()
    status = models.CharField(max_length=9, choices=Status.choices, default=Status.DRAFT)
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
