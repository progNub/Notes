from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

app_name = 'api'

urlpatterns = [
    path('posts/', views.NoteListCreateApiView.as_view(), name='api-list-notes'),
    path('posts/<id>', views.NoteDetailApiView.as_view(), name='api-note'),
    path('tag/', views.TagListCreateApiView.as_view(), name='api-list-tags'),

    path('auth/', include('djoser.urls.authtoken')),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
