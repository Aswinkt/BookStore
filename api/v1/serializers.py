from rest_framework import serializers
from base.models import User, Author, Book


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    full_name = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class AuthorSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Author
        fields = [
            'full_name',
            'bio', 
            'email'
        ]


class BookSerializer(serializers.ModelSerializer):
    author_details = AuthorSerializer(source='author', read_only=True)

    class Meta:
        model = Book
        fields = ['object_id', 'title', 'description', 'price', 'published_date', 'author_details']
        read_only_fields = ['object_id']

