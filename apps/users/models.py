from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        HSE_MANAGER = 'HSE_MANAGER', 'HSE_Manager'
        HSE_SUPERVISOR = 'HSE_SUPERVISOR', 'HSE_Supervisor'
        HSE_OFFICER = 'HSE_OFFICER', 'HSE_Officer'

    # Make email unique
    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.HSE_OFFICER
    )
    
    supervisor = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={'role':'HSE_SUPERVISOR'},
        related_name='officers'
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  # username is still required by AbstractUser

    def __str__(self):
        return f'{self.username} ({self.role})'