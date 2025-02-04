from django import forms
# from django.contrib.auth.models import User
from accounts.models import User

class LoginForm(forms.Form):
    username_or_email = forms.CharField(label='Username or Email',widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
class SignupForm(forms.ModelForm):
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control', "id":"nomd_deS8"}))
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(attrs={'class':'form-control',"id":"disci_R6"}))
    class Meta:
        model = User
        fields = ['username','email','member_type','message']
        widgets ={
                'username':forms.TextInput(attrs={'class':'form-control w-100'}),
                'email':forms.EmailInput(attrs={'class':'form-control'}),
                'member_type':forms.HiddenInput(attrs={'class':'form-control','id':'member_type_vale'}),
                'message':forms.Textarea(attrs={'class':'form-control','rows':'3'}),
            }
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
 
##PASSWORD RRESEET
#SFA

class OTPVerificationForm(forms.Form):
    otp = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'passing-navel', 'class': 'form-control d-none',}))
