from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login

class RegisterView(APIView):
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        user = User.objects.create_user(username, password=password)
        user.save()
        return JsonResponse({}, status=201)

class LoginView(APIView):
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({}, status=200)
        else:
            return JsonResponse({ "error": "Invalid credentials." }, status=401)

