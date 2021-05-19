from django.urls import path
from api import views

urlpatterns = [
    path("api/test/<int:n>", views.get_n_tweet, name="get_n_tweet"),
    path("api/death/<str:month>", views.get_death_number, name="get_death_number"),
    path("api/employment", views.get_employment, name="get_employment"),
    path("api/tweet/top/<str:mode>/<int:n>/<str:timeS>/<str:timeE>", views.get_top, name="get_top"),
    path("api/cases", views.get_cases, name="get_cases"),
]