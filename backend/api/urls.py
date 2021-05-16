from django.urls import path
from api import views

urlpatterns = [
    path("api/<n>", views.get_n_tweet, name="get_n_tweet"),
    path("api/death/<str:month>", views.get_death_number, name="get_death_number"),
]