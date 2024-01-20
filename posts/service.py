from django.core.handlers.wsgi import WSGIRequest


def get_tags(request: WSGIRequest) -> set:
    # Если нет тегов, то будет пустой список
    tags_names: set = set(request.POST.get("tags", "").split(","))
    tags_names.discard(' ')
    tags_names = set(map(str.strip, tags_names))  # Убираем лишние пробелы

    return tags_names
