"""
URL configuration for Lesson21_Django project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


from posts.views import home_page_view, create_note_view, show_note_view, show_about_view, delete_note_view, \
    edit_note_view, list_posts_user

urlpatterns = [
    path('admin/', admin.site.urls),  # Подключение панели администратора.
    path('accounts/', include('accounts.urls')),
    path("", home_page_view, name="home"),  # Добавим главную страницу.

    path("create", create_note_view, name="create-note"),
    path("note/<note_uuid>", show_note_view, name="show-note"),

    path('edit/<note_uuid>', edit_note_view, name='edit-note'),

    path('delete/<note_uuid>', delete_note_view, name='delete-note'),

    path('about', show_about_view, name='about'),
    path('user/<username>/posts', list_posts_user, name='list-posts-user'),
    path("__debug__/", include("debug_toolbar.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
