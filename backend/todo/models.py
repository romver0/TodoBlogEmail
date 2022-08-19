from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Todo(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата создания')  # auto_now_add - нельзя поменять вручную
    datecompleted = models.DateTimeField(
        # default=timezone.now,
        null=True,
        blank=True,
        verbose_name='Дата дедлайна'
    )
    is_important = models.BooleanField(default=False, verbose_name='Важность')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # class Meta:
    #     verbose_name='Тудушки'


class InfoUser(models.Model):
    сity = models.CharField(max_length=100)
    # telephone = models.CharField(max_length=)
    social_network = models.URLField(max_length=200, verbose_name='Wesite')
    # phonenumber = PhoneNumberField(unique=True, null=False, blank=True,help_text='(Пример,+79083095579')

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
