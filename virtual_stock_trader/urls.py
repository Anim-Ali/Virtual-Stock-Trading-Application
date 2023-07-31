from django.urls import path
from . import views

# routes for the app
urlpatterns = [
    path("test", views.test, name="test"),
    path("", views.home, name="home"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("quote", views.quotation_view, name="quote"),
    path("buy", views.purchase_view, name="buy"),
    path("sell", views.sell_view, name="sell"),
    path("home", views.home, name="home"),
    path("add_cash", views.add_cash, name="add cash"),
    path("sentiment", views.sentiment, name="sentiment")
]