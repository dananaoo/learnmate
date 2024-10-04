from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Room, Topic, Messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .form import RoomForm

def log(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        user=authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Password is wrong')

    context={'page':page}
    return render(request, 'base/login_register.html', context )

def logou(request):
    logout(request)
    return redirect('home')

def rega(request):
    form=UserCreationForm()

    if request.method =='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Error occured during registration')

    context={'form':form}
    return render(request, 'base/login_register.html', context)

def home(request):
    q=request.GET.get('q') if request.GET.get('q') !=None else ''
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q)| #icontains means it is not case sensetive so it will give all objects that has that value even though you write only first 3 letters
        Q(name__icontains=q) |
        Q(description__icontains=q) 
        )
    
    topics=Topic.objects.all()
    room_messages=Messages.objects.filter(Q(room__topic__name__icontains=q))
    room_count=rooms.count()

    context={'rooms':rooms, 'topics':topics, 'room_count': room_count, 'room_messages':room_messages}  #it will give these variable's values with a name in '' to home.html to work with
    return render(request, 'base/home.html', context )

def room(request, ids):
    rooms =Room.objects.get(id=ids)
    rooms_messages=rooms.messages_set.all()
    participants= rooms.participants.all()

    if request.method =='POST':
        message=Messages.objects.create(
            user=request.user,
            room=rooms,
            body=request.POST.get('body')
        )
        rooms.participants.add(request.user)
        return redirect('room', ids=rooms.id)

    
    context={'room':rooms, 'rooms_messages': rooms_messages, 'participants': participants}
    return render(request, 'base/room.html', context)

def userProfile(request, ids):
    user= User.objects.get(id=ids)
    rooms=user.room_set.all()
    room_messages=user.messages_set.all()
    topics=Topic.objects.all()
    context ={'user': user, 'rooms': rooms,'room_messages': room_messages, 'topics':topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form=RoomForm()
    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host= request.user
            room.save()
            return redirect('home')
    context={'form':form}
    return render(request, 'base/room_form.html', context )

@login_required(login_url='login')
def updateRoom(request,  ids):
    room=Room.objects.get(id=ids)
    form=RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You do not have such access, you can edit only the rooms you have created')
    if request.method=='POST':
        form=RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, ids):
    room=Room.objects.get(id=ids)

    if request.user != room.host:
        return HttpResponse('You do not have such access, you can delete only the rooms you have created')

    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'object':room})

@login_required(login_url='login')
def deleteMessage(request, ids):
    message=Messages.objects.get(id=ids)

    if request.user != message.user:
        return HttpResponse('You do not have such access, you can delete only the rooms you have created')

    if request.method=='POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'object':message})