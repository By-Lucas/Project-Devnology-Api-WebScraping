from urllib.parse import uses_relative
from django.conf import settings

from accounts.others_models.model_profile import UserProfile
from clinic.models.model_clinic import Clinic


def get_clinic(request):
    try:
        clinic = Clinic.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor=vendor)

def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = None
    return dict(user_profile=user_profile)
