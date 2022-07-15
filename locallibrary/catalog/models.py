from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
import uuid
from django.contrib.auth.models import User
from datetime import date

class Gener(models.Model):
    name = models.CharField(max_length=100,
                            help_text = 'Enter a book genre (e.g. Science Fiction)')
    def __str__(self):
        return self.name
 
    
class Languages(models.Model):
    
    name = models.CharField(max_length=100,
                            help_text = 'choose a language for the book e.g. Arabic, English, Faresi,etc.')
    def __str__(self):
        return self.name
    
    
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    lang =  models.ManyToManyField(Languages, help_text = 'Choose a languages you write with.')
    
    class Meta: 
        ordering = ['first_name', 'last_name']
              
    def get_absolute_url(self):
         """Returns the url to access a particular author instance."""
         return reverse('author-detail', args=[str(self.id)])
 
    def __str__(self): 
        """String for representing the Model object."""
        return f'{self.first_name} {self.last_name} '  
    def display_languages(self): 
        return ', '.join(lang.name for lang in self.lang.all()[:3])
    display_languages.short_description = 'Language'

  
class Book(models.Model):
    title = models.CharField(max_length=60, help_text="Book title")
    
    author = models.ForeignKey(Author, on_delete = models.SET_NULL, null=True)
    
    summery = models.TextField(max_length = 200,
                               help_text="write a brief summary of the book")
    
    isbn = models.CharField('ISBN', max_length=13, unique=True,
                            help_text = 'ISBN is maximum length of 13')
    
    gener = models.ManyToManyField('Gener', help_text='Select a genre for this book')
    
    lang = models.ForeignKey(Languages, on_delete = models.SET_NULL,
                             null = True)
    
    class Meta:
        permissions = (('view_book_c','View book instances'), ('can_create_book', 'Can create book'))  # 'Can create book' == 'Can edite book' or 'Can change book'
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])
    
    def display_gener(self):
        return ', '.join(gener.name for gener in self.gener.all()[:3])
    display_gener.short_description = 'Gener'
    
    
class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, 
                          help_text = 'Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete = models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    
    status = models.CharField(max_length = 1, choices = LOAN_STATUS,
                              default= 'a', help_text='Book availability',
                              blank = True
                              )   
    
    borrower = models.ForeignKey(User, on_delete= models.SET_NULL, null=True, blank=True) 
    
    class Meta:
        ordering = ['due_back']
        permissions = (('can_mark_returned','Set book as returned'),('can_view_book_instance', 'Can view book instance'))
        
    def __str__(self):
        return f'{str(self.id)} ({self.book.title})'
    
    # Check wither the due_back date has end or not. 
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
    

        
     
        
        
    
    