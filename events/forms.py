from django import forms
from django.contrib.auth.models import User
from .models import Event , Booking ,Profile

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['organizer']

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type':'time'}),
            'seats':forms.NumberInput(attrs={'type': 'number'}),                  
        }
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['guest','event',]

        widgets = {
            'seats': forms.NumberInput(attrs={'type': 'number'}),                  
        }        


class UserSignup(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ,'password']

        widgets={
        'password': forms.PasswordInput(),
        }


class UserLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())


class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        exclude = ['user','following']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),                 
        }    
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields = ['username', 'first_name', 'last_name', 'email' ,]