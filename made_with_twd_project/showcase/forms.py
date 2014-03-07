__author__ = 'leif'
from django.contrib.auth.models import User
from django import forms
from models import Team, Rating, Demo


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username','email','password')


class TeamForm(forms.ModelForm):
    name = forms.CharField(label='Team Name', widget=forms.TextInput(attrs={'size':'64','maxlength':'512'}))
    logo = forms.ImageField(label='Logo')
    members = forms.CharField(label='Team Members',widget=forms.TextInput(attrs={'size':'128','maxlength':'512'}))
    photo = forms.ImageField(label='Photo of Team Members')


    class Meta:
        model = Team
        exclude = ('user',)


class RatingForm(forms.ModelForm):

    class Meta:
        model = Rating
        exclude = ('rater','demo',)

class DemoForm(forms.ModelForm):

    class Meta:
        model = Demo
        exclude = ('team','rating_count','rating_sum',)
