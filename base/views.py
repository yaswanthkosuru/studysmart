from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Room, Topic, Message
from .froms import RoomForm, signupform
from django.contrib.auth.forms import UserCreationForm

""" Create your views here.
rooms = [
   {"id": 1, "name": "lets learn java", "topic": "java"},
   {"id": 2, "name": "lets learn html", "topic": "html"},
  {"id": 3, "name": "lets learn css", "topic": "css"},
]"""


def loginpage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "user not exist")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "user not exist")

    context = {"page": page}
    return render(request, "base/login_register.html", context)


def logoutUser(request):
    logout(request)
    return redirect("home")


def registeruser(request):
    form = signupform
    context = {"form": form}
    if request.method == "POST":
        form = signupform(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "error ocuured during registration")
    return render(request, "base/login_register.html", context)


def home(request):
    q = request.GET.get("q", "")
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )
    rooms_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    topics = Topic.objects.all()
    context = {
        "rooms": rooms,
        "topics": topics,
        "rooms_count": rooms_count,
        "room_messages": room_messages,
    }
    return render(request, "base/home.html", context)


def room(request, pk):
    thisroom = Room.objects.get(id=pk)
    room_messages = thisroom.message_set.all().order_by("-created")
    participants = thisroom.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=thisroom,
            body=request.POST.get("body"),
        )
        thisroom.participants.add(request.user)
        return redirect("room", pk=thisroom.id)

    context = {
        "room": thisroom,
        "room_messages": room_messages,
        "participants": participants,
    }
    return render(request, "base/room.html", context)


@login_required(login_url="login")
def create_room(request):
    form = RoomForm
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": RoomForm}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def update_room(request, pk):

    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse("you are not allowed to do this!")
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("you are not allowed to do this!")
    if request.method == "POST":
        room.delete()
        return redirect("home")
    context = {"obj": room}
    return render(request, "base/delete.html", context)


@login_required(login_url="login")
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    print(message)
    if request.user != room.host:
        return HttpResponse("you are not allowed to do this!")
    if request.method == "POST":
        message.delete()
        return redirect("home")
    context = {"obj": room}
    return render(request, "base/delete.html", context)
