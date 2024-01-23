from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('posts/', views.NoteListCreateApiView.as_view(), name='api-list-notes'),
    path('posts/<id>', views.NoteDetailApiView.as_view(), name='api-note'),
    path('tag/', views.TagListCreateApiView.as_view(), name='api-list-tags'),
]
