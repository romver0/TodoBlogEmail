from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import BadHeaderError
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # Встроенные формы
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from datetime import timezone, datetime
from smtplib import SMTPRecipientsRefused, SMTPDataError
from todo.forms import *  # свои формы


def home(request: HttpRequest):
    return render(request, 'todo/home.html')


def signup_user(request: HttpRequest):
    if request.method == 'GET':
        context = {
            'form': UserCreationForm()
        }
        return render(request, 'todo/signupuser.html', context)
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    last_login=datetime.now(),
                    date_joined=datetime.now(),
                    password=request.POST['password1'],
                    email=request.POST['email'],
                )
                try:
                    if user.email:
                        send_mail('Регистрация', 'Вы успешно зарегались!!!', settings.EMAIL_HOST_USER, [user.email])
                    user.save()  # сохранения пользователя в бд
                    login(request, user)  # вход в свой профиль
                except (BadHeaderError, SMTPRecipientsRefused, SMTPDataError) as error:
                    context = {
                        'email': user.email,
                        'error': 'Неверный/Не проверенный email'
                    }
                    return render(request, 'todo/signupuser.html', context=context)
                return redirect('profile')
            except (IntegrityError, ValueError) as error:
                context = {
                    'form': UserCreationForm(),
                    'err': 'Имя пользователя уже используется',
                }
                return render(request, 'todo/signupuser.html', context)
        else:
            context = {
                'form': UserCreationForm(),
                'err': 'Пароли не совпадают'
            }
            return render(request, 'todo/signupuser.html', context)


def logout_user(request: HttpRequest):
    if request.method == 'POST':
        logout(request)
        return redirect('blog:all_blogs')


def login_user(request: HttpRequest):
    if request.method == 'GET':
        context = {
            'form': AuthenticationForm(),
        }
        return render(request, 'todo/login.html', context)
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            context = {
                'form': AuthenticationForm(),
                'err': 'Неправильный пароль или имя'
            }
            return render(request, 'todo/login.html', context)
        else:
            login(request, user)  # вход в свой профиль
            return redirect('profile')


def profile(request: HttpRequest):
    todos = Todo.objects.filter(user=request.user)
    info = InfoUser.objects.filter(user=request.user)
    request.session['count'] = todos.count()
    request.session['count_important'] = Todo.objects.filter(user=request.user, is_important=True).count()
    context = {
        'todos': todos,
        'info': info,
    }
    return render(request, 'todo/profile.html', context=context)


def is_important_view(request: HttpRequest):
    todos = Todo.objects.filter(user=request.user)
    request.session['count_important'] = Todo.objects.filter(user=request.user, is_important=True).count()
    context = {
        'todos': todos,
    }
    return render(request, 'todo/isImportant.html', context=context)


def game_views(request: HttpRequest):
    return render(request, 'todo/game.html')


def create_todo(request: HttpRequest):
    if request.method == 'GET':
        context = {
            'form': TodoForm()
        }
        return render(request, 'todo/createtodo.html', context=context)
    else:
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)  # сохраняет все данные в БД
            new_todo.user = request.user
            new_todo.save()
            return redirect('todos')
        except ValueError:
            context = {
                'form': TodoForm(),
                'err': 'Переданы неверные данные',
            }
            return render(request, 'todo/createtodo.html', context)


def view_todo(request: HttpRequest, todo_id: int):
    todo = get_object_or_404(Todo, pk=todo_id)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        context = {
            'todo': todo,
            'form': form,
        }
        return render(request, 'todo/viewtodo.html', context=context)
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('todos')
        except ValueError:
            context = {
                'form': TodoForm(),
                'err': 'Переданы неверные данные',
            }
            return render(request, 'todo/viewtodo.html', context)


def complete_todo(request: HttpRequest, todo_id: int):
    todo = get_object_or_404(Todo, pk=todo_id)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('todos')


def delete_todo(request: HttpRequest, todo_id: int):
    todo = get_object_or_404(Todo, pk=todo_id)
    if request.method == 'POST':
        todo.delete()
    return redirect('todos')


def show_todo(request: HttpRequest):
    todos = Todo.objects.filter(user=request.user)
    form = TodoForm()
    request.session['count'] = todos.count()
    request.session['count_important'] = Todo.objects.filter(user=request.user, is_important=True).count()

    context = {
        'todos': todos,
        'form': form
    }
    return render(request, 'todo/todos.html', context=context)


def info_views(request: HttpRequest):
    if request.method == 'GET':
        context = {
            'info': InfoForm()
        }
        return render(request, 'todo/info.html', context=context)
    else:
        try:
            form = InfoForm(request.POST)
            new_info = form.save(commit=False)
            new_info.user = request.user
            new_info.save()
            return redirect('profile')
        except ValueError:
            context = {
                'info': InfoForm,
                'err': 'Переданы неверные данные',
            }
            return render(request, 'todo/info.html', context)


'https://docs.djangoproject.com/en/4.0/topics/auth/default/#django.contrib.auth.login'


def handler_not_found(request: HttpRequest, exception: str):
    return render(request, 'todo/404.html', status=404)
