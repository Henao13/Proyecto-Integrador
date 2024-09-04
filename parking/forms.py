from django import forms

class LoginForm(forms.Form):
    placa = forms.CharField()
    contraseña = forms.CharField(widget=forms.PasswordInput)