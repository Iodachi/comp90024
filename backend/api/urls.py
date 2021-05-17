from django.urls import path
from api import views

urlpatterns = [
    path("api/test/<n>", views.get_n_tweet, name="get_n_tweet"),
    path("api/death/<str:month>", views.get_death_number, name="get_death_number"),
    path("api/employment", views.get_employment, name="get_employment"),
]