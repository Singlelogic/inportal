from datetime import datetime

from django.test import TestCase
from django.urls import reverse

from dct.models import Accumulator, AccumulatorDate


class ChangedStatusAccumTest(TestCase):
    """
    Test for mixin class ChangedStatusAccum.
    Checking whether a battery status change record is created in the database
    when creating and changing the data collection terminal.
    """
    fixtures = ['initial_data.json']

    def test_form_valid_create_dct_without_battery(self):
        """
        Checking whether a battery status change record is created in the
        database when creating a terminal without installing the battery.
        """
        self.client.post(reverse('create_dct_url'),
                         {'name': 'ТСД-3', 'serial_number': 435406234747,
                          'model': 1, 'mac_address': '43:ac:34:db:53:a1'})
        result = AccumulatorDate.objects.filter(id=2)
        self.assertEqual(bool(result), False)

    def test_form_valid_create_dct_with_battery(self):
        """
        Checking whether a battery status change record is created in the
        database when creating a terminal with battery installation.
        """
        self.client.post(reverse('create_dct_url'),
                         {'name': 'ТСД-3', 'serial_number': 435406234747,
                          'model': 1, 'mac_address': '43:ac:34:db:53:a1',
                          'accumulator': 1})
        new_obj = AccumulatorDate.objects.get(id=2)
        result = [new_obj.accumulator, new_obj.state,
                  new_obj.date.strftime('%Y.%m.%d %I:%M')]
        accum = Accumulator.objects.get(id=1)
        expected = [accum, 1, datetime.today().strftime('%Y.%m.%d %I:%M')]
        self.assertEqual(result, expected)

    def test_form_valid_install(self):
        """
        Checking whether a battery status change record is created in the
        database when the battery installing in the terminal.
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
        Checking whether a battery status change record is created in the
        database when the battery uninstalling from the terminal.
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

    def test_form_valid_change_accum(self):
        """
        Checking whether a battery status change record is created in
        the database when a battery is replaced with another battery.
        """
        self.client.post(reverse('update_dct_url', kwargs={'pk': 2}),
                         {'name': 'ТСД-2', 'serial_number': 435406234746,
                          'model': 1, 'mac_address': '43:ac:34:db:53:af',
                          'accumulator': 1})
        new_obj_uninstall = AccumulatorDate.objects.get(id=2)
        new_obj_install = AccumulatorDate.objects.get(id=3)
        result = [new_obj_uninstall.accumulator, new_obj_uninstall.state,
                  new_obj_uninstall.date.strftime('%Y.%m.%d %I:%M'),
                  new_obj_install.accumulator, new_obj_install.state,
                  new_obj_install.date.strftime('%Y.%m.%d %I:%M')]
        accum_uninstall = Accumulator.objects.get(id=2)
        accum_install = Accumulator.objects.get(id=1)
        expected = [accum_uninstall, 2, datetime.today().strftime('%Y.%m.%d %I:%M'),
                    accum_install, 1, datetime.today().strftime('%Y.%m.%d %I:%M')]
        self.assertEqual(result, expected)

    def test_form_valid_without_change_without_battery(self):
        """
        Checking whether a battery status change record is created
        in the database when changing a terminal without a battery.
        """
        self.client.post(reverse('update_dct_url', kwargs={'pk': 1}),
                         {'name': 'ТСД-1', 'serial_number': 435406234745,
                          'model': 1, 'mac_address': '43:ac:34:db:53:ae'})
        result = AccumulatorDate.objects.filter(id=2)
        self.assertEqual(bool(result), False)

    def test_form_valid_without_change_without_battery(self):
        """
        Checking whether a battery status change record is created
        in the database when changing a terminal with a battery.
        """
        self.client.post(reverse('update_dct_url', kwargs={'pk': 2}),
                         {'name': 'ТСД-2', 'serial_number': 435406234746,
                          'model': 1, 'mac_address': '43:ac:34:db:53:af',
                          'accumulator': 2})
        result = AccumulatorDate.objects.filter(id=2)
        self.assertEqual(bool(result), False)
