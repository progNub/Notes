from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import QuerySet

from accounts.models import User
from posts.models import Note




# 1 Создать в панели администратора для модели пользователей отображение списка записей со следующими колонками:
# Username, ФИО, Кол-во заметок.
@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ("username", "first_name", "last_name", 'count_notes', 'is_active')

    fieldsets = (
        # 1  tuple(None, dict)
        (None, {"fields": ("username", "password")}),

        # 2  tuple(str, dict)
        ("Персональная информация", {"fields": ("first_name", "last_name", "email", "phone")}),

        # 3  tuple(str, dict)
        (
            "Права пользователя",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),

        # 4  tuple(str, dict)
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )
    actions = ["activate", 'deactivate']

    @admin.display(description="Кол-во записей")
    def count_notes(self, obj):
        return obj.notes.count()

    @admin.action(description="Заблокировать пользователей")
    def deactivate(self, obj, queryset: QuerySet[User]):
        queryset.update(is_active=False)

    @admin.action(description="Разблокировать пользователей")
    def activate(self, obj, queryset: QuerySet[User]):
        queryset.update(is_active=True)

    def get_queryset(self, request):
        return User.objects.all().prefetch_related('notes')
