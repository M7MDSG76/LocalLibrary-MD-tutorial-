from django.urls import path, include
from . import views
#  from django.contrib.auth.urls
urlpatterns = [
    path('', views.index, name = 'index'),
    path('books/', views.BookListView.as_view(), name = 'books'),
    path('authors/', views.AuthorListView.as_view(), name = 'authors'),
    path('gener/', views.GenerListView.as_view(), name = 'geners'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name = 'book-detail'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name = 'author-detail'),
    
    #Add Django site authentication urls (for login, logout, password management)
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Url path to the user borrowed book page (only loged-in users can access).
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name = 'my-borrowed'),
    
    # All borrowed books page (only librarians can access).
    path('borrowedbooks/', views.AllLoanedBooksListView.as_view(), name = 'all-borrowed-books'),
    
    # Renewal date page (Only librarians can access)
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name= 'renew-book-librarians'),
    
    
    # Author Edite urls.
    path('author/create/', views.AuthorCreate.as_view(), name= 'author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name= 'author-update'),
    path('author/<int:pk>/delete', views.AuthorDelete.as_view(), name= 'author-delete'),
    
    # Book Edite urls.
    path('book/create/', views.BookCreate.as_view(), name= 'book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name= 'book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name= 'book-delete'),
    
    
    
    
]

