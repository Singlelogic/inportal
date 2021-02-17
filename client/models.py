from django.db import models
from django.urls import reverse


class Client(models.Model):
    """Hardware users"""
    client = models.CharField(max_length=50, unique=True, db_index=True,
                              verbose_name='Пользователь')

    def __str__(self):
        return self.client

    def get_absolute_url(self):
        """
        Method for getting the absolute path of an instance.
        """
        return reverse('update_client_url', kwargs={'pk': self.pk})
