from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.handlers.wsgi import WSGIRequest
from django.utils import timezone

from django.contrib.auth.decorators import login_required

from .models import Note, delete_old_image, Tag
from .service import get_tags


def home_page_view(request: WSGIRequest):
    # Обязательно! каждая функция view должна принимать первым параметром request.
    all_notes = Note.objects.all().select_related('autor').prefetch_related('tags')
    context: dict = {
        "notes": all_notes
    }
    return render(request, "home.html", context)


def show_note_view(request: WSGIRequest, note_uuid):
    note = get_object_or_404(Note.objects.select_related('autor').prefetch_related('tags'), uuid=note_uuid)
    return render(request, "note.html", {"note": note})


def create_note_view(request: WSGIRequest):
    if not request.user.is_authenticated:
        return redirect(reverse('authentication'))
    if request.method == "POST":
        note = Note.objects.create(
            title=request.POST["title"],
            content=request.POST["content"],
            autor=request.user,
            image=request.FILES.get("noteImage"))

        tags_objects: set[Tag] = set()
        for tag in get_tags(request):
            tag_obj, created = Tag.objects.get_or_create(name=tag)
            tags_objects.add(tag_obj)
        note.tags.set(tags_objects)  # `set` это переопределение всех тегов для заметки.

        return HttpResponseRedirect(reverse('show-note', args=[note.uuid]))

    # Вернется только, если метод не POST.
    return render(request, "create_form.html")


@login_required
def edit_note_view(request: WSGIRequest, note_uuid):
    note = get_object_or_404(Note, uuid=note_uuid)
    if request.user != note.autor:
        return HttpResponseForbidden('Нет прав')

    if request.method == 'POST':
        if not (request.POST['title'] == note.title and request.POST['content'] != note.content and
                not (request.FILES.get('noteImage'))):
            if get_tags(request) != {tag.name for tag in note.tags.all()}:

                note.title = request.POST['title']
                note.content = request.POST['content']
                if request.FILES.get('noteImage'):
                    delete_old_image(note)
                    note.image = request.FILES.get("noteImage")
                note.mod_time = timezone.now()
                note.save()
                tags_objects: set[Tag] = set()
                for tag in get_tags(request):
                    tag_obj, created = Tag.objects.get_or_create(name=tag)
                    tags_objects.add(tag_obj)
                note.tags.set(tags_objects)
            else:
                error = 'Изменений не было'
                return render(request, "edit_form.html", context={'note': note, 'error': error})
        return render(request, "note.html", {"note": note})
    return render(request, "edit_form.html", context={'note': note})


@login_required
def delete_note_view(request: WSGIRequest, note_uuid):
    note = get_object_or_404(Note, uuid=note_uuid)
    if request.user != note.autor:
        return HttpResponseForbidden('Нет прав')
    note.delete()
    return redirect('home')


def show_about_view(request: WSGIRequest):
    return render(request, "about.html")


def list_posts_user(request: WSGIRequest, username):
    context: dict = {
        "notes": Note.objects.filter(autor__username=username)
        .select_related('autor').prefetch_related('tags')
    }
    return render(request, "home.html", context)
