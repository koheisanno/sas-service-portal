from django.urls import reverse
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.exceptions import ValidationError
from .models import UserProfile
from django.contrib.auth.models import User
from allauth.account.utils import perform_login
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import render


class MyAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        if request.path.rstrip("/") == reverse("account_signup").rstrip("/"):
            return False
        return True

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def validate_disconnect(self, account, accounts):
        raise ValidationError("Can't disconnect.")

    def pre_social_login(self, request, sociallogin): 
        user = sociallogin.user
        if user.email.split('@')[1] != "sas.edu.sg":
            raise ImmediateHttpResponse(render(request, "account/signup_closed.html"))
        if user.id:  
            return          
        try:
            existingUser = User.objects.get(email=user.email)  # if user exists, connect the account to the existing account and login
            sociallogin.state['process'] = 'connect'                
            perform_login(request, existingUser, 'none')
        except User.DoesNotExist:
            pass