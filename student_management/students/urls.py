from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns=[
    path('students/',views.student_list,name='student_list'),
    path('register/',views.student_register,name='student_register'),
    path('update/<int:id>/',views.student_update,name='student_update'),
    path('delete/<int:id>/',views.student_delete,name='student_delete'),
    path('user_register/',views.user_register,name='user_register'),
    path('login/',auth_views.LoginView.as_view(redirect_authenticated_user=True),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('', views.home, name='home'),
]