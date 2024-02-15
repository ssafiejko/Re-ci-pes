from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path
from . import views


urlpatterns= [
    path('login/' ,views.loginPage, name='login'),
    path('register/' ,views.registerPage, name='register'),
    path('logout/' ,views.logoutUser, name='logout'),
    path('', views.home, name='home'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),
    path('recipe/<str:pk>/', views.recipe, name='recipe'),
    path('add-recipe/', views.createRecipe, name='add-recipe'),
    path('update-recipe/<str:pk>/', views.updateRecipe, name='update-recipe'),
    path('delete-recipe/<str:pk>/', views.deleteRecipe, name='delete-recipe'),
    path('update-user/', views.updateUser, name='update-user'),

    path('password-reset/', PasswordResetView.as_view(template_name='users/password_reset.html'), name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),


]