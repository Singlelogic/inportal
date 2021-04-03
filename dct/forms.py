from django import forms

from .models import DataCollectTerminal


class DataCollectTerminalCreateForm(forms.ModelForm):
    class Meta:
        model = DataCollectTerminal
        fields = ['name', 'model', 'serial_number', 'mac_address', 'user',
                  'accumulator', 'debited', 'repair', 'remark']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'ТСД-1'}),
        }


class DataCollectTerminalUpdateForm(forms.ModelForm):
    name = forms.CharField(label='Наименование', disabled=True)

    class Meta:
        model = DataCollectTerminal
        fields = ['name', 'model', 'serial_number', 'mac_address', 'user',
                  'accumulator', 'debited', 'repair', 'remark']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'ТСД-1'}),
        }
