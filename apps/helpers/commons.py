from django.utils.translation import gettext_lazy as _

ADMINISTRATOR = 'adm_access'
COMMOM_USER = 'user_commom_access'


BASE_ACCESS_LEVEL_CHOICES = (
    (ADMINISTRATOR, _('Administrador')),
    (COMMOM_USER, _('Usuário comum')),
)

ACCESS_LEVEL_CHOICES = (
    (ADMINISTRATOR, _('Administrador')),
    (COMMOM_USER, _('Usuário comum')),
)
USER_CLINIC_CHOICES = (
    (ADMINISTRATOR, _('Administrador')),
    (COMMOM_USER, _('Usuário comum')),
)
