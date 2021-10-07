from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),

    path('', views.Home,name='home'),
    path('user/', views.UserPage, name='user'),

    path('setting/', views.Setting, name='setting'),# profile pic

    path('product/', views.Products,name='product'),
    path('customer/<str:pk>', views.Customers,name='customer'),


    path('createorder/<str:pk>', views.CreateOrder,name='createorder'),
    path('update/<str:pk>', views.update, name='update'),
    path('delete/<str:pk>', views.delete, name='delete'),

    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
         name='reset_password'),

    path('password_reset_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html')
         ,name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'),
         name='password_reset_confirm'),

    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),


]


'''
1 - Submit email form                         //PasswordResetView.as_view()
2 - Email sent success message                //PasswordResetDoneView.as_view()
3 - Link to password Rest form in email       //PasswordResetConfirmView.as_view()
4 - Password successfully changed message     //PasswordResetCompleteView.as_view()
'''