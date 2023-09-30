from django.shortcuts import render
from django.views import View
from django.views.generic import (TemplateView, UpdateView, ListView, DetailView)
from django.core.paginator import Paginator

# Create your views here.


class MyChats(ListView):
    Chats = []
    paginator = Paginator(Chats, 10)


class Chat(DetailView):
    pass