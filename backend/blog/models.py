from django.utils import timezone
from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name='Тема')
    description = models.TextField(verbose_name='Описание')
    # date = models.DateField()
    date = models.DateTimeField(
        default=timezone.now,
        null=True,
        blank=True,
        verbose_name='Дата выхода поста'
    )


    def __str__(self):
        return self.title
