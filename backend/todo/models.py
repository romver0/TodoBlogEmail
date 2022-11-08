from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime


class Todo(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.CharField(max_length=400, blank=True, verbose_name='Описание')
    created = models.DateTimeField(default=timezone.now,
                                   verbose_name='Дата создания')  # auto_now_add - нельзя поменять вручную
    datecompleted = models.DateTimeField(
        # default=timezone.now,
        default=timezone.now,
        null=True,
        blank=True,
        verbose_name='Дата дедлайна'
    )
    is_important = models.BooleanField(default=False, verbose_name='Важность')
    done = models.BooleanField(default=False, verbose_name='Выполнение')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # class Meta:
    #     verbose_name='Тудушки'


class InfoUser(models.Model):
    сity = models.CharField(max_length=100)
    social_network = models.URLField(max_length=200, verbose_name='Website')

    phonenumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phonenumber = models.CharField(validators=[phonenumberRegex], max_length=16, unique=True, null=False,
                                   blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.user
# class User(models.Model):
#     title = models.CharField()
#     description = models.CharField()
#     email = models.EmailField(max_length=254)
#     img = models.ImageField(upload_to=)
#     file = models.FileField(
#         upload_to=)  # https://docs.djangoproject.com/en/4.1/ref/models/fields/#django.db.models.FileField.upload_to
