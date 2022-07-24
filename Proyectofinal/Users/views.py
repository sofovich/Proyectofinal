from django.shortcuts import render, redirect
from django.urls.base import reverse

from .models import *
from .forms import *


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test


from django.db.models import Q



def login_request(request):

      if request.method == "POST":
            form = AuthenticationForm(request=request, data = request.POST)

            if form.is_valid():
                  usuario = form.cleaned_data.get('username')   
                  contra = form.cleaned_data.get('password')

                  user = authenticate(username=usuario, password=contra)   

                  if user is not None:         
                        login(request, user)
                        return render(request,"BlogApp/home.html",  {"mensaje":f"Welcome to the blog, {usuario}"})   
                  else:
                        return render(request,"Users/login.html", {"form":form, "mensaje":"Error, the user name is incorrect. Please, login again"})   

            else:
                        return render(request,"Users/login.html" ,  {"form":form, "mensaje":"Error, the entered data is invalid. Please, login again"})  

      form = AuthenticationForm()    
      return render(request,"Users/login.html", {'form':form})


def register(request):

      if request.method == 'POST':
            form = UserRegisterForm(data=request.POST)
            if form.is_valid():
                  new_user = form.save()
                  login(request, new_user)
                  return redirect(reverse('users:Profile', args=[id]))
            else:
                return render(request, 'Users/register.html', {"form":form, "mensaje": "The user could not be created. Please try again"})
      
      else:      
            form = UserRegisterForm()     
      return render(request, 'Users/register.html',  {"form":form})




@login_required
def editProfile(request):

      user = request.user
   
      try:
          avatar = Avatar.objects.get(user=request.user.id)
          avatar = avatar.avatar.url
      except:
          avatar = ''
     
      if request.method == 'POST':
            myForm = UserEditForm(request.POST, instance=user) 
            if myForm.is_valid():

                  info = myForm.cleaned_data
         
                  user.username = info['username']
                  user.email = info['email']
                  user.first_name = info['first_name']
                  user.last_name = info['last_name']
                  user.password1 = info['password1']
                  user.password2 = info['password1']
                  user.save()

                  return redirect(reverse('users:Profile', args=[id]))
            else:
                return render(request, 'Users/edit_profile.html', {"myform":myForm, "mensaje": "The user could not be updated. Please try again"})

      else: 
            myForm= UserEditForm(initial={'username':user.username, 'email':user.email, 'first_name':user.first_name, 'last_name':user.last_name}) 
      return render(request, 'Users/edit_profile.html', {"myForm":myForm, "user":user})  




@login_required
def profile(request, user_id):
    
    user = request.user
   
    try:
        avatar = Avatar.objects.get(user=request.user.id)
        avatar = avatar.avatar.url
    except:
        avatar = ''

    context = {'user': user, 'avatar': avatar, 'title': 'Profile'}
    return render(request, 'Users/profile.html', context)


@user_passes_test(lambda u: u.is_superuser)   
def editAvatar(request):
    
    user = request.user

    try:
        avatar = Avatar.objects.get(user=request.user.id)
        avatar = avatar.avatar.url
    except:
        avatar = ''

    if request.method == 'POST':
        form_avatar= AvatarForm(request.POST, request.FILES, instance=user)
        if form_avatar.is_valid():
            u = User.objects.get(username=request.user)
            new_avatar = Avatar(user=u, avatar=form_avatar.cleaned_data['avatar'])
            new_avatar.save()
            return redirect(reverse('users:Profile', args=[id]))
        else:
            return render(request, 'Users/edit_avatar.html', {"form_avatar":form_avatar, "mensaje": "The avatar could not be updated. Please try again"})
    else:
        form_avatar= AvatarForm()
    return render (request, 'Users/edit_avatar.html', {"form_avatar":form_avatar, "avatar":avatar})



@login_required
def messages(request):
    
    user = request.user
    try:
        avatar = Avatar.objects.get(user=request.user.id)
        avatar = avatar.avatar.url
    except:
        avatar = ''
    
    messages = Messages.objects.filter(Q(receiver=user) | Q(sender=user)).order_by('-sent_at')
    received = messages.filter(receiver=user).order_by('-sent_at')
    sent = messages.filter(sender=user).order_by('-sent_at')

    context = {'title': 'Inbox', 'user': user, 'messages': messages, 'received': received, 'sent':sent, 'avatar': avatar}
    return render(request, 'Users/messages.html', context)


@login_required
def new_message(request):
    
    user = request.user
    try:
        avatar = Avatar.objects.get(user=request.user.id)
        avatar = avatar.avatar.url
    except:
        avatar = ''

    if request.method != 'POST':
        form = MessageForm()
    else:
        form = MessageForm(data=request.POST)
        if form.is_valid():

            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
            return redirect ('blogapp:Messages')
    
    context = {'form': form,'title': 'New message','avatar':avatar}
    return render(request, 'Users/new_msg.html', context)
