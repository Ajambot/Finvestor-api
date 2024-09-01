from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import PositionSerializer
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import requests

ws_url = "https://trade-service.wealthsimple.com"

class WsLoginView(APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]
        otp = request.data["otp"]
        body = {"email": email, "password": password, "otp": otp}
        resp = requests.post(f"{ws_url}/auth/login", data=body)
        if not resp.ok:
            return JsonResponse(resp.json(), status=resp.status_code)
        headers = resp.headers
        access_token = headers.get("x-access-token")
        refresh_token = headers.get("x-refresh-token")
        expiry = headers.get("x-access-token-expires")

        response = JsonResponse({}, status=200)
        response.set_cookie("ws-access-token", access_token, httponly=True, secure=True)
        response.set_cookie("ws-refresh-token", refresh_token, httponly=True, secure=True)
        response.set_cookie("ws-access-token-expires", expiry, httponly=True, secure=True)

        return response

class WsFetchView(APIView):
    def get(self, request):
        ws_access_token = request.headers.get('ws-access-token')
        if ws_access_token is None:
            return JsonResponse({"detail": "Wealthsimple Authorization header missing or malformed"}, status=401)
        headers = {
            "Authorization": f"Bearer {ws_access_token}",
            "Content-Type": "application/json"
        }
        try:
            resp = requests.get(f"{ws_url}/account/positions", headers=headers)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return JsonResponse({"detail": str(e)}, status=resp.status_code)
        # TODO: Save fetched positions to database
        return JsonResponse(resp.json(), status=200)

class PositionView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = PositionSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        serializer = PositionSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)