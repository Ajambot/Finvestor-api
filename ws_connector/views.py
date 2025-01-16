# Create your views here.
from django.http import JsonResponse
from .models import Position, Credential, User
from .serializer import PositionSerializer
from rest_framework.views import APIView
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

        if not access_token:
            return JsonResponse({"error": "Unexpected response from third-party API."}, status=502)

        if request.user.is_authenticated:
            user = request.user
            if not hasattr(user, 'credential'):
                credential = Credential.objects.create(
                    user = user,
                    ws_access_token = access_token,
                )
            else:
                credentialObj = Credential.objects.get(user=request.user)
                credentialObj.ws_access_token = access_token
                credentialObj.save()
            return JsonResponse({ "message": "Wealthsimple Access Token stored successfully in user profile" }, status = 200)
        else:
            response = JsonResponse({ "message": "Token stored successfully in local storage" }, status=200)
            response.set_cookie("ws-access-token", access_token, httponly=True, secure=True)
            return response

class WsFetchView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            ws_access_token = request.user.credential.ws_access_token
        else:
            ws_access_token = request.COOKIES.get('ws-access-token') 

        if ws_access_token is None:
            return JsonResponse({"error": "Wealthsimple credentials missing or malformed"}, status=401)

        headers = {
            "Authorization": f"Bearer {ws_access_token}",
            "Content-Type": "application/json"
        }
        try:
            resp = requests.get(f"{ws_url}/account/positions", headers=headers)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return JsonResponse({"error": str(e)}, status=resp.status_code)

        positions = resp.json()
        positions = positions["results"]
        if request.user.is_authenticated:
            for i in range(len(positions)):
                position = positions[i]
                newPos = { 
                    "account_id": position["account_id"],
                    "user": request.user.id,
                    "symbol": position["stock"]["symbol"],
                    "book_value": position["book_value"]["amount"],
                    "amount": position["quantity"],
                }
                positions[i] = newPos

            Position.objects.filter(user=request.user.id).delete()
            serializer = PositionSerializer(data = positions, many = True)
            if(serializer.is_valid()):
                serializer.save()
                return JsonResponse({ "message" : "Positions stored successfully in user profile" }, status=200)
            return JsonResponse(serializer.errors, status=400)
        else:
            for i in range(len(positions)):
                position = positions[i]
                newPos = { 
                    "account_id": position["account_id"],
                    "symbol": position["stock"]["symbol"],
                    "book_value": position["book_value"]["amount"],
                    "amount": position["quantity"],
                }
                positions[i] = newPos
            response = JsonResponse({ "message": "Positions stored successfully in local storage" })
            response.set_cookie("ws-positions", positions, httponly=True, secure=True)
            return response

class PositionView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            positions = Position.objects.filter(user=request.user.id)
            serializer = PositionSerializer(positions, many=True)
            return JsonResponse(serializer.data, status=200, safe=False)
        else:
            positions = request.COOKIES.get("ws-positions")
            if not positions:
                positions = {}
            return JsonResponse(positions, status=200, safe=False)
