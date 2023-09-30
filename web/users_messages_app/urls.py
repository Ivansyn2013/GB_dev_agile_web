from django.urls import path


from users_messages_app import views


urlpatterns = [

    path('chat_list/<str:slug>', views.DetailView.as_view(), name='chat_list'),
    path('chat/<str:slug>', views.Chat.as_view(), name='chat'),

]


