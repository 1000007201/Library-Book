from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import Book

class LoginSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})


class BookSerializers(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['name', 'author', 'quantity', 'description']
        required_field = fields
    
    def create(self, validated_data):
        return Book.objects.create(**validated_data)
    