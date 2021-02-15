from datetime import datetime

from django.test import TestCase
from django.urls import reverse

from dct.models import (
    Accumulator, AccumulatorDate
)


class ChangedStatusAccumTest(TestCase):
    """
    Test for mixin class ChangedStatusAccum.
    Checking the battery status change when creating and changing
    the data collection terminal.
    """
    fixtures = ['initial_data.json']

    def test_form_valid_install(self):
        """
        Checking the battery install from the terminal.
        """
        self.client.post(reverse('update_dct_url', kwargs={'pk': 1}),
                         {'name': 'ТСД-1', 'serial_number': 435406234745,
                          'model': 1, 'mac_address': '43:ac:34:db:53:ae',
                          'accumulator': 1})
        new_obj = AccumulatorDate.objects.get(id=2)
        result = [new_obj.accumulator, new_obj.state,
                  new_obj.date.strftime('%Y.%m.%d %I:%M')]
        accum = Accumulator.objects.get(id=1)
        expected = [accum, 1, datetime.today().strftime('%Y.%m.%d %I:%M')]
        self.assertEqual(result, expected)

    def test_form_valid_uninstall(self):
        """
        Checking the battery uninstall from the terminal.
        """
        self.client.post(reverse('update_dct_url', kwargs={'pk': 2}),
                         {'name': 'ТСД-2', 'serial_number': 435406234746,
                          'model': 1, 'mac_address': '43:ac:34:db:53:af'})
        new_obj = AccumulatorDate.objects.get(id=2)
        result = [new_obj.accumulator, new_obj.state,
                  new_obj.date.strftime('%Y.%m.%d %I:%M')]
        accum = Accumulator.objects.get(id=2)
        expected = [accum, 2, datetime.today().strftime('%Y.%m.%d %I:%M')]
        self.assertEqual(result, expected)
