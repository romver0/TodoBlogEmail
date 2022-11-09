from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from todo import views
from blog.api.views import BlogViewSet
from todo.api.views import TodoViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'blog', BlogViewSet)
router.register(r'todo', TodoViewSet)
router.register(r'user', UserViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),

    # Ауентификация
    path('signup/', views.signup_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # Профиль пользователя
    path('profile/', views.profile, name='profile'),

    # Блог
    path('blog/', include('blog.urls')),

    # Тудушки
    path('todos/', views.show_todo, name='todos'),
    path('todos/<int:todo_id>/', views.view_todo, name='view_todo'),
    path('todos/<int:todo_id>/complete', views.complete_todo, name='complete_todo'),
    path('todos/<int:todo_id>/delete', views.delete_todo, name='delete_todo'),
    path('is_important/', views.is_important_view, name='is_important'),
    path('create/', views.create_todo, name='addTodo'),
    path('info/', views.info_views, name='info'),
    path('game/', views.game_views, name='game'),

    # api
    path('api/', include(router.urls)),
    path('', include('user.urls'))
]

handler404 = 'todo.views.handler_not_found'
