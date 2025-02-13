from django import forms
# from django.contrib.auth.models import User
from accounts.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

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
            
    def clean_password(self):
        password = self.cleaned_data.get('password')

        # ✅ Apply Django’s built-in password validation (length, common, numeric)
        validate_password(password)

        return password

    def clean(self):
        """Ensure both passwords match."""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            self.add_error("password2", "Passwords do not match.")

        return cleaned_data

 
##PASSWORD RRESEET
#SFA

class OTPVerificationForm(forms.Form):
    otp = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'passing-navel', 'class': 'form-control d-none',}))
