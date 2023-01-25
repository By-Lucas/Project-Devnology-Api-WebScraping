from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext as _

from helpers import commons
from accounts.models import User
from accounts.others_models.model_user_clinic import UserClinic


def admin_level_required(view_func):
    def _decorator(request, *args, **kwargs):
        if request.user.user_clipse or request.user.is_superuser:
            response = view_func(request, *args, **kwargs)
            return response

        try:
            user_clinic_permission = UserClinic.objects.get(user=request.user, user__is_active=True)

        except :
            user_clinic_permission = UserClinic.objects.filter(user=request.user, user__is_active=True).first()

        if user_clinic_permission.permission == commons.ADMINISTRATOR or request.user.user_clipse or request.user.is_superuser:
            response = view_func(request, *args, **kwargs)
            return response
        else:
            messages.warning(request, _('Você não tem permissão pra acessar o recurso'))
            return redirect('home')

    return wraps(view_func)(_decorator)


def admin_clipse_level_required(view_func):
    def _decorator(request, *args, **kwargs):
        if request.user.user_clipse or request.user.is_superuser:
            response = view_func(request, *args, **kwargs)
            return response

        else:
            messages.warning(request, _('Você não tem permissão pra acessar o recurso.'))
            return redirect('home')

    return wraps(view_func)(_decorator)


def customer_level_required(view_func):
    def _decorator(request, *args, **kwargs):
        if request.user.user_clipse or request.user.is_superuser:
            response = view_func(request, *args, **kwargs)
            return response
        try:
            user_clinic_permission = UserClinic.objects.get(user=request.user, user__is_active=True)

        except UserClinic.MultipleObjectsReturned or UserClinic.DoesNotExist:
            user_clinic_permission = UserClinic.objects.filter(user=request.user, user__is_active=True).first()
            
        if user_clinic_permission.permission == commons.ADMINISTRATOR or user_clinic_permission.permission == commons.COMMOM_USER or request.user.user_clipse or request.user.is_superuser:
            response = view_func(request, *args, **kwargs)
            return response
        else:
            messages.warning(request, _('Você não tem permissão pra acessar o recurso.'))
            return redirect('home')

    return wraps(view_func)(_decorator)
