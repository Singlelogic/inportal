import re

from django import forms
from django.core import validators

from .models import DataCollectTerminal


class DataCollectTerminalCreateForm(forms.ModelForm):
    name = forms.CharField(label='Наименование',
                           validators=[validators.RegexValidator(regex='^ТСД-\d+$')],
                           error_messages={'invalid': 'Некорректное название (пример названия: ТСД-1)'},
                           widget=forms.TextInput(attrs={'placeholder': 'ТСД-1'}))

    class Meta:
        model = DataCollectTerminal
        fields = ['name', 'model', 'serial_number', 'mac_address', 'user',
                  'accumulator', 'debited', 'repair', 'remark']
        help_texts = {
            'accumulator': 'Исключены списанные и привязанные к другим ТСД аккумуляторы',
            'user': 'Исключены пользователи, к которым привязаны другие ТСД'
        }
        error_messages = {
            'name': {'unique': 'ТСД с таким наименованием уже существует.'},
            'serial_number': {'unique': 'ТСД с таким серийным номером уже существует.'},
            'mac_address': {'unique': 'ТСД с таким MAC-адресом уже существует.'}
        }

    def clean_mac_address(self):
        """Validation of the mac address."""
        mac_address = self.cleaned_data['mac_address']
        pattern = r"([0-9a-fA-F]{2}(:|$)){6}$"
        print(re.match(pattern, mac_address))
        if re.match(pattern, mac_address):
            return mac_address
        raise forms.ValidationError('Некорректный MAC-адрес')


class DataCollectTerminalUpdateForm(forms.ModelForm):
    name = forms.CharField(label='Наименование', disabled=True)

    class Meta:
        model = DataCollectTerminal
        fields = ['name', 'model', 'serial_number', 'mac_address', 'user',
                  'accumulator', 'debited', 'repair', 'remark']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'ТСД-1'}),
        }
        help_texts = {
            'accumulator': 'Исключены списанные и привязанные к другим ТСД аккумуляторы',
            'user': 'Исключены пользователи, к которым привязаны другие ТСД'
        }
        error_messages = {
            'serial_number': {'unique': 'ТСД с таким серийным номером уже существует.'},
            'mac_address': {'unique': 'ТСД с таким MAC-адресом уже существует.'}
        }

    def clean_mac_address(self):
        """Validation of the mac address."""
        mac_address = self.cleaned_data['mac_address']
        pattern = r"([0-9a-fA-F]{2}(:|$)){6}$"
        print(re.match(pattern, mac_address))
        if re.match(pattern, mac_address):
            return mac_address
        raise forms.ValidationError('Некорректный MAC-адрес')
