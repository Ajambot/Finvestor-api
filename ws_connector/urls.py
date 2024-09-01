from django.urls import path

from .views import PositionView, WsFetchView, WsLoginView

urlpatterns = [
    path("wealthsimple/position", WsFetchView.as_view()),
    path("wealthsimple/login", WsLoginView.as_view()),
    path("position", PositionView.as_view()),
]