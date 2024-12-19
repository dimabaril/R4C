from django import forms


class OrderForm(forms.Form):
    customer_email = forms.EmailField(required=True)
    model = forms.CharField(max_length=2, required=True)
    version = forms.CharField(max_length=2, required=True)
