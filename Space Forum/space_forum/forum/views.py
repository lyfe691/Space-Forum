from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View
from django.http import HttpResponseNotAllowed
from .models import Forum, Thread, Post, ChatRoom
from .forms import ChatRoomForm, UserUpdateForm, UserRegisterForm, CustomAuthenticationForm
from django.contrib.auth.models import User

def home(request):
    return render(request, 'forum/home.html')

def about(request):
    return render(request, 'forum/about.html')

def contact(request):
    return render(request, 'forum/contact.html')

def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'forum/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'forum/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    return render(request, 'forum/profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form
    }

    return render(request, 'forum/edit_profile.html', context)

class ChatRoomListView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        chat_rooms = ChatRoom.objects.all()
        form = ChatRoomForm()
        return render(request, 'forum/chat_room_list.html', {'chat_rooms': chat_rooms, 'form': form})

    def post(self, request, *args, **kwargs):
        form = ChatRoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chat_room_list')
        chat_rooms = ChatRoom.objects.all()
        return render(request, 'forum/chat_room_list.html', {'chat_rooms': chat_rooms, 'form': form})

class ChatRoomView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'next'

    def get(self, request, room_name, *args, **kwargs):
        return render(request, 'forum/chat_room.html', {
            'room_name': room_name
        })

def forum_list(request):
    forums = Forum.objects.all()
    return render(request, 'forum/forum_list.html', {'forums': forums})

def thread_list(request, forum_id):
    threads = Thread.objects.filter(forum_id=forum_id)
    return render(request, 'forum/thread_list.html', {'threads': threads})

def post_list(request, thread_id):
    posts = Post.objects.filter(thread_id=thread_id)
    return render(request, 'forum/post_list.html', {'posts': posts})

def custom_permission_denied_view(request, exception=None):
    return render(request, 'forum/403.html', status=403)
