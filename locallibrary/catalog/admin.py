from dataclasses import fields
from django.contrib import admin
from .models import *
# Register your models here.
# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Gener)
# admin.site.register(BookInstance)
admin.site.register(Languages)
class BookInline(admin.TabularInline):
    model = Book
    
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'display_languages')
    list_filter = ('first_name', 'date_of_birth', 'lang')
    fieldsets = (
        ('Name', {'fields':('first_name', 'last_name')}),
        ('History', {'fields': ('date_of_birth', 'date_of_death')})      
    )
    inlines = [BookInline]
   
class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    
@admin.register(Book) 
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_gener', 'summery')
    list_filter = ('author', 'gener')

    inlines = [BookInstanceInline]


    
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'borrower') 
    list_filter = ('status', 'due_back') 
    fieldsets = (
        ('Book', {'fields': ('id', 'book', 'imprint')}),
        ('borrow', {'fields': ('borrower','status', 'due_back')}) 
    ) 
    
    
    
    
# # Register the admin class with the associated model
# admin.site.register(Author, AuthorAdmin)
# admin.site.register(Book, BookAdmin)
# admin.site.register(BookInstance,BookInstanceAdmin)
