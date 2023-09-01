from .apps import MainConfig
from django.urls import path
from .views import *

app_name = MainConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]