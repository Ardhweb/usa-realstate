from django import forms
# from django.contrib.auth.models import User
from accounts.models import User
class LoginForm(forms.Form):
    username = forms.CharField(label='Username',widget=forms.TextInput(attrs={'class':''}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':''}))
    
class SignupForm(forms.ModelForm):
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':''}))
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(attrs={'class':''}))
    class Meta:
        model = User
        fields = ['username','email','member_type','message']
        widgets ={
                'username':forms.TextInput(attrs={'class':''}),
                'email':forms.TextInput(attrs={'class':''}),
                'member_type':forms.HiddenInput(attrs={'class':''}),
            }
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

            
    
    
    
##PASSWORD RRESEET

