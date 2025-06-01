from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class customUserManager (BaseUserManager):
    def create_user(self, username, password, **kwargs):
        if not username:
            raise ValueError ("username is required")
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save(using = self._db)
        return user
    def get_by_natural_key(self, username):
        return self.get(username=username)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=50)

    objects = customUserManager()

    USERNAME_FIELD = "username"