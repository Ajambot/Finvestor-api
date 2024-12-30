from django.urls import path

from .views import PositionView, WsFetchView, WsLoginView, WsRefreshView

urlpatterns = [
    path("wealthsimple/refresh", WsFetchView.as_view()),
    path("wealthsimple/login", WsLoginView.as_view()),
    path("positions", PositionView.as_view()),
    path("wealthsimple/token/refresh", WsRefreshView.as_view())
]
