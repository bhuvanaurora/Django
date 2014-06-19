from django import forms
from rango.models import Page, Category
from rango.models import UserProfile
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="please enter the category")
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    
    class Meta:
        model = Category
    
class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="please enter the title")
    url = forms.URLField(max_length=200, help_text="please enter url of the page")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    
    class Meta:
        model = Page
        fields = ('title', 'url', 'views')
        
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
        
        return cleaned_data

class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="please enter a username")
    email = forms.CharField(help_text="please enter your email")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="please enter a password")
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    website = forms.URLField(help_text="please enter your website", required=False)
    picture = forms.ImageField(help_text="please upload a profile picture", required=False)
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')