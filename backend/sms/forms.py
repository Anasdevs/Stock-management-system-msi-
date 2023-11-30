from django import forms
from .models import IssuedItem

class IssuedForm(forms.ModelForm):
    class meta:
        model = IssuedItem
        fields = '__all__'