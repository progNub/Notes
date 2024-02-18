from django.urls import path
from accounts.views import RegisterUser, user_logout, user_login, authentication_view, user_profile, \
    edit_user_profile, edit_user_password, reset_password, get_page_edit_password

from posts.views import show_posts_history

urlpatterns = [
    path('authentication', authentication_view, name='authentication'),
    path('registration', RegisterUser.as_view(), name='registration'),

    path('confirm_email/<uidb64>/<token>', RegisterUser.confirm_email, name='registration-confirm-email'),

    path('logout', user_logout, name='logout'),
    path('login', user_login, name='login'),
    path('<username>/profile', user_profile, name='profile'),
    path('<username>/edit_profile', edit_user_profile, name='edit-profile'),

    path('<user_id>/reset_password', reset_password, name='reset-password'),
    path('confirm_reset/<uidb64>/<token>', get_page_edit_password, name='form-edit-password'),
    path('<username>/edit_password', edit_user_password, name='edit-password'),

    path('history/posts', show_posts_history, name='posts_history')
]
