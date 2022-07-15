from turtle import title
from django.test import TestCase
from catalog.models import Author, Book



class AuthorModelTest(TestCase):
    
    # Responsible for
    @classmethod
    def setUpTestData(cls):
        first_name ='mohammed'
        last_name = 'alghanmi'
        author = Author.objects.create(first_name = first_name, last_name= last_name)

    def test_authorFirstNameLabel(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')
        
    def test_authorLastNameLabel(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')
        
    def test_authorDateOfDreathLabel(self):
        author = Author.objects.get(id = 1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'Died')
        
    def test_authorFirstNameMaxLength(self):
        author = Author.objects.get(id = 1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)
        
    def test_authorLastNameMaxLength(self):
        author = Author.objects.get(id = 1)
        max_length = author._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 100)
        
    def test_authorGetAbsoluteURL(self):
        author = Author.objects.get(id = 1)
        self.assertEqual(author.get_absolute_url(), '/catalog/author/1')
    
    def test_author_object_name_equals_first_name_space_last_name(self):
        author = Author.objects.get(id = 1)
        expected_object_name = f'{author.first_name} {author.last_name} '
        self.assertEqual(str(author), expected_object_name)
        
        
class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        title = 'Book Title asaaaadasfsssssssssssssssssssssssdsssssssssssssss'
        author = Author.objects.create(first_name = 'Mohammed', last_name= 'Alghanmi')
        book = Book.objects.create(title = title, author = author, isbn = '1234567890123', )
    
    def test_book_title_max_length(self):
        book = Book.objects.get(id = 1)
        title_max_length = book._meta.get_field('title').max_length  
        
        def is_less_than_or_equal_limit(title_length, limit):
            if title_length <= limit:
                return True
            return False
            
        self.assertTrue(is_less_than_or_equal_limit(title_max_length, 60))
    
    def test_book_isbn_max_length(self):
        book = Book.objects.get(id = 1)
        isbn_max_length = book._meta.get_field('isbn').max_length
        
        self.assertEqual(isbn_max_length, 13)
        
    def test_book_absolute_url(self):
        book = Book.objects.get(id = 1)
        book_absolute_url = book.get_absolute_url()
        
        self.assertEqual(book_absolute_url, '/catalog/book/1')
    
    def test_book__str__(self):
        book = Book.objects.get(id = 1)
        
        self.assertEqual(str(book), 'Book Title asaaaadasfsssssssssssssssssssssssdsssssssssssssss')