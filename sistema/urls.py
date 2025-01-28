"""
URL configuration for sistema project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from task import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('signup/',views.signup, name='signup'),
    path('tasks/new', views.new_tasks , name='newtasks'),
    path('logout/', views.signout , name='logout'),
    path('perfil/', views.perfil , name='perfil'),
    path('notifications/', views.notifications, name='notifications'),
    path('mark_as_read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('tasks/', views.tasks, name='tasks'),
    path('search/', views.search_tasks, name='search_tasks'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('configuracion/', views.configuracion, name='configuracion'),
    path('tasks/all/', views.tareatodos, name='tareatodos'),    
    path('tasks/<int:task_id>/', views.task_details, name='task_details'),    
    path('signin/', views.signin , name='signin'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    # path('task/<int:task_id>/comment/', views.task_comment, name='task_comment'),
    path('task/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('error/', views.error_page, name='error_page'), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
