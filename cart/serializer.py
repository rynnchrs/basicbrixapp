from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password


# Serializer for the built-in User table in django
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
                    'password':{'write_only': True},
                }

    # Use to validate and hash the password
    def validate_password(self, password: str) -> str:
        return make_password(password)


# Register serializer extended with the User Serializer
class RegisterSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Customer
        fields = ['user','name', 'email']

    # create function of the serializer
    def create(self, validated_data):
        user_data = validated_data.pop('user')

        user = UserSerializer.create(UserSerializer(),validated_data=user_data)
        user_info = Customer.objects.create(user= user,name =validated_data['name'], email = validated_data['email'])
        return user_info


# Store serializer for the Products Table
class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


# Store serializer for the Products Table by Admin (can CRUD)
class AdminStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


