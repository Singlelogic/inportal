from django import forms

from .models import DataCollectTerminal


class DataCollectTerminalForm(forms.ModelForm):
    class Meta:
        model = DataCollectTerminal
        fields = ['name', 'model', 'serial_number', 'mac_address', 'user',
                  'accumulator', 'remark']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'ТСД-1'}),
        }