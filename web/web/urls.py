"""
URL configuration for web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from authapp.views import home, RegisterUser, LoginUser, profile_user_view, top_players, logout_user, \
    ProfileUpdateView, RegisterDoneView, user_activate, login_github, login_github_callback, login_vk, login_vk_callback


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home,  name='home'),
    path('register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('profile/', profile_user_view, name='profile'),
    path('top_players', top_players, name='top'),
    path('logout/', logout_user,  name='logout'),
    path('edit_profile/', ProfileUpdateView.as_view(),  name='edit_profile'),
    path('', include("authapp.urls")),
    path('', include("users_messages_app.urls")),

    path('login/github/', login_github, name='login_github'),
    path('login/github/callback/', login_github_callback, name='login_github_callback'),
    path('login/vk/', login_vk, name='login_vk'),
    path('login/vk/callback/', login_vk_callback, name='login_vk_callback'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
