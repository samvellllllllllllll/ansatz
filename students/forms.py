from django.contrib.auth.forms import UserCreationForm
from django import forms
from courses.models import Course
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# class MyUserCreationForm(UserCreationForm):
#     def __init__(self, *args, **kwargs):
#         super(UserCreationForm, self).__init__(*args, **kwargs)
#         self.fields['username'].help_text = 'Только буквы, цифры и @/./+/-/_'
#         # self.fields['password1'].help_text = ''
#         self.fields['password2'].help_text = ''

# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(
#         label=_("email"),
#         max_length=254,
#         widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'})
#     )
#     first_name = forms.CharField(
#         label=_("Имя"),
#         max_length=30,
#         required=True,
#         widget=forms.TextInput(attrs={'class': 'form-control'})
#     )
#     last_name = forms.CharField(
#         label=_("Фамилия"),
#         max_length=30,
#         required=True,
#         widget=forms.TextInput(attrs={'class': 'form-control'})
#     )
    
#     class Meta:
#         model = User
#         fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
    
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if User.objects.filter(email=email).exists():
#             raise ValidationError(_("Этот email уже используется."))
#         return email
    
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.username = self.cleaned_data['email']
#         if commit:
#             user.save()
#         return user
    
class CourseEnrollForm(forms.Form):
    course=forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.HiddenInput)

from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import CustomUser

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}),
        min_length=8,
        max_length=128,
        label="Пароль"
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}),
        min_length=8,
        max_length=128,
        label="Подтверждение пароля"
    )
    
    class Meta:
        model = CustomUser
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Введите ваш email'})
        }
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже зарегистрирован.')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise ValidationError('Пароли не совпадают')
        
        try:
            validate_password(password)
        except ValidationError as e:
            raise ValidationError({'password': e.messages})
        
        return cleaned_data

class EmailVerificationForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput()
    )