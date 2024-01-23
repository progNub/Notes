from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from posts.models import Note, Tag


class AutorField(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username']


class TagField(serializers.PrimaryKeyRelatedField):
    queryset = Tag.objects.all()

    class Meta:
        model = Tag

    def to_representation(self, value):
        """что бы тэг выводился без id и ключа 'name'"""
        return value.name

    def to_internal_value(self, data):
        """так как метод to_representation переопределен то выдавало ошибку при создании заметки,
        что вместо pk был получен объект типа str"""
        obj, created = Tag.objects.get_or_create(name=data)
        return obj


class NoteListSerializer(serializers.ModelSerializer):
    autor = AutorField()
    tags = TagField(many=True)

    class Meta:
        model = Note
        fields = ['uuid', 'title', 'created_at', 'image', 'tags', 'autor']


class NoteCreateSerializer(serializers.ModelSerializer):
    autor = AutorField(read_only=True)
    tags = TagField(many=True)

    class Meta:
        model = Note
        fields = ['uuid', 'title', 'content', 'created_at', 'autor', 'image', 'tags']
        write_only_fields = ["title", "content", "image", "tags"]
        read_only_fields = ["uuid", "created_at", "autor", ]


class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        write_only_fields = ['name']
