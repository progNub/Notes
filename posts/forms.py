from django import forms
from django_select2.forms import Select2Widget, Select2TagWidget

from posts.models import Note, Tag


class MySelect2Widget(Select2TagWidget):
    allow_multiple_selected = True



class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'image', 'tags']

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            'content': forms.Textarea(attrs={"class": "form-control"}),
            'image': forms.FileInput(attrs={"class": "form-control"}),
            'tags': MySelect2Widget(attrs={"class": "form-control"}),
        }
