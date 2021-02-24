from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from dct.models import (
    Accumulator, AccumulatorDate, DataCollectTerminalRemark,
    DataCollectTerminal
)


class ModifiedMethodFormValidMiximTest(TestCase):
    """
    Test for mixin class ChangedStatusAccum.
    Checking whether a battery status change record is created in the database
    when creating and changing the data collection terminal.
    """
    fixtures = ['initial_data.json']

    # Tests for 'change_status_accum' method
    def test_create_dct_without_battery(self):
        """
        Checking whether a battery status change record is created in the
        database when creating a terminal without installing the battery.
        """
        self.client.post(reverse('create_dct_url'),
                         {'name': 'ТСД-3', 'serial_number': 435406234747,
                          'model': 1, 'mac_address': '43:ac:34:db:53:a1'})
        result = AccumulatorDate.objects.filter(id=2)
        self.assertEqual(bool(result), False)

    def test_create_dct_with_battery(self):
        """
        Checking whether a battery status change record is created in the
        database when creating a terminal with battery installation.
        """
        self.client.post(reverse('create_dct_url'),
                         {'name': 'ТСД-3', 'serial_number': 435406234747,
                          'model': 1, 'mac_address': '43:ac:34:db:53:a1',
                          'accumulator': 1})
        new_obj = AccumulatorDate.objects.last()
        result = [new_obj.accumulator, new_obj.state,
                  new_obj.date.strftime('%Y.%m.%d %I:%M')]
        accum = Accumulator.objects.get(id=1)
        expected = [accum, 1, timezone.now().strftime('%Y.%m.%d %I:%M')]
        self.assertEqual(result, expected)

    def test_install_battery(self):
        """
        Checking whether a battery status change record is created in the
        database when the battery installing in the terminal.
        """
        self.client.post(reverse('update_dct_url', kwargs={'pk': 1}),
                         {'name': 'ТСД-1', 'serial_number': 435406234745,
                          'model': 1, 'mac_address': '43:ac:34:db:53:ae',
                          'accumulator': 1})

        new_obj = AccumulatorDate.objects.last()
        result = [new_obj.accumulator, new_obj.state,
                  new_obj.date.strftime('%Y.%m.%d %I:%M')]
        accum = Accumulator.objects.get(pk=1)
        expected = [accum, 1, timezone.now().strftime('%Y.%m.%d %I:%M')]
        self.assertEqual(result, expected)

    def test_uninstall_battery(self):
        """
        Checking whether a battery status change record is created in the
        database when the battery uninstalling from the terminal.
        """
        self.client.post(reverse('update_dct_url', kwargs={'pk': 2}),
                         {'name': 'ТСД-2', 'serial_number': 435406234746,
                          'model': 1, 'mac_address': '43:ac:34:db:53:af'})
        new_obj = AccumulatorDate.objects.last()
        result = [new_obj.accumulator, new_obj.state,
                  new_obj.date.strftime('%Y.%m.%d %I:%M')]
        accum = Accumulator.objects.get(id=2)
        expected = [accum, 2, timezone.now().strftime('%Y.%m.%d %I:%M')]
        self.assertEqual(result, expected)
    #
    # def test_change_battery(self):
    #     """
    #     Checking whether a battery status change record is created in
    #     the database when a battery is replaced with another battery.
    #     """
    #     self.client.post(reverse('update_dct_url', kwargs={'pk': 2}),
    #                      {'name': 'ТСД-2', 'serial_number': 435406234746,
    #                       'model': 1, 'mac_address': '43:ac:34:db:53:af',
    #                       'accumulator': 1})
    #     new_obj_uninstall = AccumulatorDate.objects.get(id=2)
    #     new_obj_install = AccumulatorDate.objects.get(id=3)
    #     result = [new_obj_uninstall.accumulator, new_obj_uninstall.state,
    #               new_obj_uninstall.date.strftime('%Y.%m.%d %I:%M'),
    #               new_obj_install.accumulator, new_obj_install.state,
    #               new_obj_install.date.strftime('%Y.%m.%d %I:%M')]
    #     accum_uninstall = Accumulator.objects.get(id=2)
    #     accum_install = Accumulator.objects.get(id=1)
    #     expected = [accum_uninstall, 2, timezone.now().strftime('%Y.%m.%d %I:%M'),
    #                 accum_install, 1, timezone.now().strftime('%Y.%m.%d %I:%M')]
    #     # expected = [accum_uninstall, 2, datetime.today().strftime('%Y.%m.%d %I:%M'),
    #     #             accum_install, 1, datetime.today().strftime('%Y.%m.%d %I:%M')]
    #     self.assertEqual(result, expected)

    def test_without_change_without_battery(self):
        """
        Checking whether a battery status change record is created
        in the database when changing a terminal without a battery.
        """
        self.client.post(reverse('update_dct_url', kwargs={'pk': 1}),
                         {'name': 'ТСД-1', 'serial_number': 435406234745,
                          'model': 1, 'mac_address': '43:ac:34:db:53:ae'})
        result = AccumulatorDate.objects.filter(id=2)
        self.assertEqual(bool(result), False)

    def test_without_change_with_battery(self):
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

    # Tests for 'data_collect_terminal_remark' method
    # def test_is_write_db_when_create_dct(self):
    #     """
    #     Checking whether an entry is created in the remarks database when
    #     creating a terminal.
    #     """
    #     self.client.post(reverse('create_dct_url'),
    #                      {'name': 'ТСД-3', 'serial_number': 435406234747,
    #                       'model': 1, 'mac_address': '43:ac:34:db:53:a1'})
    #     result = DataCollectTerminalRemark.objects.filter(id=3)
    #     self.assertEqual(bool(result), False)

    # def test_is_write_db_first_change(self):
    #     """
    #     Checking whether an entry is created in the remarks database
    #     on the first change remark's terminal.
    #     """
    #     self.client.post(reverse('create_dct_url'),
    #                      {'name': 'ТСД-3', 'serial_number': 435406234747,
    #                       'model': 1, 'mac_address': '43:ac:34:db:53:a1',
    #                       'remark': 'TEST'})
    #     self.client.post(reverse('update_dct_url', kwargs={'pk': 3}),
    #                      {'name': 'ТСД-3', 'serial_number': 435406234747,
    #                       'model': 1, 'mac_address': '43:ac:34:db:53:a1',
    #                       'remark': 'TEST 1'})
    #     new_obj1 = DataCollectTerminalRemark.objects.get(id=3)
    #     new_obj2 = DataCollectTerminalRemark.objects.get(id=4)
    #     result = [new_obj1.data_collect_terminal, new_obj1.remark,
    #               new_obj1.date.strftime('%Y.%m.%d %I:%M'),
    #               new_obj2.data_collect_terminal, new_obj2.remark,
    #               new_obj2.date.strftime('%Y.%m.%d %I:%M')]
    #     dct3 = DataCollectTerminal.objects.get(id=3)
    #     expected = [dct3, 'TEST', datetime.today().strftime('%Y.%m.%d %I:%M'),
    #                 dct3, 'TEST 1', datetime.today().strftime('%Y.%m.%d %I:%M')]
    #     self.assertEqual(result, expected)
    #
    # def test_is_write_db_first_change_empty(self):
    #     """
    #     Checking whether a record has been created in the remarks database
    #     on the terminal of the first remark change,
    #     if the first remark was empty.
    #     """
    #     self.client.post(reverse('update_dct_url', kwargs={'pk': 2}),
    #                      {'name': 'ТСД-2', 'serial_number': 435406234746,
    #                       'model': 1, 'mac_address': '43:ac:34:db:53:af',
    #                       'remark': 'TEST'})
    #     new_obj = DataCollectTerminalRemark.objects.get(id=3)
    #     result = [new_obj.data_collect_terminal, new_obj.remark,
    #               new_obj.date.strftime('%Y.%m.%d %I:%M')]
    #     dct2 = DataCollectTerminal.objects.get(id=2)
    #     expected = [dct2, 'TEST', datetime.today().strftime('%Y.%m.%d %I:%M')]
    #     self.assertEqual(result, expected)
    #
    # def test_is_write_db_change_remark(self):
    #     """
    #     Checking whether an entry has been created in the renarks database
    #     on the remark editing terminal
    #     """
    #     self.client.post(reverse('update_dct_url', kwargs={'pk': 1}),
    #                      {'name': 'ТСД-1', 'serial_number': 435406234745,
    #                       'model': 1, 'mac_address': '43:ac:34:db:53:ae',
    #                       'remark': 'TEST 2'})
    #     old_obj = DataCollectTerminalRemark.objects.get(id=2)
    #     new_obj = DataCollectTerminalRemark.objects.get(id=3)
    #     result = [old_obj.data_collect_terminal, old_obj.remark,
    #               old_obj.date.strftime('%Y.%m.%d %I:%M'),
    #               new_obj.data_collect_terminal, new_obj.remark,
    #               new_obj.date.strftime('%Y.%m.%d %I:%M')]
    #     dct = DataCollectTerminal.objects.get(id=1)
    #     expected = [dct, 'TEST 1', '2021.02.16 01:46',
    #                 dct, 'TEST 2', datetime.today().strftime('%Y.%m.%d %I:%M')]
    #     self.assertEqual(result, expected)
    #
    # def test_is_write_db_change_tcd(self):
    #     """
    #     Checking whether an entry was created in the remarks database when
    #     editing the terminal but without changing the remarks.
    #     """
    #     self.client.post(reverse('update_dct_url', kwargs={'pk': 1}),
    #                      {'name': 'ТСД-1', 'serial_number': 435406234745,
    #                       'model': 1, 'mac_address': '43:ac:34:db:53:ae',
    #                       'remark': 'TEST 1', 'accumulator': 1})
    #     result = DataCollectTerminalRemark.objects.filter(id=3)
    #     self.assertEqual(bool(result), False)
