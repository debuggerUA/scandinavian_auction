from django import forms

class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))
    
class RegistrationForm(forms.Form):
    login = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))
    confirm_password  = forms.CharField(widget=forms.PasswordInput(render_value=False))

class AdminAddUserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput(render_value = False))
    confirm_password = forms.CharField(widget = forms.PasswordInput(render_value = False))
    email = forms.EmailField()
    is_staff = forms.BooleanField(required = False)
    is_active = forms.BooleanField()
    is_superuser = forms.BooleanField(required = False)
    
