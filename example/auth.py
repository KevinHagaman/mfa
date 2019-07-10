from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import auth
from django.conf import settings

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
        if request.session.get("mfa",{}).get("verified",False)  and getattr(settings,"MFA_QUICKLOGIN",False):
            if request.session["mfa"]["method"]!="Trusted Device":
                response.set_cookie("base_username", request.user.username, path="/",max_age = 15*24*60*60)
        return response
    else:
        if "mfa" in settings.INSTALLED_APPS and getattr(settings,"MFA_QUICKLOGIN",False) and request.COOKIES.get('base_username'):
            username=request.COOKIES.get('base_username')
            from mfa.helpers import has_mfa
            res =  has_mfa(username = username,request=request,)
            if res: return res
            ## continue and return the form.
    return render(request, "login.html", context)
'''
def loginView(request): # this function handles the login form POST
    username = request.user.username
    user = auth.authenticate(username=username, password=password)  
    if user is not None: # if the user object exist
         from mfa.helpers import has_mfa
         res =  has_mfa(username = username,request=request) # has_mfa returns false or HttpResponseRedirect
         if res:
             return res
         return log_user_in(request,username=user.username) 
         #log_user_in is a function that handles creatung user session, it should be in the setting file as MFA_CALLBACK
         '''
def create_session(request,username):
    user=User.objects.get(username=username)
    user.backend='django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return HttpResponseRedirect(reverse('home'))


def logoutView(request):
    logout(request)
    return  render(request,"logout.html",{})