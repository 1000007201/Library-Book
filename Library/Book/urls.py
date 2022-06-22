from django.urls import path
from .views import LoginApiView, LogoutApiView, AddBookApiView, UpdateBookApiView, DeleteBookApiView, StudentApiView

urlpatterns = [
    path('login/', LoginApiView.as_view()),
    path('logout/', LogoutApiView.as_view()),
    path('add/', AddBookApiView.as_view()),
    path('update/<str:id>', UpdateBookApiView.as_view()),
    path('delete/<str:id>', DeleteBookApiView.as_view()),
    path('get/book/<str:id>', StudentApiView.as_view()),
    path('get/book/', StudentApiView.as_view())
]
