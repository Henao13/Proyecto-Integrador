# parking/forms.py

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class LoginForm(forms.Form):
    id_vehiculo = forms.CharField(label='Placa')
    contraseña = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Login'))

class SaldoForm(forms.Form):
    saldo = forms.DecimalField(max_digits=10, decimal_places=2, label='Saldo a depositar')

    def __init__(self, *args, **kwargs):
        super(SaldoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Añadir saldo'))