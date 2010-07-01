from django import forms

class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))
    
class RegistrationForm(forms.Form):
    login = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))
    confirm_password  = forms.CharField(widget=forms.PasswordInput(render_value=False))
