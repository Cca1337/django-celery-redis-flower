from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("weather", views.weather, name="weather"),
    path("word-counter", views.word_counter, name="word_counter"),     
    path("emails", views.email_sender, name="email_sender"),   
    path("dashboard", views.dashboard, name="dashboard"),             
]

urlpatterns += staticfiles_urlpatterns()

