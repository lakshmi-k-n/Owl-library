from django.contrib import admin

# Register your models here.
from .models import Author, Book
# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    ''''
            
    '''
    list_display = (
        'id',
        'name',
    )

class BookAdmin(admin.ModelAdmin):
    ''''
            
    '''
    list_display = (
        'id',
        'title',
        'get_author_name',
    )
    def get_author_name(self, obj):
        return obj.author.name

admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
