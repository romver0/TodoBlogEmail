from django.utils import timezone
from django.db import models
from datetime import datetime

from TodoWoo.settings import ALLOWED_HOSTS


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name='Тема')
    description = models.TextField(blank=True, verbose_name='Описание')
    date = models.DateTimeField(
        default=timezone.now,
        # default=datetime.now,
        verbose_name='Дата выхода поста'
    )
    # url = models.URLField(max_length=200, default=f'{ALLOWED_HOSTS[0]}:8000/blog/')

    def __str__(self):
        return self.title
