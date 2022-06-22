from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import LoginSerializers, BookSerializers
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import Response, APIView
from django.utils.decorators import method_decorator
from .jwt_token import token_required, get_token
from .utils import Utils
from .models import Book


class LoginApiView(GenericAPIView):
    serializer_class = LoginSerializers
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        data = request.data
        serializer = LoginSerializers(data=data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        password = serializer.data.get('password')
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({'Error': 'username and password are not valid', 'Code': 404})
        token = get_token(user)
        login(request, user)
        return Response({'Message': f'{username} logged in', 'Code': 200, 'token': token})


class LogoutApiView(APIView):
    def get(self, request):
        logout(request)
        return Response({'Message': 'Logged Out', 'Code': 200})


class AddBookApiView(GenericAPIView):
    serializer_class = BookSerializers
    authentication_classes = ()
    permission_classes = ()

    @method_decorator(token_required)
    def post(self, request, user_id):
        data = request.data
        user_obj = Utils.check_superuser(user_id)
        if user_obj:
            return Response(user_obj)
        serializer = BookSerializers(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'Message': serializer.data, 'Code': 200})


class UpdateBookApiView(GenericAPIView):
    serializer_class = BookSerializers
    authentication_classes = ()
    permission_classes = ()

    @method_decorator(token_required)
    def patch(self, request, user_id, id):
        user_obj = Utils.check_superuser(user_id)
        if user_obj:
            return Response(user_obj)
        book = Book.objects.get(pk=id)
        data = request.data
        serializer = BookSerializers(instance=book, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'Message': 'Book updated', 'Code': 200})


class DeleteBookApiView(APIView):
    
    @method_decorator(token_required)
    def delete(self, request, user_id, id):
        user_obj = Utils.check_superuser(user_id)
        if user_obj:
            return Response(user_obj)
        book = Book.objects.get(pk=id)
        book.delete()
        return Response({'Message': 'Book Deleted', 'Code': 200})


class StudentApiView(GenericAPIView):
    serializer_class = BookSerializers
    def get(self, request, id=None):
        if id:
            book = Book.objects.get(pk=id)
            serializer = BookSerializers(book)
            return Response({'data': serializer.data, 'Code': 200})
        book = Book.objects.all()
        serializer = BookSerializers(book, many=True)
        return Response({'data': serializer.data, 'Code': 200})
