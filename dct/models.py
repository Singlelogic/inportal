from django.utils import timezone

from django.db import models
from django.urls import reverse

from client.models import Client
from .utils import is_ru

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
    name = models.CharField(primary_key=True, max_length=50, db_index=True,
                            verbose_name='Наименование')
    slug = models.SlugField(max_length=50, blank=True, unique=True)
    model = models.IntegerField(choices=MODELS, default=1, verbose_name='Модель')
    serial_number = models.CharField(max_length=50, unique=True,
                                     verbose_name='Серийный номер')
    mac_address = models.CharField(max_length=20, unique=True, db_index=True,
                                   verbose_name='MAC-адрес')
    user = models.OneToOneField(Client, null=True, blank=True,
                                on_delete=models.PROTECT, verbose_name='Пользователь')
    accumulator = models.OneToOneField('Accumulator', null=True, blank=True,
                                       on_delete=models.PROTECT, verbose_name='Аккумулятор')
    remark = models.TextField(null=True, blank=True, verbose_name='Примечание')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    debited = models.BooleanField(default=False, verbose_name='Списан')
    repair = models.BooleanField(default=False, verbose_name='В ремонте')

    def __str__(self):
        return self.name

    def __gt__(self, other):
        return int(self.name[4:]) > int(other.name[4:])

    def save(self, *args, **kwargs):
        self.slug = is_ru(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Method for getting the absolute path of an instance.
        """
        return reverse('update_dct_url', kwargs={'slug': self.slug})

    class Meta:
        verbose_name_plural = 'ТСД'
        verbose_name = 'ТСД'


class DataCollectTerminalRemark(models.Model):
    """
    Remark for data collect terminal.
    """
    data_collect_terminal = models.ForeignKey(DataCollectTerminal, null=True,
                                              blank=True, on_delete=models.CASCADE)
    remark = models.TextField(null=True, blank=True, verbose_name='Примечание')
    date = models.DateTimeField(verbose_name='Дата')

    def __str__(self):
        return f'{self.data_collect_terminal}: {self.remark} - ' \
               f'{self.date.strftime("%Y.%m.%d %I:%M")}'

    class Meta:
        verbose_name = 'Примечание'
        verbose_name_plural = 'Примечания'
        ordering = ['-date']


class Accumulator(models.Model):
    """Accumulator for Date Collect Terminal"""
    number = models.IntegerField(primary_key=True, db_index=True, verbose_name='Номер')
    remark = models.TextField(null=True, blank=True, verbose_name='Примечание')
    date_purchase = models.DateTimeField(auto_now_add=True, verbose_name='Дата закупки')

    def __str__(self):
        return str(self.number)

    class Meta:
        verbose_name_plural = 'Аккумуляторы'
        verbose_name = 'Аккумулятор'
        ordering = ['number']

    def get_absolute_url(self):
        """
        Method for getting the absolute path of an instance.
        """
        return reverse('update_accumulator_url', kwargs={'pk': self.pk})

    def changed_status(self, state):
        """
        Changing the battery status.
        Possible states:
        1. Installed
        2. Uninstalled
        """
        AccumulatorDate.objects.create(state=state, accumulator=self)

    def lifetime(self) -> int:
        """Returns the number of days worked by the battery."""
        sum = 0
        if self.accumulatordate_set.all():
            for i in self.accumulatordate_set.all():
                if i.state == 1:
                    start = i.date
                else:
                    stop = i.date
                    delta = stop - start
                    sum += delta.days
            if i.state == 1:
                delta = timezone.now() - start
                sum += delta.days
            return sum
        return 0


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
        return f'{self.accumulator}: {self.state} - {self.date.strftime("%Y.%m.%d %I:%M")}'

    class Meta:
        ordering = ['date']
