from django.db import models
from django.urls import reverse

from client.models import Client


class DataCollectTerminal(models.Model):
    """Data Collect Terminal"""
    MODELS = (
        (1, 'Motorola MC7596'),
        (2, 'Motorola MC7598'),
        (3, 'Motorola MC7090'),
        (4, 'Motorola MC9090ER'),
        (5, 'Intermec CK3a1'),
        (6, 'Intermec CK3n1'),
    )
    name = models.CharField(max_length=50, unique=True, db_index=True,
                            verbose_name='Наименование')
    model = models.IntegerField(choices=MODELS, default=1, verbose_name='Модель')
    serial_number = models.CharField(max_length=50, verbose_name='Серийный номер')
    mac_address = models.CharField(max_length=20, unique=True, db_index=True,
                                   verbose_name='MAC-адрес')
    user = models.ForeignKey(Client, null=True, blank=True,
                             on_delete=models.PROTECT, verbose_name='Пользователь')
    accumulator = models.ForeignKey('Accumulator', null=True, blank=True,
                                    on_delete=models.PROTECT, verbose_name='Аккумулятор')
    remark = models.TextField(null=True, blank=True, verbose_name='Примечание')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('update_dct_url', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'ТСД'
        verbose_name = 'ТСД'


class Accumulator(models.Model):
    """Accumulator for Date Collect Terminal"""
    number = models.CharField(max_length=10, unique=True, db_index=True,
                              verbose_name='Номер')
    remark = models.TextField(null=True, blank=True, verbose_name='Примечание')

    def __str__(self):
        return self.number

    class Meta:
        verbose_name_plural = 'Аккумуляторы'
        verbose_name = 'Аккумулятор'

    def changed_status(self):
        """
        Changing the battery status.
        Possible states:
        1. Installed
        2. Uninstalled
        """
        AccumulatorDate.objects.create(state=1, accumulator=self)


class AccumulatorDate(models.Model):
    """
    This class contains data about the date of installation and the date of
    removal of the batteries from the data collection terminals.
    """
    STATE = (
        (1, 'Install'),
        (2, 'Uninstall'),
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    state = models.IntegerField(choices=STATE, default=1,
                                verbose_name='Состояние')
    accumulator = models.ForeignKey(Accumulator, on_delete=models.CASCADE,
                                    verbose_name='Дата изменения состояния')

    def __str__(self):
        return f'{self.accumulator}: {self.state} - {self.date}'