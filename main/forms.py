from unittest.util import _MAX_LENGTH
from django import forms

class order_form(forms.Form):
    shipping_address = forms.CharField(max_length=100)