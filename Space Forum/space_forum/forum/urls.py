from django.urls import path
from .views import (
    home, about, contact, signup, user_login, user_logout, profile,
    forum_list, thread_list, post_list,
    ChatRoomListView, ChatRoomView, edit_profile
)

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('forums/', forum_list, name='forum_list'),
    path('forums/<int:forum_id>/', thread_list, name='thread_list'),
    path('threads/<int:thread_id>/', post_list, name='post_list'),
    path('chat/', ChatRoomListView.as_view(), name='chat_room_list'),
    path('chat/<str:room_name>/', ChatRoomView.as_view(), name='chat_room'),
]
