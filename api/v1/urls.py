from django.urls import path
from .views import (
    RegisterView, 
    LoginView, 
    BookListCreateView, 
    BookDetailView, 
    AuthorBooksView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<str:object_id>/', BookDetailView.as_view(), name='book-detail'),
    path('authors/<str:object_id>/books/', AuthorBooksView.as_view(), name='author-books'),
] 



