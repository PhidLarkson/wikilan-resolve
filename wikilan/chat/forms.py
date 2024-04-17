from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from .models import *

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ["name","description"]
        
class MessageForm(forms.ModelForm):    
        class Meta:
            model = Message
            fields = ["content"]

class ThreadForm(forms.ModelForm):
    class Meta:
        model = MessageThread
        fields = ["content"]
        exclude = ['user','timestamp','key']

class ThreadReplyForm(forms.ModelForm):
    class Meta:
        model = ThreadReply
        fields = ["content"]
        exclude = ['thread','user','timestamp']
