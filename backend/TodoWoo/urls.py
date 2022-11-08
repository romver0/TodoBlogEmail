from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from blog.api.views import BlogViewSet
from todo.api.views import TodoViewSet, UserViewSet
from todo import views

router = routers.DefaultRouter()
router.register(r'blog', BlogViewSet)
router.register(r'todo', TodoViewSet)
router.register(r'user', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Ауентификация
    path('signup/', views.signupuser, name='register'),
    path('login/', views.loginuser, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    # Профиль пользовтеля
    # path('profile/', views.signupuser, name='register'),
    # Тудушки
    path('', views.home, name='home'),
    path('blog/', include('blog.urls')),
    path('todos/', views.showTodo, name='todos'),
    path('todos/<int:todo_id>/', views.viewtodo, name='viewtodo'),
    path('todos/<int:todo_id>/complete', views.completetodo, name='completetodo'),
    path('todos/<int:todo_id>/delete', views.deletetodo, name='deletetodo'),
    path('is_important/', views.isImportantViews, name='is_important'),
    path('current/', views.currenttodos, name='currenttodos'),
    path('create/', views.createtodo, name='addTodo'),
    path('info/', views.infoviews, name='info'),
    path('game/', views.gameviews, name='game'),

    # api
    path('api/', include(router.urls)),
    path('', include('user.urls'))
]

handler404 = 'todo.views.handler_not_found'
