from django import forms

from posts.models import Note, Tag
from posts.service import get_tags


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'image', 'tags']

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            'content': forms.Textarea(attrs={"class": "form-control"}),
            'image': forms.FileInput(attrs={"class": "form-control"}),
            'tags': forms.SelectMultiple(attrs={"class": "form-control"}),
        }


