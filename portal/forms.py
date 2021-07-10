from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from allauth.account.forms import ChangePasswordForm,SetPasswordForm,ResetPasswordForm,AddEmailForm
from .models import UserProfile
from django.contrib.auth.models import User


class MemberChangePasswordForm(ChangePasswordForm):
    def clean(self):
        raise ValidationError(_('You cannot change password.'))


class MemberSetPasswordForm(SetPasswordForm):
    def clean(self):
        raise ValidationError(_('You cannot set password.'))


class MemberResetPasswordForm(ResetPasswordForm):
    def clean(self):
        raise ValidationError(_('You cannot reset password.'))


class MemberAddEmailForm(AddEmailForm):
    def clean(self):
        raise ValidationError(_('You cannot add an email.'))