from cgi import test
import datetime
from urllib import response
from django.test import TestCase, Client
from django.utils import timezone

from catalog.models import *

from django.urls import reverse

from django.contrib.auth.models import User # Required to assign User as a borrower

from django.contrib.auth.models import Permission # Required to grant the permission needed to set a book as returned.

import uuid

"""
Testin List:

 - AuthorListViewTest:
   1 - test_view_url_exist_at_desired_location [Ok].
   2 - test_view_url_accessible_by_name [Ok].
   3 - test_view_uses_correct_tmplate [Ok].
   4 - test_pagination_is_five [Ok].
   5 - test_lists_all_authors [Ok].
    
 - LoanedBookInstancesByUserListViewTest:
   6 - test_redirect_if_not_logged_in [Ok]. ---> You need to use 'fetch_redirect_response=False' with assertRedirect()!!!.
   7 - test_logged_uses_correct_template [Ok].
   8 - test_only_borrowed_books_in_list [Ok].
   9 - test_pages_ordered_by_due_date [Ok].
    
 - RenewBookLibrarianFunctionView:
   10 - test_redirect_if_not_loggedd_in [Ok]. ---> You need to use 'fetch_redirect_response=False' with assertRedirect()!!!.
   11 - forbidden_if_logged_in_but_not_correct_permission [Ok].
   12 - test_logged_in_with_permission_another_user_borrowed [Ok].
   13 - test_HTTP_404_for_invalid_book_if_logged_in [Ok].
   14 - test_uses_correct_template [Ok].
   15 - test_form_renewal_date_initialy_has_date_three_weeks [Ok].
   16 - test_redirects_to_all_borrowed_books_list_on_success [Ok]. ---> You need to use 'fetch_redirect_response=False' with assertRedirect()!!!.
   17 - test_form_invalid_renew_date_past [Ok].
   18 - test_form_invalid_renewal_date_future [Ok].
"""



class AuthorListViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        number_of_authors = 13
        for author_number in range(number_of_authors):
            author = Author.objects.create(
                first_name = f'Ya3rob #{author_number}',
                last_name = f'Al-Harbi #{author_number}'
            )
            
    def test_view_url_exist_at_desired_location(self):
        
        # Assign response from url
        # Write The url like this '/appName/viewName/' .
        response = self.client.get('/catalog/authors/')
        
        # Check the status code is successful (code 200).  
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name(self):
        
        # Assign response from url
        # Write The url like this '/appName/viewName/' .
        response = self.client.get(reverse('authors'))
        
        # Check the status code is successful (code 200).
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_tmplate(self):
        
        # Assign response from url
        # Write The url like this '/appName/viewName/' .
        response = self.client.get(reverse('authors'))
        
        # Check the status code is successful (code 200).
        self.assertEqual(response.status_code, 200)
        
        # Check if the correct template
        self.assertTemplateUsed(response, 'author_list.html' )
    
    
    # Check for the objects since the pagination divided them into several pages,
    # This method for 1st to 5th author objects.
    def test_pagination_is_five(self):
        # Assign response from url
        # Write The url like this '/appName/viewName/' .
        response = self.client.get(reverse('authors'))
        
        # Check the status code is successful (code 200).
        self.assertEqual(response.status_code, 200)
        # Check the page 'is_paginated' is in the request context.
        self.assertTrue('is_paginated' in response.context)
        
        # Check if the 'is_paginated' is True
        self.assertTrue(response.context['is_paginated'] == True)
        
        # Check the length of the pagination is equal to spacific number.
        self.assertEqual(len(response.context['authors']), 5)    
        
    # related to the pagination tests
    def test_lists_authors_6th_tp_10th(self):
        # Assign response from url
        # Write The url like this '/appName/viewName/' .
        response = self.client.get(reverse('authors')+ '?page=2')
        
        # Check the status code is successful (code 200).
        self.assertEqual(response.status_code, 200)
        
        # Check if the target object is in the request context.
        self.assertTrue('authors' in response.context)
       
        # # Check the length of the list is n
        # self.assertEqual(len(response.context['authors']), 13)
        
         # Check the page 'is_paginated' is in the request context.
        self.assertTrue('is_paginated' in response.context)
        
        # Check if the 'is_paginated' is True
        self.assertTrue(response.context['is_paginated'] == True)
        
        # Check the length of the pagination is equal to spacific number.
        self.assertEqual(len(response.context['authors']), 5)
           
    # related to the pagination tests
    def test_lists_authors_11th_tp_13th(self):
        
        # Assign response from url
        # Write The url like this '/appName/viewName/' .
        response = self.client.get(reverse('authors')+ '?page=3')
        
        # Check the status code is successful (code 200).
        self.assertEqual(response.status_code, 200)
        
        # Check if the target object is in the request context.
        self.assertTrue('authors' in response.context)
       
        # # Check the length of the list is n
        # self.assertEqual(len(response.context['authors']), 13)
        
         # Check the page 'is_paginated' is in the request context.
        self.assertTrue('is_paginated' in response.context)
        
        # Check if the 'is_paginated' is True
        self.assertTrue(response.context['is_paginated'] == True)
        
        # Check the length of the pagination is equal to spacific number.
        self.assertEqual(len(response.context['authors']), 3)
    

class LoanedBookInstancesByUserListViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Create two users
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        
        test_user1.save()
        test_user2.save()
        
        test_author = Author.objects.create(first_name = 'Ya3rb',
                                            last_name = 'Al-Harbi')
        
        test_gener = Gener.objects.create(name = 'Fantacy')
        
        test_language = Languages.objects.create(name = 'Arabic')
        
        
        test_book = Book.objects.create(
            title = 'Testing Book',
            summery = 'Testing Book Summery',
            isbn = 'ABCDEFG',
            author = test_author,
            lang = test_language
        )
        
        
        gener_objects_for_book = Gener.objects.all()
        
        # Direct Assignment for Many to Many field.
        test_book.gener.set(gener_objects_for_book)
        
        test_book.save()
        
        
        number_of_book_copies = 30
        
        for book_copy in range(number_of_book_copies):
            return_date = timezone.localtime() + datetime.timedelta(days = book_copy%5)
            the_borrower = test_user1 if book_copy % 2 else test_user2
            status = 'm'
            
            BookInstance.objects.create(
                book = test_book,
                imprint = 'Unlikely Imprint, 2016',
                due_back = return_date,
                borrower = the_borrower,
                status = status,
            )
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/catalog/mybooks/')
        
        # Use "fetch_redirect_response" to avoid 404 error from the assertRedirects function.
        self.assertRedirects(response, '/accounts/login/?next=/catalog/mybooks/', fetch_redirect_response=False)
        
    def test_logged_uses_correct_template(self):
        login = self.client.login(username = 'testuser1', password = '1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-borrowed'))
        
        self.assertEqual(str(response.context['user']), 'testuser1')
        
        self.assertEqual(response.status_code, 200)
        
        self.assertTemplateUsed(response, 'user/bookinstance_list_borrowed_user.html')
        
    def test_only_borrowed_books_in_list(self):
        login = self.client.login(username = 'testuser1', password = '1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-borrowed'))
        
        # Check if user is logged-in
        self.assertEqual(str(response.context['user']), 'testuser1')
        
        
        self.assertEqual(response.status_code, 200)
        
        self.assertTrue('bookinstace_list' in response.context)
        
        self.assertEqual(len(response.context['bookinstance_list']),0)
        
        # Change all Bookinstances with status 'o'.
        books = BookInstance.objects.all()[:10]
        
        for book in books:
            book.status = 'o'
            book.save()
            
        response = self.client.get(reverse('my-borrowed'))
        
        self.assertEqual(response.context['user'], 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('bookinstance' in response.context)
        
        for bookitem in response.context['bookinstance_list']:
            self.assertEqual(response.context['user'], bookitem.borrower)
            self.assertEqual(bookitem.status, 'o')
            
    def test_pages_ordered_by_due_date(self):
        for bookitem in BookInstance.objects.all():
            bookitem.status = 'o'
            bookitem.save()
        
        login = self.client.login(username = 'testuser1', password = '1X<ISRUkw+tuK')
        response = self.client.get(reverse('authors'))
        
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        
        self.assertTrue('bookinstance_list' in response.context)
       
        self.assertEqual(len(response.context['bookinstance_list']), 10)
        
        last_date = 0
        for bookitem in response.context['bookinstance_list']:
            if last_date == 0:
                last_date = bookitem.due_back
            else:
                self.assertTrue(last_date <= bookitem.due_back)
                last_date = bookitem.due_back
   
                
class RenewBookLibrarianFunctionView(TestCase):
    
    def setUp(self):
        # Create users
        test_user1 = User.objects.create_user(username = 'TestUser1', 
                                              password = '1X<ISRUkw+tuK')
        
        test_user2 = User.objects.create_user(username = 'TestUser2',
                                             password = '2HJ1vRV0Z&3iD')
        
        test_user1.save()
        test_user2.save()
        
        
        # Give user permission
        permission = Permission.objects.get(name = 'Set book as returned')
        test_user2.user_permissions.add(permission)
        test_user2.save()
        
        
        # Create a book
        test_author = Author.objects.create(first_name = 'Ya3rob', last_name = 'Al-Harbi')
        test_gener = Gener.objects.create(name = 'Fantacy')
        test_language = Languages.objects.create(name = 'Arabic')
        test_book = Book.objects.create(
            title = 'Testing Book',
            summery = 'Testing Book Summery',
            isbn = 'ABCDEFG',
            author = test_author,
            lang = test_language,
        )
        
        # Set gener to book
        
        # Direct assignment not allowed for ManyToMany fields.
        gener_objects_for_book = Gener.objects.all()
        test_book.gener.set(gener_objects_for_book)
        
        test_book.save()
        
        
        # Create Book Instace for test_user1
        renew_date = datetime.date.today() + datetime.timedelta(days = 5)
        
        self.test_book_instance1 = BookInstance.objects.create(
            book = test_book,
            imprint = 'Unlikely imprint, 2022',
            borrower = test_user1,
            status = 'o'
        )
        
        # Create Book Instace for test_user1
        renew_date = datetime.date.today() + datetime.timedelta(days = 5)
        
        self.test_book_instance2 = BookInstance.objects.create(
            book = test_book,
            imprint = 'Unlikely imprint, 2022',
            borrower = test_user2,
            status = 'o'
        )
         
    def test_redirect_if_not_loggedd_in(self):
       
        response = self.client.get(reverse('renew-book-librarians', kwargs ={'pk': self.test_book_instance1.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
        
    def forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username = 'TestUser1', password= '1X<ISRUkw+tuK')
        response = self.client.get(reverse('renew-book-librarians', kwargs={'pk': self.test_book_instance1.pk}))
        self.assertEqual(response.status_code, 403)
        
    def test_logged_in_with_permission_borrowed_book(self):
        login = self.client.login(username = 'TestUser2', password = '2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew-book-librarians', kwargs= {'pk': self.test_book_instance2.pk}))
        self.assertEqual(response.status_code, 200)
        
    def test_logged_in_with_permission_another_user_borrowed(self):
        login = self.client.login(username = 'TestUser2', password = '2HJ1vRV0Z&3iD')
        
        response = self.client.get(reverse('renew-book-librarians', kwargs= {'pk': self.test_book_instance1.pk}))
        self.assertEqual(response.status_code, 200)
        
        
    def test_HTTP_404_for_invalid_book_if_logged_in(self):
        test_uid = uuid.uuid4()

        login = self.client.login(username = 'TestUser2', password = '2HJ1vRV0Z&3iD')    
        
        response = self.client.get(reverse('renew-book-librarians', kwargs= {'pk': test_uid}))
        self.assertEqual(response.status_code, 404)   
        
    def test_uses_correct_template(self):
        login = self.client.login(username = 'TestUser2', password = '2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew-book-librarians', kwargs= {'pk': self.test_book_instance1.pk}))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Librarian/book_renew_librarian.html') 
        
    def test_form_renewal_date_initialy_has_date_three_weeks(self):
        login = self.client.login(username = 'TestUser2', password = '2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('renew-book-librarians', kwargs= {'pk': self.test_book_instance1.pk}))
        self.assertEqual(response.status_code, 200)
        
        three_weeks_in_future = datetime.date.today() + datetime.timedelta(weeks=3)
        self.assertEqual(response.context['form'].initial['due_back'], three_weeks_in_future)
        
    def test_redirects_to_all_borrowed_books_list_on_success(self):
        login = self.client.login(username= 'TestUser2', password = '2HJ1vRV0Z&3iD')
        
        valid_date_in_the_future = datetime.date.today() + datetime.timedelta(weeks=2)
        
        response = self.client.post(reverse('renew-book-librarians', kwargs={'pk': self.test_book_instance1.pk}), 
                                    {'due_back': valid_date_in_the_future})
        
        self.assertRedirects(response, reverse('all-borrowed-books'), fetch_redirect_response=False)
          
    def test_form_invalid_renew_date_past(self):
        
        login = self.client.login(username= 'TestUser2', password = '2HJ1vRV0Z&3iD')
        past_date = datetime.date.today() - datetime.timedelta(weeks=1)
        
        response = self.client.post(reverse('renew-book-librarians', kwargs={'pk': self.test_book_instance1.pk}), 
                                    {'due_back': past_date})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'due_back', 'Invalid date - renewal in past')
        
        
    def test_form_invalid_renewal_date_future(self):
        login = self.client.login(username= 'TestUser2', password = '2HJ1vRV0Z&3iD')
        
        renewal_date_future = datetime.date.today() + datetime.timedelta(weeks=5)
        
        response = self.client.post(reverse('renew-book-librarians', kwargs={'pk': self.test_book_instance1.pk}), 
                                   {'due_back': renewal_date_future})
        
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'due_back', 'Invalid date - renewal more than 4 weeks ahead')
        