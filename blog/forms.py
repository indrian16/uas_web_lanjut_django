from django import forms
from . models import Article
from ckeditor.widgets import CKEditorWidget

class ArticleForm(forms.ModelForm):
    
    class Meta:
        model = Article
        fields = ("title", "body", "category",)
        widgets = {
            "title": forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder': 'title article',
                    'required': True,
                },
            ),
            "body": forms.CharField(widget=CKEditorWidget()),
            "category": forms.Select(
                attrs = {
                    'class': 'selectpicker',
                    'type': 'text',
                    'placeholder': 'title article',
                    'required': True,
                    'data-style': "btn btn-danger btn-block",
                }
            ),
        }
