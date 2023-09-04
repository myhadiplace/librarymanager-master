from django import forms
from .models import Book, Users, Author, Reservation,GENERS
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
import django_filters
from datetime import datetime, timedelta

class NewBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields ="__all__"
        # labels = {
        #     "nick_name":"Player Name",
        #     "born": "Date of Birth",
        #     "foot":"Foot",
        #     'current_club':"Current Club",
        #     "player_image":"Player Image"
        # }
        error_messages = {
            "title":{
                "required":"title must not be empty"
            },
            "ISBN" : {
                "required":"ISBN must not be empty"
            },
            "book_image":{
                "required":"image must not be empty"
            }
        }

class NewAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = "__all__"


class NewUserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = "__all__"
        error_messages = {
            "full_name":{
                "required":"name must not be empty"
            },
            "username" : {
                "required":"username must not be empty",
                'unique': 'this username already been taken'
            },
            "password":{
                "required":"password must not be empty"
            }
        }

class LoginUserForm(forms.Form):
    username = forms.CharField(label="username",max_length=30,widget=forms.TextInput(attrs={'placeholder': 'username'}))
    password = forms.CharField(label='password',max_length=50,widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    

class OtpLoginForm(forms.Form):
    otp_number_field = forms.IntegerField(label='authenticate number',min_value=1000,max_value=9999)
    

class BookFilterForm(forms.Form):
    gener_choices = [('','ALL')] + GENERS
    geners = forms.ChoiceField(choices=gener_choices,required=False)
    price_min = forms.DecimalField(required=False)
    price_max = forms.DecimalField(required=False)
    author_country = CountryField().formfield(required=False,widget=CountrySelectWidget(attrs={'class': 'custom-class'}))


class NormalDateReseveForm(forms.Form):
    DATE_CHOICES = [(num+1,f'{num+1} days') for num in range(7)]
    user_token = forms.CharField(max_length=400,widget=forms.HiddenInput())
    book_name = forms.CharField(max_length=200,widget=forms.HiddenInput())
    reserve_date = forms.ChoiceField(choices=DATE_CHOICES, widget=forms.Select)

class VipDateReseveForm(forms.Form):
    DATE_CHOICES = [(num+1,f'{num+1} days') for num in range(14)]
    user_token = forms.CharField(max_length=400,widget=forms.HiddenInput())
    book_name = forms.CharField(max_length=200,widget=forms.HiddenInput())
    reserve_date = forms.ChoiceField(label='reserve for',choices=DATE_CHOICES, widget=forms.Select)



