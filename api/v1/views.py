from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from base.models import User, Author, Book
from .serializers import UserSerializer, LoginSerializer, AuthorSerializer, BookSerializer
from base.messages import MESSAGES
import logging
from rest_framework import serializers

logger = logging.getLogger(__name__)

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response_data = {
            "status": "Failed",
            "message": MESSAGES.get("failed_to_register")
        }
        status_code = status.HTTP_400_BAD_REQUEST
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                email=serializer.validated_data['email'],
                username=serializer.validated_data['username'],
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                password=serializer.validated_data['password']
            )
            refresh = RefreshToken.for_user(user)
            response_data = {
                "status": "Success",
                "message": MESSAGES.get("success_register"),
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                "user": {
                    "email": user.email,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "full_name": user.full_name
                }
            }
            status_code = status.HTTP_201_CREATED
        return Response(response_data, status=status_code)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        response_data = {
            "status": "Failed",
            "message": MESSAGES.get("failed_to_login")
        }
        status_code = status.HTTP_400_BAD_REQUEST
        try:
            logger.info(f"Login attempt with data: {request.data}")
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                logger.error(f"Serializer validation failed: {serializer.errors}")
                return Response(response_data, status=status_code)

            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)

            if not user or not user.is_active:
                response_data["message"] = MESSAGES.get("invalid_credentials")
                return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

            refresh = RefreshToken.for_user(user)
            response_data = {
                "status": "Success",
                "message": MESSAGES.get("login_success").format(user=user),
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                "user": {
                    "email": user.email,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "full_name": user.full_name
                }
            }
            status_code = status.HTTP_200_OK
            return Response(response_data, status=status_code)
        except Exception as exception:
            logger.exception(f"Login error: {str(exception)}")
            return Response(response_data, status=status_code)


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        author_name = self.request.data.get('author')
        author_bio = self.request.data.get('author_bio')
        
        if not author_name:
            raise serializers.ValidationError({'author': 'Author name is required'})

        try:
            # First try to find an existing author
            author = Author.objects.filter(user__full_name=author_name).first()
            
            # If author doesn't exist, create a new user and author
            if not author:
                # Generate a unique email
                base_email = f"{author_name.lower().replace(' ', '_')}@bookstore.com"
                email = base_email
                counter = 1
                while User.objects.filter(email=email).exists():
                    email = f"{base_email.split('@')[0]}{counter}@bookstore.com"
                    counter += 1

                # Create a new user for the author
                user = User.objects.create_user(
                    username=author_name.lower().replace(' ', '_'),
                    email=email,
                    first_name=author_name.split()[0],
                    last_name=' '.join(author_name.split()[1:]) if len(author_name.split()) > 1 else '',
                    is_author=True
                )
                # Create the author
                author = Author.objects.create(
                    user=user,
                    bio=author_bio or '',
                    created_by=self.request.user
                )
            elif author_bio:  
                author.bio = author_bio
                author.save()

            # Save the book with the author
            serializer.save(created_by=self.request.user, author=author)
            
        except Exception as e:
            logger.error(f"Error creating/updating author: {str(e)}")
            raise serializers.ValidationError({'author': str(e)})


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'object_id'
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Handle author update if provided
        author = request.data.get('author')
        author_bio = request.data.get('author_bio')
        if author:
            try:
                author = Author.objects.filter(user__full_name=author).first()
                if author:
                    author.bio = author_bio
                    author.save()
            except Exception as e:
                return Response(
                    {'error': str(e)}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class AuthorBooksView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        object_id = self.kwargs.get('object_id')
        return Book.objects.filter(author__object_id=object_id)