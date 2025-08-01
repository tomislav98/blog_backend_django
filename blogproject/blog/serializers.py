from rest_framework import serializers
from .models import User, Comment, Post, PostTag, Tag, Category, PostCategory
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.utils.text import slugify


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'user_name', 'email', 'role', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.user_name
        return token

"""

🧪 In Simple Terms:
Action	Purpose
🡒 Serialization	Converts a Django object (e.g. Comment) → JSON for API response
🡐 Deserialization	Takes incoming JSON (from a POST/PUT request) → validates and converts
                    it → saves as a Django model instance


Client POSTs data
       ↓
JSON (JavaScript Object Notation) — a text-based format -> Python dictionary
Serializer fields defined (user_name, email, password, password2)
       ↓
Field validations (email uniqueness, password strength, required fields)
       ↓
Custom validate(): check if password == password2
       ↓
If valid → serializer.save() calls create()
       ↓
In create():
    - Remove password2 (not stored)
    - Hash password
    - Create User instance
       ↓
User saved in database
       ↓
Response sent back (e.g., user info without password)

"""

# that  means take data from model -> json, it's called in view logic
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    # This is not in model so I ovveride
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('user_name', 'email', 'password', 'password2')
        extra_kwargs = {
            'user_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # remove confirmation field

        password = validated_data.pop('password')


         # Use the custom manager to hash the password correctly
        user = User.objects.create_user(password=password, **validated_data)
        return user


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    category_names = serializers.SerializerMethodField()

    tag_names = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )
    category_names_input = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'body', 'toc', 'image', 'status',
            'view_count', 'created_at', 'updated_at', 'user',
            'comments_count', 'tag_names', 'category_names_input',
            'category_names', 'tags'
        ]
        read_only_fields = ['id', 'view_count', 'slug', 'created_at', 'updated_at', 'category_names']

    def get_comments_count(self, obj):
        return obj.comments.filter(status='APPROVED').count()

    def get_tags(self, obj):
        return TagSerializer(
            [pt.tag for pt in obj.post_tags.all()],
            many=True
        ).data

    def get_category_names(self, obj):
        return [pc.category.name for pc in obj.post_categories.all()]

    def create(self, validated_data):
        tag_names = validated_data.pop('tag_names', [])
        category_names = validated_data.pop('category_names_input', [])
        post = Post.objects.create(**validated_data)

        for name in tag_names:
            slug = slugify(name)
            tag, _ = Tag.objects.get_or_create(name=name, defaults={'slug': slug})
            PostTag.objects.get_or_create(post=post, tag=tag)

        for name in category_names:
            category, _ = Category.objects.get_or_create(name=name)
            PostCategory.objects.get_or_create(post=post, category=category)

        return post




class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Include user info
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment

        fields = [
            'id', 'user', 'post', 'parent_comment', 'comment_body',
            'status', 'created_at', 'replies'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'status', 'replies']


    def get_replies(self, obj):
        replies = obj.replies.filter(status='APPROVED')
        return CommentSerializer(replies, many=True).data

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']
