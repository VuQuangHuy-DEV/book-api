from rest_framework import generics
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomUser
import jwt, datetime



# Create your views here.

# Book

class BookListCreateView(generics.ListCreateAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.all()


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    APPEND_SLASH = True
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# BookHistory

class BookHistoryListCreateView(generics.ListCreateAPIView):
    serializer_class = BookHistorySerializer

    def get_queryset(self):
        return BookHistory.objects.all()


class BookHistoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookHistory.objects.all()
    serializer_class = BookSerializer


# BookReview

class BookReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = BookReviewSerializer

    def get_queryset(self):
        return BookReview.objects.all()


class BookReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookReview.objects.all()
    serializer_class = BookReviewSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        response = Response();
        email = request.data['email']
        password = request.data['password']

        user = CustomUser.objects.filter(email=email).first()
        payload = {
            'email': user.email,
            'username': user.username
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        data = {
            "status_code": response.status_code,
            "message": "Registration successful",
            "data": {
                "email": user.email,
                "username": user.username,
                "token": token
            }

        }
        response.data = data

        return response


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = CustomUser.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'email': user.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        # cach nay cho no khoong hien token tra ve
        # return Response({
        #     'jwt':token
        # })

        # Tra ve qua cookie
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unavthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unavthenticated')
        user = CustomUser.objects.filter(email=payload['email']).first()
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response