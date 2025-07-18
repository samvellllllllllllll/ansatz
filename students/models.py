from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.conf import settings
import random
import string

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField('email', unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    is_email_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    class Meta:
        ordering = ('email',)
        
    def __str__(self):
        return self.email

class ConfirmationCode(models.Model):
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    email=models.EmailField('email address', unique=True)
    code = models.CharField(max_length=6, verbose_name='Код подтверждения')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    def is_valid(self):
        expiration_time = timezone.now() - timezone.timedelta(
            minutes=settings.CONFIRMATION_CODE_EXPIRE_MINUTES)
        return self.created_at >= expiration_time
    
    @classmethod
    def generate_code(cls, email):
        # Удаляем старые коды пользователя
        cls.objects.filter(email=email).delete()
        
        # Генерируем 6-значный цифровой код
        code = ''.join(random.choices(string.digits, k=6))
        return cls.objects.create(email=email, code=code)
    
    class Meta:
        verbose_name = 'Код подтверждения'
        verbose_name_plural = 'Коды подтверждения'
        ordering = ['-created_at']

    def __str__(self):
        return f'Код {self.code} для {self.user.email}'