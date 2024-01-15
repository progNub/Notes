from django.urls import path
from accounts.views import registration_view, user_logout, user_login, authentication_view, user_profile, \
    edit_user_profile, edit_user_password

urlpatterns = [
    path('authentication', authentication_view, name='authentication'),
    path('registration', registration_view, name='registration'),
    path('logout', user_logout, name='logout'),
    path('login', user_login, name='login'),
    path('<username>/profile', user_profile, name='profile'),
    path('<username>/edit_profile', edit_user_profile, name='edit-profile'),
    path('<username>/edit_password', edit_user_password, name='edit-profile-password'),
]
