from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import * 


class OperatorAccountForm(UserCreationForm):
    # email=forms.EmailField(max_length=100)
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
        exclude = ['id']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'phone', 'address', 'mail', 'avatar_id']
        exclude = ['id', 'created_at', 'updated_at', 'contributions', 'contributions_count']

class TextBookForm(forms.ModelForm):
    class Meta:
        model = TextBook
        fields = ['title', 'author', 'description', 'cover', 'file']
        exclude = ['id', 'created_at', 'updated_at', 'special_id', 'level', 'publisher', 'category']

class PastQuestionForm(forms.ModelForm):
    class Meta:
        model = PastQuestion
        fields = '__all__'

class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = '__all__'

class ThesisForm(forms.ModelForm):
    class Meta:
        model = Thesis
        fields = '__all__'

class DissertationForm(forms.ModelForm):
    class Meta:
        model = Dissertation
        fields = '__all__'



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
