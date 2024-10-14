from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Tarifa

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

class PaymentForm(forms.Form):
    TIPO_TARIFA_CHOICES = [
        ('Pagar día', 'Pagar día'),
        ('Pagar hora', 'Pagar hora'),
        ('Recargar saldo', 'Recargar saldo'),
    ]

    tipo_tarifa = forms.ChoiceField(choices=TIPO_TARIFA_CHOICES, required=True)
    saldo = forms.DecimalField(label='Monto a depositar', max_digits=10, decimal_places=2, required=False)
    card_number = forms.CharField(label='Número de Tarjeta', max_length=16, required=False)
    card_expiry = forms.CharField(label='Fecha de Expiración (MM/AA)', max_length=5, required=False)
    card_cvc = forms.CharField(label='CVC', max_length=3, required=False)

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Realizar Pago'))

    def clean(self):
        cleaned_data = super().clean()
        tipo_tarifa = cleaned_data.get('tipo_tarifa')

        if tipo_tarifa == 'Recargar saldo':
            if not cleaned_data.get('saldo'):
                self.add_error('saldo', 'Este campo es requerido.')
            if not cleaned_data.get('card_number'):
                self.add_error('card_number', 'Este campo es requerido.')
            if not cleaned_data.get('card_expiry'):
                self.add_error('card_expiry', 'Este campo es requerido.')
            if not cleaned_data.get('card_cvc'):
                self.add_error('card_cvc', 'Este campo es requerido.')

        return cleaned_data