from django.core.handlers.wsgi import WSGIRequest


class PostsHistory:
    KEY_DEFAULT = 'history'

    def __init__(self, request: WSGIRequest):
        self._sessions = request.session

        if PostsHistory.KEY_DEFAULT not in self._sessions.keys():
            self._sessions.setdefault(PostsHistory.KEY_DEFAULT, [])

    def _remove_history(self, index=0) -> None:
        self._sessions[PostsHistory.KEY_DEFAULT].pop(index)

    def add_history(self, note_uuid, limit=20) -> None:
        if len(self._sessions[PostsHistory.KEY_DEFAULT]) >= limit:
            self._remove_history()
        if note_uuid not in self._sessions[PostsHistory.KEY_DEFAULT]:
            self._sessions[PostsHistory.KEY_DEFAULT].append(note_uuid)
            self._sessions.save()

    def clear_all_history(self) -> None:
        self._sessions[PostsHistory.KEY_DEFAULT].clear()
        self._sessions.save()

    def get_history(self) -> list[str]:
        return self._sessions[PostsHistory.KEY_DEFAULT]
