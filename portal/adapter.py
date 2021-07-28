from django.urls import reverse
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.exceptions import ValidationError
from .models import UserProfile
from django.contrib.auth.models import User
from allauth.account.utils import perform_login

class MyAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        if request.path.rstrip("/") == reverse("account_signup").rstrip("/"):
            return False
        return True

    def get_login_redirect_url(self, request):
        if UserProfile.objects.get(user=request.user).classOf==None:
            print(UserProfile.objects.get(user=request.user).classOf==None)
            return "/users/info/"

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def validate_disconnect(self, account, accounts):
        raise ValidationError("Can't disconnect.")

    def is_open_for_signup(self, request, sociallogin):
        u = sociallogin.user
        return u.email.split('@')[1] == "sas.edu.sg"

    def pre_social_login(self, request, sociallogin): 
        user = sociallogin.user
        if user.id:  
            return          
        try:
            existingUser = User.objects.get(email=user.email)  # if user exists, connect the account to the existing account and login
            sociallogin.state['process'] = 'connect'                
            perform_login(request, existingUser, 'none')
        except User.DoesNotExist:
            pass