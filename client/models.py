from django.db import models


class Client(models.Model):
    """Hardware users"""
    client = models.CharField(max_length=50, unique=True, db_index=True,
                              verbose_name='Пользователь')

    def __str__(self):
        return self.client
