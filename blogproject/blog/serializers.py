from rest_framework import serializers
from .models import User, Post
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password



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
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'body', 'image', 'status', 'view_count', 'created_at', 'updated_at', 'user']
        read_only_fields = ['id', 'view_count', 'created_at', 'updated_at']
