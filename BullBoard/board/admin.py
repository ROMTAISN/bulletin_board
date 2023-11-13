from django.contrib import admin
from tinymce.widgets import TinyMCE

from .models import *
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_post', 'category_post', 'content')
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }


admin.site.register(Responses)
admin.site.register(Post, PostAdmin)
