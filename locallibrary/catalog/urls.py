from django.urls import path, include
from . import views

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
    path('book/<uuid:pk>/renew/', views.renew_book_librarians, name = 'renew-book-librarians'),
    
    
]

