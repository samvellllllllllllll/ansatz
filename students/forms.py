from django.contrib.auth.forms import UserCreationForm
from django import forms
from courses.models import Course

class MyUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Только буквы, цифры и @/./+/-/_'
        # self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

class CourseEnrollForm(forms.Form):
    course=forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.HiddenInput)