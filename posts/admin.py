from django.contrib import admin
from django.db.models import QuerySet, F
from django.db.models.functions import Upper
from django.utils.safestring import mark_safe

from posts.models import Note, Tag


# Register your models here.

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ["title", "created_at", 'mod_time', "tags_function", "autor"]
    search_fields = ["title", "content"]
    ordering = ('-mod_time',)

    # Действия
    actions = ["title_up"]

    # Поля, которые не имеют большого кол-ва уникальных вариантов!
    list_filter = ["autor__username", "autor__email", "tags__name"]

    fieldsets = (
        # 1
        (None, {"fields": ("title", "autor", "image", "tags")}),
        ("Содержимое", {"fields": ("content",)}),
        ("Даты", {"fields": ('mod_time',)}),
    )

    def get_queryset(self, request):
        return Note.objects.all().select_related('autor').prefetch_related('tags')

    @admin.action(description="Upper Title")
    def title_up(self, queryset: QuerySet[Note]):
        queryset.update(title=Upper(F("title")))

    @admin.display(description="Теги")
    def tags_function(self, obj: Note) -> str:
        tags = list(obj.tags.all())
        text = ""
        for tag in tags:
            text += f"<span style=\"color: blue;\">{tag}</span><br>"
        return mark_safe(text)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name"]
