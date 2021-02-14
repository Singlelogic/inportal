from django.test import TestCase
from django.urls import reverse

from dct.models import (
    AccumulatorDate, DataCollectTerminal
)


class ChangedStatusAccumTest(TestCase):
    """
    Test for mixin class ChangedStatusAccum
    """
    fixtures = ['initial_data.json']

    def test_form_valid(self):
        """
        Checking the battery status change when creating and changing
        the data collection terminal.
        """
        dct = DataCollectTerminal.objects.get(id=1)
        print(dct.accumulator)
        accumulator_date = AccumulatorDate.objects.all()
        print(accumulator_date)

        self.client.post(reverse('update_dct_url', kwargs={'pk': 1}),
                         {'name': 'ТСД-1', 'serial_number': 435406234745,
                          'model': 1, 'mac_address': '43:ac:34:db:53:af'})

        dct = DataCollectTerminal.objects.get(id=1)
        print(dct.accumulator)
        accumulator_date = AccumulatorDate.objects.all()
        print(accumulator_date)

        # resp = self.client.get(reverse('list_dct_url'))
        # print(resp.context['datacollectterminal_list'])
