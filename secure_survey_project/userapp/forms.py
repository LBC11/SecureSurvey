from django import forms
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['gender', 'age', 'marriage',
                  'income', 'education', 'job',
                  'phone', 'phone_maker', 'email']
