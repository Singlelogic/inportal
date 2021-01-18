from django.db import models

from account.models import Profile


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
    user = models.ForeignKey(Profile, null=True, on_delete=models.PROTECT,
                             verbose_name='Пользователь')
    accumulator = models.ForeignKey('Accumulator', null=True, on_delete=models.PROTECT,
                                    verbose_name='Аккумулятор')
    remark = models.TextField(null=True, blank=True, verbose_name='Примечания')

    def __str__(self):
        return self.name


class Accumulator(models.Model):
    """Accumulator for Date Collect Terminal"""
    number = models.CharField(max_length=10, unique=True, db_index=True,
                            verbose_name='Номер')
    date_change = models.DateField(verbose_name='Дата установки')
    remark = models.TextField(null=True, blank=True, verbose_name='Примечания')

    def __str__(self):
        return self.number
