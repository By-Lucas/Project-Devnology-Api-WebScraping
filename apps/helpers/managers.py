from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def _create_user(self, name, username, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('O e-mail é obrigatório')
        
        if not username:
            raise ValueError(_('O nome de usuário deve ser definido'))

        email = self.normalize_email(email)
        user = self.model(name=name,  email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name, email, password=None, username=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(full_name=name, email=email, password=password, username=username, **extra_fields)

    def create_superuser(self, name, email, password, username=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Super usuário precisa ter is_superuser=True')

        return self._create_user(name=name, email=email, password=password, username=username, **extra_fields)
