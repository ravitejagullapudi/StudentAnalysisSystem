from django import  forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Teacher

class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username','password1','password2','first_name','last_name','email')

DEPARTMENT=[
    ('IT','IT'),
    ('CSE','CSE'),
    ('ECE','ECE'),
    ('MEC','MECH'),
    ('EEE','EEE'),
    ('CIV','CIVIL'),
    ('ALL','ALL Departments'),
]

class ProfileForm(forms.Form):
    department = forms.CharField(widget=forms.Select(choices=DEPARTMENT))
    mobile = forms.IntegerField()
    teac_id= forms.IntegerField()
    class Meta:
        model = Teacher
        fields = ('user_id','mobile','department','teac_id')

class LoginForm(forms.Form):
    username=forms.CharField(max_length=50)
    password=forms.CharField(widget= forms.PasswordInput)
    class Meta:
        model=User
        fields=('username','password')
