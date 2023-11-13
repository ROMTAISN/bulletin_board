from django import forms
from django.core.exceptions import ValidationError

from tinymce.widgets import TinyMCE

from .models import Post, Responses


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=40)
    content = forms.CharField(widget=TinyMCE())

    class Meta:
        model = Post
        fields = [
            'title',
            'category_post',
            'content',
        ]

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if title == content:
            raise ValidationError('Текст не должен быть идентичен названию.')

        return cleaned_data


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Responses
        fields = ['res_content']

        widgets = {
            'res_content': forms.TextInput(),
        }
