from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
'''
def loginView(request):
    context={}
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(username=username,password=password)
        if user:
            from mfa.helpers import has_mfa
            res = has_mfa(username = username, request = request)  # has_mfa returns false or HttpResponseRedirect
            if res:
                return res
            return create_session(request,user.username)
        context["invalid"]=True
    return render(request, "login.html", context)
'''
def loginView(request): # this function handles the login form POST
    user = auth.authenticate(username=username, password=password)  
    if user is not None: # if the user object exist
         from mfa.helpers import has_mfa
         res =  has_mfa(username = username,request=request) # has_mfa returns false or HttpResponseRedirect
         if res:
             return res
         return log_user_in(request,username=user.username) 
         #log_user_in is a function that handles creatung user session, it should be in the setting file as MFA_CALLBACK
def create_session(request,username):
    user=User.objects.get(username=username)
    user.backend='django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return HttpResponseRedirect(reverse('home'))


def logoutView(request):
    logout(request)
    return  render(request,"logout.html",{})