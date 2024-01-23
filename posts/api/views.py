from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny, SAFE_METHODS

from posts.api.permissions import IsOwnerOrAdminOrReadOnly
from posts.api.serializers import NoteListSerializer, NoteCreateSerializer, TagListSerializer
from posts.models import Note, Tag


class NoteDetailApiView(RetrieveUpdateAPIView):
    queryset = Note.objects.all().prefetch_related('tags').select_related('autor')  # как и где брать объекты
    serializer_class = NoteCreateSerializer
    lookup_field = 'uuid'
    lookup_url_kwarg = 'id'
    permission_classes = [IsOwnerOrAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)


class NoteListCreateApiView(ListCreateAPIView):
    queryset = Note.objects.all().prefetch_related('tags').select_related('autor')  # как и где брать объекты
    lookup_field = 'uuid'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return NoteListSerializer
        return NoteCreateSerializer

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)


class TagListCreateApiView(ListCreateAPIView):
    queryset = Tag.objects.all()  # как и где брать объекты
    serializer_class = TagListSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedOrReadOnly]

# class NoteListCreateApiView(GenericAPIView):
#     queryset = Note.objects.all()  # как и где брать объекты
#
#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return NoteCreateSerializer
#         return NoteListSerializer
#
#     def get(self, *args, **kwargs):
#         query_set = self.get_queryset()
#         serializer = self.get_serializer(query_set, many=True)
#         data = serializer.data
#         return Response(data)
#
#     def post(self, *args, **kwargs):
#         serializer: NoteCreateSerializer = self.get_serializer(data=self.request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save(autor=self.request.user)
#         return Response(serializer.data)


# class NoteDetailApiView(GenericAPIView):
#     queryset = Note.objects.all()
#     serializer_class = NoteCreateSerializer
#     lookup_field = 'uuid'
#
#     def get(self, request, uuid, *args, **kwargs):
#         note = get_object_or_404(self.get_queryset(), uuid=uuid)
#         serializer = self.get_serializer(instance=note)
#         return Response(serializer.data)
#
#     # для изменения полей
#     def put(self, request, uuid, *args, **kwargs):
#         note = get_object_or_404(self.get_queryset(), uuid=uuid)
#         serializer: NoteCreateSerializer = self.get_serializer(data=self.request.data, instance=note)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     # для изменения некоторых полей
#     def patch(self, request, uuid, *args, **kwargs):
#         note = get_object_or_404(self.get_queryset(), uuid=uuid)
#         serializer: NoteCreateSerializer = self.get_serializer(data=self.request.data, instance=note, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, uuid, *args, **kwargs):
#         note = get_object_or_404(self.get_queryset(), uuid=uuid)
#         note.delete()
#         return Response(status=204)


#
# @api_view()
# def list_create_note_api_view(request):
#     notes = Note.objects.all()
#     data = []
#     for note in notes:
#         obj_dict = {
#             'uuid': note.uuid,
#             'title': note.title,
#             'content': note.content,
#             'created_at': note.created_at,
#             'mod_time': note.mod_time,
#             'autor': str(note.autor),
#             'tags': note.tags.all().values_list('name', flat=True)}
#         if note.image:
#             obj_dict['image'] = note.image.url
#         else:
#             obj_dict['image'] = None
#         data.append(obj_dict)
#     return Response(data)
#
#
# @api_view()
# def detail_note_api_view(request, uuid: str):
#     note = get_object_or_404(Note, uuid=uuid)
#     obj_dict = {
#         'uuid': note.uuid,
#         'title': note.title,
#         'content': note.content,
#         'created_at': note.created_at,
#         'mod_time': note.mod_time,
#         'autor': str(note.autor),
#         'tags': note.tags.all().values_list('name', flat=True)}
#     if note.image:
#         obj_dict['image'] = note.image.url
#     else:
#         obj_dict['image'] = None
#     return Response(obj_dict)
