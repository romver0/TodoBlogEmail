# from django.http import HttpResponse
# from django.shortcuts import render
# from django.contrib.auth import authenticate, login
# from .forms import *
#
#
# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_activate:
#                     login(request, user)
#                     return HttpResponse('Аутентификация прошла успешно!')
#                 else:
#                     return HttpResponse('Отключённый аккаунт')
#             else:
#                 return HttpResponse('Инвалидный логин')
#     else:
#         form = LoginForm()
#     return render(request, 'account/login.html',{'from':form})
#
#
# def register(request):
#     if request.method == 'POST':
#         user_form = UserRegistrationForm(request.POST)
#         if user_form.is_valid():
#             # Create a new user object but avoid saving it yet
#             new_user = user_form.save(commit=False)
#             # Set the chosen password
#             new_user.set_password(user_form.cleaned_data['password'])
#             # Save the User object
#             new_user.save()
#             # print('is_valid = ',user_form.is_valid())
#             return render(request, 'account/register_done.html', {'new_user': new_user})
#     else:
#         user_form = UserRegistrationForm()
#     return render(request, 'account/register.html', {'user_form': user_form})


'https://pocoz.gitbooks.io/django-v-primerah/content/glava-4-sozdanie-social-website/registratsiya-polzovatelei-i-profili-polzovatelei/registratsiya-polzovatelei.html'
from datetime import timezone, datetime
from smtplib import SMTPRecipientsRefused, SMTPDataError

from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import BadHeaderError

'https://docs.djangoproject.com/en/4.1/topics/auth/'
'https://docs.djangoproject.com/en/4.1/ref/contrib/auth/'

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # Встроенные формы
from todo.forms import *  # свои формы
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate


# def proverka(text):
#     lower = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
#     return lower.intersection(text.lower()) != set()

def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == 'GET':
        context = {
            'form': UserCreationForm()
        }
        return render(request, 'todo/signupuser.html', context)
    else:
        print('request.POST = ', request.POST)
        # Create a new user
        if (request.POST['password1'] == request.POST['password2']):
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    last_login=datetime.now(),
                    date_joined=datetime.now(),
                    password=request.POST['password1'],
                    email=request.POST['email'],
                    # profession=request.POST['profession'],
                )
                try:
                    if user.email:
                        send_mail('Регистрация', 'Вы успешно зарегались!!!', settings.EMAIL_HOST_USER, [user.email])
                    user.save()  # сохранения пользователя в бд
                    login(request, user)  # вход в свой профиль
                except BadHeaderError:
                    context = {
                        'email': user.email,
                        'error': 'Неверный/Не проверенный email'
                    }
                    return render(request, 'todo/signupuser.html', context=context)
                except SMTPRecipientsRefused:
                    context = {
                        'email': user.email,
                        'error': 'Неверный/Не проверенный email'
                    }
                    return render(request, 'todo/signupuser.html', context=context)

                except SMTPDataError:
                    context = {
                        'email': user.email,
                        'error': 'Неверный/Не проверенный email'
                    }
                    return render(request, 'todo/signupuser.html', context=context)
                # user.save()  # сохранения пользователя в бд
                # login(request, user)  # вход в свой профиль
                return redirect('currenttodos')
            except IntegrityError:
                context = {
                    'form': UserCreationForm(),
                    # 'nameLen':len(request.POST['password1']),
                    'err': 'Имя пользователя уже используется',
                    # 'err2':'Cлишком короткий пароль',
                    # 'err3': 'Используйте только англ алфавит',
                }
                return render(request, 'todo/signupuser.html', context)
            except ValueError:
                context = {
                    'form': UserCreationForm(),
                    'err': 'Имя пользователя уже используется',
                }
                return render(request, 'todo/signupuser.html', context)
        else:
            # Tell the user the passwords didn't match
            context = {
                'form': UserCreationForm(),
                'err': 'Пароли не совпадают'
            }
            return render(request, 'todo/signupuser.html', context)


def logoutuser(request):
    if request.method == 'POST':
        print('сработал logoutuser ', request)
        logout(request)
        return redirect('blog:all_blogs')


def loginuser(request):
    if request.method == 'GET':
        context = {
            'form': AuthenticationForm(),
        }
        return render(request, 'todo/login.html', context)
    else:
        # print(User.objects)
        # print('request.POST = ', request.POST)
        # print('',request.POST.get('username'))
        # print('',request.POST.get('password'))
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
            return redirect('currenttodos')


def currenttodos(request):
    # todos=Todo.objects.all() #доступны все объекты
    # todos=Todo.objects.filter(user=request.user,datecompleted__isnull=True) #datecompleted__isnull=True => не может быть пустым==True
    todos = Todo.objects.filter(user=request.user)
    info = InfoUser.objects.filter(user=request.user)
    if len(info) > 1:
        print(info[0].delete())
    # info=info[len(info)-1]
    # print(info)
    context = {
        'todos': todos,
        'info': info,
    }
    return render(request, 'todo/profile.html', context=context)


def isImportantViews(request):
    todos = Todo.objects.filter(user=request.user)
    count = 0
    for todo in todos:
        if todo.is_important:
            count += 1

    context = {
        'todos': todos,
        'count': count
    }
    return render(request, 'todo/isImportant.html', context=context)


def gameviews(request):
    return render(request, 'todo/game.html')


def createtodo(request):
    if request.method == 'GET':
        context = {
            'form': TodoForm()
        }
        return render(request, 'todo/createtodo.html', context=context)
    else:
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)  # сохраняет все данные в БД
            print('request.user = ', request.user)
            new_todo.user = request.user
            new_todo.save()
            return redirect('todos')
        except ValueError:
            context = {
                'form': TodoForm(),
                'err': 'Переданы неверные данные',
            }
            return render(request, 'todo/createtodo.html', context)


def viewtodo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        context = {
            'todo': todo,
            'form': form,
        }
        print(todo)
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


def completetodo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('todos')
        # return render(request, 'todo/todos.html', {'complete': 'выполнено'})
        # return redirect('todos')


def deletetodo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    if request.method == 'POST':
        try:
            print('Удалено')
            todo.delete()
            # todo.save()
        except:
            print('не удалено')
    return redirect('todos')


def showTodo(request):
    todos = Todo.objects.filter(user=request.user)
    form = TodoForm()
    context = {
        'todos': todos,
        'form': form
    }
    print('todos = ', todos)
    return render(request, 'todo/todos.html', context=context)


def infoviews(request):
    if request.method == 'GET':
        context = {
            'info': InfoForm()
        }
        return render(request, 'todo/info.html', context=context)
    else:
        try:
            form = InfoForm(request.POST)
            print('InfoForm/requst.POST =  ', request.POST)
            new_info = form.save(commit=False)
            new_info.user = request.user
            new_info.save()
            # print(new_info)
            return redirect('currenttodos')
        except ValueError:
            context = {
                'info': InfoForm,
                'err': 'Переданы неверные данные',
            }
            return render(request, 'todo/info.html', context)


'https://docs.djangoproject.com/en/4.0/topics/auth/default/#django.contrib.auth.login'


def handler_not_found(request, exception):
    return render(request, 'todo/404.html', status=404)
