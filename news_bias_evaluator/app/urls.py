from django.urls import path, re_path
from django.contrib import admin
from . import views

app_name = 'app'
urlpatterns = [
    path('', views.main, name='main'),
    path('results/', views.onSubmit, name='results'),
    path('admin/', views.dispatch, name='dispatch'),
    path('login/', views.log, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('admin/dashboard/', views.access_dashboard, name="dashboard"),
    path('admin/dashboard/process_admin_request/', views.process_admin_request, name="process_admin_request"),
    path('admin/database/', admin.site.urls, name='database'),
    re_path(r'^trainingStatus/$', views.get_training_status, name='get_training_status')
    re_path(r'^trainingEvaluationData/$', views.get_training_evaluation_data, name='get_training_evaluation_data')
]