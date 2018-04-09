# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import User
from django.shortcuts import render, redirect
from django.contrib import messages



def index(request):
    return render(request, "beltapp/index.html")


def create(request):
    result = User.objects.my_validation(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/')        
    request.session['user_id'] = result.id
    messages.success(request, "Successfully Registered")
    return redirect('/friends')

def login(request):
    result = User.objects.my_validation_2(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/')
    
    request.session['user_id'] = result.id
    #messages.success(request, "Thanks for logging in!")
    return redirect('/friends')

def display(request):
    try:
        request.session['user_id']
    except:
        return redirect('/')
    usrid = request.session['user_id']
    currentuser = User.objects.get(id=usrid)
    #friendlist = Friendship.objects.get_friends(request.POST)
    allusers = {
        'user': currentuser,
        'friends': User.objects.all().filter(friendships=currentuser),
        'nonfriends': User.objects.all().exclude(friendships=currentuser)
        
    }   
  
    
    
    

    return render(request, "beltapp/friends.html", allusers)

def add_friend(request, friend_id):
    usrid = request.session['user_id']
    new_friend = User.objects.get(id=friend_id)
    this_user = User.objects.get(id=usrid)
    this_user.friendships.add(new_friend)

    return redirect('/friends')

def remove_friend(request, friend_id): 
    usrid = request.session['user_id'] 
    del_friend = User.objects.get(id=friend_id)
    this_user = User.objects.get(id=usrid)
    this_user.friendships.remove(del_friend)

    
    return redirect('/friends')

def user(request, friend_id):
    thisuser = {
        'user': User.objects.get(id=friend_id)#!! make sure user.id is coming from the right place
    }
    
    return render(request, "beltapp/user.html", thisuser) #where is the correct user coming from?

def logout(request):
    request.session.clear()
    return render(request, "beltapp/index.html")