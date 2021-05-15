from django.urls import path
from api import views

urlpatterns = [
    path("api/<n>", views.get_n_tweet, name="get_n_tweet"),
]